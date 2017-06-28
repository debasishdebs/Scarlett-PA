from GreyMatter import general_conversations, tell_time, get_wheather, get_youtube


def brain(name, speech_text):

    def check_message(check):
        words_of_message = speech_text.split()
        check = check.split()

        if set(check).issubset(set(words_of_message)):
            return True
        else:
            return False

    if check_message("who are you"):
        general_conversations.who_are_you()
        return True
    elif check_message("tell a joke"):
        general_conversations.tell_joke()
        return True
    elif check_message("how am i") or check_message("how do i look"):
        general_conversations.how_am_i()
        return True
    elif check_message("how are you"):
        general_conversations.how_are_you()
        return True
    elif check_message("where are you born") or check_message("where were you born") or check_message("what is your birthplace"):
        general_conversations.where_born()
        return True
    elif check_message("tell about yourself"):
        general_conversations.who_are_you()
        general_conversations.where_born()
        return True
    elif check_message("what time"):
        tell_time.what_is_time()
        return True
    elif check_message("weather today") or check_message("weather today"):
        get_wheather.GetWeather()
        return True
    elif check_message("play"):
        # print(speech_text)
        obj = get_youtube.GetYoutubeMusic(speech_text)
        obj.run_()
        return True
    else:
        general_conversations.undefined(speech_text)
        return False
