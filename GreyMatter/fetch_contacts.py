def backup():
    def t3():
        import gdata.gauth
        # import webbrowser
        from selenium import webdriver
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.common.by import By

        CLIENT_ID = '428607628598-dd19u5f3ma4rssk8sbm1ccjsbe3pq1ip.apps.googleusercontent.com'
        CLIENT_SECRET = 'fLOZ4Po28pAUB1wYA_WbsZql'
        SCOPE = 'https://www.google.com/m8/feeds/'
        USER_AGENT = 'Scarlett-AI'

        auth_token = gdata.gauth.OAuth2Token(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, scope=SCOPE, user_agent=USER_AGENT)

        APPLICATION_REDIRECT_URI = 'http://localhost/oauth2callback'
        authorize_url = auth_token.generate_authorize_url(redirect_uri=APPLICATION_REDIRECT_URI)

        print(authorize_url)

        driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver")
        driver.get(authorize_url)
        import time

        WebDriverWait(driver, 5).until(lambda driver: driver.find_element(By.ID, "identifierId"))
        username = driver.find_element_by_id("identifierId")
        username.send_keys("d.kanhar")

        WebDriverWait(driver, 5).until(lambda driver: driver.find_element(By.ID, "identifierNext"))
        driver.find_element_by_id("identifierNext").click()
        # time.sleep(10)

        try:
            WebDriverWait(driver, 5).until(lambda driver: driver.find_element(By.ID, "skipChallenge"))
            driver.find_element_by_id("skipChallenge").click()

            try:
                WebDriverWait(driver, 5).until(lambda driver: driver.find_element(By.ID, "password"))
                password = driver.find_element_by_name("password")
                password.send_keys("2NINitu!1")

                WebDriverWait(driver, 5).until(lambda driver: driver.find_element(By.ID, "passwordNext"))
                driver.find_element_by_id("passwordNext").click()

            except:
                WebDriverWait(driver, 5).until(lambda driver: driver.find_element(By.LINK_TEXT, "Enter your password"))
                driver.find_element_by_link_text("Enter your password").click()

                WebDriverWait(driver, 5).until(lambda driver: driver.find_element(By.ID, "password"))
                password = driver.find_element_by_name("password")
                password.send_keys("2NINitu!1")

                WebDriverWait(driver, 5).until(lambda driver: driver.find_element(By.ID, "passwordNext"))
                driver.find_element_by_id("passwordNext").click()
        except:
            WebDriverWait(driver, 5).until(lambda driver: driver.find_element(By.ID, "password"))
            password = driver.find_element_by_name("password")
            password.send_keys("2NINitu!1")

            WebDriverWait(driver, 5).until(lambda driver: driver.find_element(By.ID, "passwordNext"))
            driver.find_element_by_id("passwordNext").click()
        # time.sleep(10)

        WebDriverWait(driver, 5).until(lambda driver: driver.find_element(By.ID, "submit_approve_access"))
        driver.find_element_by_id("submit_approve_access").click()

        time.sleep(5)

        current_url = driver.current_url
        # print(current_url)
        import atom.http_core
        redirect_url = current_url
        url = atom.http_core.ParseUri(redirect_url)
        token = auth_token.get_access_token(url.query)
        # print(token)
        # print(auth_token)
        print(driver.current_url)

        import gdata.contacts.client

        client = gdata.contacts.client.ContactsClient(source='Scarlett-AI')
        query = gdata.contacts.client.ContactsQuery(max_results=10000)
        auth_token.authorize(client)
        feed = client.GetContacts(q=query)
        print(feed)
        # print(feed[0])

        from contactsFeedParser import googleContactsFeedParser
        parser = googleContactsFeedParser()
        print(100*"-")
        parser.parse_(message=feed)

        driver.quit()

        pass

    # t3()

import gdata.gauth
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import atom.http_core
import gdata.contacts.client
from contactsFeedParser import googleContactsFeedParser
import time


