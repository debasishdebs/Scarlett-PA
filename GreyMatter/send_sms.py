# Currently supports:
# 1:Whatsapp
# 2: Messenger
# 3: SMS

import pandas as pd
from whatsapp import Client


class SendWhatsapp(object):
    def __init__(self, contactName):
        self.nameToSearch = contactName
        pass

    def __driver_(self):
        self.contacts = self.__read_contacts_()
        self.contact_number = self.__fetch_number_()
        pass

    def __read_contacts_(self):
        df = pd.read_csv("Contacts.csv")
        return df

    def __fetch_number_(self):
        contact_number = self.contacts.loc['NAME' == self.nameToSearch][['PHONE', 'EMAIL']]
        return contact_number

    def __send_(self):

        return


class SendMessenger(object):
    def __init__(self):
        pass


class SendSMS(object):
    def __init__(self):
        pass
