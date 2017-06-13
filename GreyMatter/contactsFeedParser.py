import pickle
import pandas as pd


class googleContactsFeedParser(object):
    def __init__(self):

        pass

    def parse_(self, message=None, deep=True):
        # print(message is not None)
        df = self.__create_frame_structure__()
        # print(df)
        if message is not None:
            f = open("contactsFeed.pkl", "wb+")
            if deep:
                pickle.dump(message, f)

                df = self.parserEngine(str(message))

            f.close()
        else:
            f = open("contactsFeed.pkl", "rb+")
            message = pickle.load(f)
            message = str(message)

            df = self.parserEngine(message)

            f.close()

        self.contacts = df

        pass

    def get_(self):
        return self.contacts

    def parserEngine(self, message):
        indices_start = list(self.find_all(message, "<ns0:entry ns1:etag="))
        indices_end = list(self.find_all(message, "/ns0:entry"))

        contacts = dict()

        for i in range(len(indices_start)):
            start = indices_start[i]
            end = indices_end[i]

            substring = message[start:end]
            # print(substring)
            # print(100*"-")

            substring_start_name = list(self.find_all(substring, "<ns0:title>"))
            substring_end_name = list(self.find_all(substring, "</ns0:title"))

            for j in range(len(substring_start_name)):
                s_s_n = substring_start_name[j]
                s_e_n = substring_end_name[j]

                name = substring[s_s_n:s_e_n]
                name = name.replace("<ns0:title>", "")

                contacts[name] = dict()

        # print(contacts)
        for i in range(len(indices_start)):
            start = indices_start[i]
            end = indices_end[i]

            substring = message[start:end]

            for name in contacts.keys():
                substring_start_name = list(self.find_all(substring, "<ns0:title>"))
                substring_end_name = list(self.find_all(substring, "</ns0:title"))

                for j in range(len(substring_start_name)):
                    s_s_n = substring_start_name[j]
                    s_e_n = substring_end_name[j]

                    n = substring[s_s_n:s_e_n]
                    n = n.replace("<ns0:title>", "")

                    if n == name:
                        email = ''
                        substring_start_email = list(self.find_all(substring, "<ns1:email address=\""))
                        substring_end_email = list(self.find_all(substring, "\" primary=\"true\" rel="))

                        for k in range(len(substring_end_email)):
                            s_s_e = substring_start_email[k]
                            s_e_e = substring_end_email[k]
                            email = substring[s_s_e:s_e_e]
                            email = email.replace("<ns1:email address=\"", "")

                        if email != '':
                            contacts[name]['EMAIL'] = email
                        else:
                            contacts[name]['EMAIL'] = pd.np.nan
                        pass

        for i in range(len(indices_start)):
            start = indices_start[i]
            end = indices_end[i]

            substring = message[start:end]

            for name in contacts.keys():
                substring_start_name = list(self.find_all(substring, "<ns0:title>"))
                substring_end_name = list(self.find_all(substring, "</ns0:title"))

                for j in range(len(substring_start_name)):
                    s_s_n = substring_start_name[j]
                    s_e_n = substring_end_name[j]

                    n = substring[s_s_n:s_e_n]
                    n = n.replace("<ns0:title>", "")

                    if n == name:
                        phone = ''
                        substring_start_phone = list(self.find_all(substring, "<ns1:phoneNumber"))
                        substring_end_phone = list(self.find_all(substring, "/ns1:phoneNumber>"))

                        for k in range(len(substring_end_phone)):
                            s_s_e = substring_start_phone[k]
                            s_e_e = substring_end_phone[k]
                            phone = substring[s_s_e:s_e_e]
                            to_clean = phone[phone.find("<"):phone.find(">")]
                            phone = phone.replace(to_clean, "")
                            phone = phone.replace("<", "")
                            phone = phone.replace(">", "")

                        if phone != '':
                            contacts[name]['PHONE'] = phone
                        else:
                            contacts[name]['PHONE'] = pd.np.nan
                        pass

        df = pd.DataFrame.from_dict(contacts, orient='index')
        df = df.reset_index()
        df = df.rename(columns={"index": "NAME"})
        print(df)

        df.to_csv("Contacts.csv")
        return df

    def find_all(self, a_str, sub):
        start = 0
        while True:
            start = a_str.find(sub, start)
            if start == -1:
                return
            yield start
            start += len(sub)

    def fetch_(self):
        return self.contacts

    def __create_frame_structure__(self):
        df = pd.DataFrame(columns=['NAME', 'EMAIL', 'PHONE1', 'PHONE2', 'PHONE3', 'PHONE4'])
        return df

if __name__ == '__main__':

    obj = googleContactsFeedParser()
    obj.parse_()
