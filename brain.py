from GreyMatter import general_conversations, tell_time


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
    elif check_message("tell a joke"):
        general_conversations.tell_joke()
    elif check_message("how am i") or check_message("how do i look"):
        general_conversations.how_am_i()
    elif check_message("how are you"):
        general_conversations.how_are_you()
    elif check_message("where are you born") or check_message("where were you born") or check_message("what is your birthplace"):
        general_conversations.where_born()
    elif check_message("tell about yourself"):
        general_conversations.who_are_you()
        general_conversations.where_born()
    elif check_message("what time"):
        tell_time.what_is_time()
    else:
        general_conversations.undefined()
