# Currently supports:
# 1:Whatsapp
# 2: Messenger
# 3: SMS

import pandas as pd
# from whatsapp import Client
import config as cfg
from fbchat import Client
from pushbullet import Pushbullet
import creds as cr


class ContactDriver(object):
    def __init__(self):
        self.__driver__()
        pass

    def __driver__(self):
        self.contacts = self.__read_contacts_()
        pass

    def __read_contacts_(self):
        import os
        df = pd.read_csv(os.path.abspath(cfg.CONTACTS_DUMP_CSV))
        return df

    def fetch_contact(self, contactName):
        contact_details = self.contacts[self.contacts['NAME'] == contactName][['NAME', 'PHONE', 'EMAIL']]

        return contact_details


class SendWhatsapp(object):
    def __init__(self, contactName):
        self.nameToSearch = contactName
        pass

    def __driver_(self):
        self.contactObj = ContactDriver()
        pass

    def __initialize_client_(self):
        self.client = Client()
        pass

    def __fetch_number_(self):
        contact_number = self.contactObj.fetch_contact(self.nameToSearch)
        return contact_number

    def send(self, message):

        return


class SendMessenger(object):
    def __init__(self):
        self.__driver_()
        pass

    def __initialize_clinet_(self):
        self.client = Client("d.kanhar@gmail.com", "2NInitu!1")
        pass

    def __deinitialize_client_(self):
        self.client.logout()
        pass

    def send(self, message, contactName):
        try:
            user = self.client.searchForUsers(contactName)[0]

            uid = user.uid

            self.client.sendMessage(message, thread_id=uid)

            self.__deinitialize_client_()

            return True
        except:
            return False

        pass

    def __driver_(self):
        self.__initialize_clinet_()
        users = self.client.fetchAllUsers()
        pass


class SendSMS(object):
    def __init__(self):
        self.__driver_()
        pass

    def __initialize_clinet_(self):
        self.client = Pushbullet(cr.PUSHBULLET_API_KEY)
        pass

    def __driver_(self):
        self.contactObj = ContactDriver()
        self.__initialize_clinet_()
        pass

    def send(self, message, contactName):
        contact_number = self.contactObj.fetch_contact(contactName)
        print(contact_number)
        number = str(contact_number['PHONE'].values[0])
        number = number.replace(" ", "")

        print(number)
        device = self.client.devices[0]

        self.client.push_sms(device, number, message)
        pass


if __name__ == '__main__':
    # obj = SendMessenger()
    # obj.send("Hi. This is check. I'm texting u using my JARVIS, i.e. Scarlett!", "Ayushi Verma")
    obj = SendSMS()
    obj.send("Hi. This is test. Sending SMS from Scarlett!", "Ayushi Verma")
