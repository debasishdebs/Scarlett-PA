import urllib
import urllib2
from bs4 import BeautifulSoup
import pafy
import os
import config as cfg
import creds as cr


class GetYoutubeMusic(object):
    def __init__(self):
        pass

    def __driver__(self):
        return

    def run_(self):
        pass


def search_video(songToSearch, speechSpoken):
    query = urllib.quote(songToSearch)
    url = cfg.YOUTUBE_SEARCH_URL + query
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)

    urls = []
    for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
        url_vid = 'https://www.youtube.com' + vid['href']
        urls.append(url_vid)

    vid_metadata = dict()
    ctr = 0
    views_count = dict()
    for url in urls:
        if "watch?v=" in url:
            video = pafy.new(url)
            vid_metadata[str(ctr)] = {'url': url, 'rating': video.rating, 'views': video.viewcount, 'likes': video.likes, 'title': video.title}
            views_count[str(ctr)] = video.viewcount
            ctr += 1

    print(vid_metadata)

    # First search weather the spoken speech is subset of any of songs fetched!
    # If yes, and it is multiple then select one with max views.
    # If one video, play that.
    # Else play the one with maximum views.
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

    best_video = vid_metadata[key_to_video]
    url = best_video['url']
    video = pafy.new(url)
    audiostreams = video.audiostreams

    from SenseCells.tts import tts
    tts(video.title)

    # Download the best file with m4a extenstion, as cant play webm files which is default!
    # bestaudio = video.getbestaudio(preftype='m4a')
    # bestaudio.download(quiet=False, filepath=os.getcwd()+"/../../../Songs/")

    # Download webm file, lowest resolution
    song = audiostreams[0].download(quiet=False, filepath=os.getcwd()+cfg.YOUTUBE_SONG_PATH)
    print(audiostreams)
    print(song)
    print(song[:-5]+'.mp3')
    song_origin = song
    song_source = song[:-5]+'.mp3'

    # Convert webm to m4a using subprocess
    import pipes
    cmd = cfg.YOUTUBE_FFMPEG_FORMAT_CONVERT.format(pipes.quote(os.path.abspath(song_origin)),
                                              pipes.quote(os.path.abspath(song_source)))
    print(cmd)
    os.system(cmd)

    cmd = "mplayer {}".format(pipes.quote(os.path.abspath(song_source)))
    print(cmd)
    os.system(cmd)

    pass


def identify_artist(speech):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.abspath(os.getcwd() + cr.GOOGLE_APP_NLP_CRED_PATH)
    print(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])

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
    from pprint import pprint
    # pprint(response)
    # print(50*"-")

    # Using IBM Watson Natural Language Understanding API
    import watson_developer_cloud
    import watson_developer_cloud.natural_language_understanding.features.v1 as features

    nlu = watson_developer_cloud.NaturalLanguageUnderstandingV1(version=cr.IBM_WDC_NLUV1_VERSION,
                                                                username=cr.IBM_WDC_NLUV1_USERNAME,
                                                                password=cr.IBM_WDC_NLUV1_PASSWORD)
    ret = nlu.analyze(text=speech, features=[features.Entities(), features.Keywords()])

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
        if 'play' in speech.lower():
            play_action = True

    # print(play_action)

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


def main(speech):
    query = identify_artist(speech)
    search_video(query, speech)
    # Prompt user weather the song intended was played or not. If no, take feedback. This feedback is where ML comes in!


if __name__ == '__main__':

    main("Play one love by Justin Bieber")