class FetchContacts(object):
    def __init__(self):
        self.CLIENT_ID = '428607628598-dd19u5f3ma4rssk8sbm1ccjsbe3pq1ip.apps.googleusercontent.com'
        self.CLIENT_SECRET = 'fLOZ4Po28pAUB1wYA_WbsZql'
        self.SCOPE = 'https://www.google.com/m8/feeds/'
        self.USER_AGENT = 'Scarlett-AI'
        self.APPLICATION_REDIRECT_URI = 'http://localhost/oauth2callback'

        self.path_to_gcekodriver = "/usr/local/bin/chromedriver"

        self.username = "d.kanhar"
        self.password = "2NINitu!1"

        self.num_contacts = 10000
        self.sleep_time = 5

        pass

    def fetch_(self):

        contacts = self.__driver()

        return contacts

    def __driver(self):

        self.auth_token = self.__authenticate_()
        self.__retry_browser()
        time.sleep(self.sleep_time)
        self.token = self.__parse_url()
        self.contactsFeed = self.__fetch_contacts()
        contacts = self.__parse_contacts()

        self.driver.quit()

        return contacts

    def __authenticate_(self):
        auth_token = gdata.gauth.OAuth2Token(client_id=self.CLIENT_ID, client_secret=self.CLIENT_SECRET,
                                             scope=self.SCOPE, user_agent=self.USER_AGENT)

        authorize_url = auth_token.generate_authorize_url(redirect_uri=self.APPLICATION_REDIRECT_URI)

        self.authorizw_url = authorize_url

        self.driver = self.__open_browser()
        self.driver.get(authorize_url)

        return auth_token

    def __open_browser(self):
        driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver")
        return driver

    def __fetch_contacts(self):
        client = gdata.contacts.client.ContactsClient(source=self.USER_AGENT)
        query = gdata.contacts.client.ContactsQuery(max_results=self.num_contacts)
        self.auth_token.authorize(client)
        feed = client.GetContacts(q=query)
        return feed

    def __parse_contacts(self):

        parser = googleContactsFeedParser()
        parser.parse_(message=self.contactsFeed)
        contacts = parser.get_()

        return contacts

    def __retry_browser(self):
        # Currently expecting that the browser successfully authenticates itself in 2nd run, which might not be case.
        # We need to automate this till actually the run is succesfull.
        ret = False
        while True:
            try:
                ret = self.__authorize_from_browser()
            except:
                self.driver.quit()
                self.driver = self.__open_browser()
                self.driver.get(self.authorizw_url)

                ret = self.__authorize_from_browser()

            if ret:
                break
            else:
                continue

        return ret

    def __parse_url(self):
        current_url = self.driver.current_url

        redirect_url = current_url
        url = atom.http_core.ParseUri(redirect_url)
        token = self.auth_token.get_access_token(url.query)

        return token

    def __authorize_from_browser(self):
        WebDriverWait(self.driver, 5).until(lambda driver: driver.find_element(By.ID, "identifierId"))
        username = self.driver.find_element_by_id("identifierId")
        username.send_keys(self.username)

        WebDriverWait(self.driver, 5).until(lambda driver: driver.find_element(By.ID, "identifierNext"))
        self.driver.find_element_by_id("identifierNext").click()

        try:
            WebDriverWait(self.driver, 5).until(lambda driver: driver.find_element(By.ID, "skipChallenge"))
            self.driver.find_element_by_id("skipChallenge").click()

            try:
                WebDriverWait(self.driver, 5).until(lambda driver: driver.find_element(By.ID, "password"))
                password = self.driver.find_element_by_name("password")
                password.send_keys(self.password)

                WebDriverWait(self.driver, 5).until(lambda driver: driver.find_element(By.ID, "passwordNext"))
                self.driver.find_element_by_id("passwordNext").click()

            except:
                WebDriverWait(self.driver, 5).until(lambda driver: driver.find_element(By.LINK_TEXT, "Enter your password"))
                ret = self.driver.find_element_by_link_text("Enter your password").click()
                print(ret)

                WebDriverWait(self.driver, 5).until(lambda driver: driver.find_element(By.ID, "password"))
                password = self.driver.find_element_by_name("password")
                password.send_keys(self.password)

                WebDriverWait(self.driver, 5).until(lambda driver: driver.find_element(By.ID, "passwordNext"))
                self.driver.find_element_by_id("passwordNext").click()
        except:
            WebDriverWait(self.driver, 5).until(lambda driver: driver.find_element(By.ID, "password"))
            password = self.driver.find_element_by_name("password")
            password.send_keys(self.password)

            WebDriverWait(self.driver, 5).until(lambda driver: driver.find_element(By.ID, "passwordNext"))
            self.driver.find_element_by_id("passwordNext").click()

        WebDriverWait(self.driver, 5).until(lambda driver: driver.find_element(By.ID, "submit_approve_access"))
        self.driver.find_element_by_id("submit_approve_access").click()
        return True


if __name__ == '__main__':
    obj = FetchContacts()
    contacts = obj.fetch_()
    print(contacts)
