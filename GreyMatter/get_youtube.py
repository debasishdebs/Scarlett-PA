import urllib
import urllib2
from bs4 import BeautifulSoup
import pafy
import os
import config as cfg
import creds as cr
from pprint import pprint
import pipes
import watson_developer_cloud
import watson_developer_cloud.natural_language_understanding.features.v1 as features


class GetYoutubeMusic(object):
    def __init__(self, speech):
        self.speech = speech

        self.WDC_NLUV1_VERSION = cr.IBM_WDC_NLUV1_VERSION
        self.WDC_NLUV1_USERNAME = cr.IBM_WDC_NLUV1_USERNAME
        self.WDC_NLUV1_PWD = cr.IBM_WDC_NLUV1_PASSWORD

        self.YT_SEARCH_URL = cfg.YOUTUBE_SEARCH_URL
        self.YT_SAVED_PATH = cfg.YOUTUBE_SONG_PATH

        self.CONVERT_AUDIO_FFMPEG_COMMAND = cfg.YOUTUBE_FFMPEG_FORMAT_CONVERT
        pass

    def __driver__(self):
        self.query = self.identify_artist()
        return

    def run_(self):
        self.__driver__()
        self.search_video()
        pass

    def identify_artist(self):
        # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.abspath(os.getcwd() + cr.GOOGLE_APP_NLP_CRED_PATH)
        # print(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])

        # Using Google Cloud API
        # from googleapiclient import discovery
        # import httplib2
        # from oauth2client.client import GoogleCredentials
        #
        # DISCOVERY_URL = cr.GOOGLE_APP_NLP_DISCOVERY_URL
        #
        # http = httplib2.Http()
        #
        # credentials =
        # GoogleCredentials.get_application_default().create_scoped(['https://www.googleapis.com/auth/cloud-platform'])
        # credentials.authorize(http)
        #
        # service = discovery.build('language', 'v1beta2', http=http, discoveryServiceUrl=DISCOVERY_URL)
        #
        # service_request = service.documents().annotateText(
        #     body={
        #         'document': {
        #             'type': 'PLAIN_TEXT',
        #             'content': speech
        #         },
        #         'features': {
        #             'extractSyntax': False,
        #             'extractEntities': True,
        #             'extractDocumentSentiment': False
        #         }
        #     })
        #
        # response = service_request.execute()

        # Using IBM Watson Natural Language Understanding API

        nlu = watson_developer_cloud.NaturalLanguageUnderstandingV1(version=self.WDC_NLUV1_VERSION,
                                                                    username=self.WDC_NLUV1_USERNAME,
                                                                    password=self.WDC_NLUV1_PWD)
        ret = nlu.analyze(text=self.speech, features=[features.Entities(), features.Keywords()])

        pprint(ret)

        # Going forward with IBM Watson APIs
        keywords = ret['keywords']
        key = []
        for elem in keywords:
            key.append(elem['text'])

        # If Play is present in any of Keywords:
        # If yes, check if any Artist or Music group present in other Keywords.
        # If yes, fetch other keywords, and use that as text to search for song of particular artist!
        play_action = False

        for elem in key:
            if 'play' in elem.lower():
                play_action = True
        if not play_action:
            if 'play' in self.speech.lower():
                play_action = True

        # If Play_Action is True, we need to call search_video function
        if play_action:
            search_query = ''

            entities = ret['entities']
            entities = entities[0]

            ty = entities['type']
            text = entities['text']

            if ty == 'MusicGroup' or ty == 'Person' or ty == 'Company':
                # Means it corresponds to particular artist of Musical Band!
                search_query += text + ' '
                for elem in key:
                    if 'play' not in elem.lower():
                        if text not in elem.lower():
                            search_query += elem + ' '
            print(search_query)

        return search_query

    def get_best_video(self, vid_metadata, views_count):
        # First search weather the spoken speech is subset of any of songs fetched!
        # If yes, and it is multiple then select one with max views.
        # If one video, play that.
        # Else play the one with maximum views.

        speechSpoken = self.speech

        video_titles = []
        for k, v in vid_metadata.items():
            name = v['title']
            words_in_speech = speechSpoken.split()
            name = name.split()

            if set(name).issubset(set(words_in_speech)):
                video_titles.append([v['title'], k])

        if len(video_titles) > 1:
            # Select video with max views
            max_views = 0
            key_to_video = ''
            for elem in video_titles:
                key = elem[1]
                video_data = vid_metadata[key]
                if max_views == 0:
                    max_views = video_data['views']
                    key_to_video = key
                else:
                    if max_views < video_data['views']:
                        max_views = video_data['views']
                        key_to_video = key

        elif len(video_titles) == 1:
            key_to_video = video_titles[0][1]
            pass
        else:
            # When no video found, then play the one with max views.
            get_max_views = 0
            get_max_views_key = 0
            for k, v in views_count.items():
                if views_count[k] > get_max_views:
                    get_max_views = v
                    get_max_views_key = k

            key_to_video = get_max_views_key

            pass

            # We need to generate logic which takes weighted average of Ratings, Likes & Views to get best video.
            # Now, simple best video is one with max Views.
        return key_to_video

    def download_video(self, best_video):
        url = best_video['url']
        video = pafy.new(url)
        audiostreams = video.audiostreams

        # Download the best file with m4a extenstion, as cant play webm files which is default!
        # bestaudio = video.getbestaudio(preftype='m4a')
        # bestaudio.download(quiet=False, filepath=os.getcwd()+"/../../../Songs/")

        # Download webm file, lowest resolution
        song = audiostreams[0].download(quiet=False, filepath=os.getcwd() + self.YT_SAVED_PATH)
        print("SAVED AT ", song)
        return song

    def convert_audio(self, song, TO='.mp3'):
        song_origin = song
        k = song.rfind(".")
        song_dest = song[:k] + '{}'.format(TO)

        # Convert webm to m4a using subprocess
        cmd = self.CONVERT_AUDIO_FFMPEG_COMMAND.format(pipes.quote(os.path.abspath(song_origin)),
                                                       pipes.quote(os.path.abspath(song_dest)))

        os.system(cmd)
        return song_dest

    def play_audio(self, source):
        try:
            cmd = "mplayer {}".format(pipes.quote(os.path.abspath(source)))
            os.system(cmd)
            return True
        except:
            return False

    def search_video(self):
        songToSearch = self.query
        speechSpoken = self.speech

        query = urllib.quote(songToSearch)
        url = self.YT_SEARCH_URL + query
        response = urllib2.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html)

        urls = []
        for vid in soup.findAll(attrs={'class': 'yt-uix-tile-link'}):
            url_vid = 'https://www.youtube.com' + vid['href']
            urls.append(url_vid)

        vid_metadata = dict()
        ctr = 0
        views_count = dict()
        for url in urls:
            if "watch?v=" in url:
                video = pafy.new(url)
                vid_metadata[str(ctr)] = {'url': url, 'rating': video.rating, 'views': video.viewcount,
                                          'likes': video.likes, 'title': video.title}
                views_count[str(ctr)] = video.viewcount
                ctr += 1

        key_to_video = self.get_best_video(vid_metadata, views_count)

        best_video = vid_metadata[key_to_video]

        song = self.download_video(best_video)

        song_dest = self.convert_audio(song)

        print(song_dest, " is the full path to play")

        ret = self.play_audio(song_dest)

        if ret:
            pass
        else:
            print("Error encountered while playing audio")

        pass


if __name__ == '__main__':

    get_yt_obj = GetYoutubeMusic("Play a song by Justin Beiber")
    get_yt_obj.run_()
