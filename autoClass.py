print("""
~\_['.']_/~ Consider it done!
""")
from urlextract import URLExtract
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from selenium import webdriver
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from datetime import datetime

chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("--no-sandbox")
chromeOptions.add_argument("--disable-setuid-sandbox")
chromeOptions.add_argument("--remote-debugging-port=9222")
chromeOptions.add_argument("--disable-notifications")
chromeOptions.add_argument("--use-fake-device-for-media-stream")
chromeOptions.add_argument("--use-fake-ui-for-media-stream")
#chromeOptions.add_experimental_option('prefs',{'profile.default_content_setting_values.media_stream_mic':1})

SCOPES = ['https://www.googleapis.com/auth/classroom.announcements.readonly']

creds = None

if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)

    with open('token.json', 'w') as token:
        token.write(creds.to_json())

service = build('classroom', 'v1', credentials=creds)
lastClassId = None


def firstTime():

    global lastClassId
    results = service.courses().announcements().list(courseId=316240260843).execute()
    extractor = URLExtract()
    #print(results)
    for element in results['announcements']:
        urls = extractor.find_urls(element['text'])
        for url in urls:
            if url.find("meet.google") != -1:
                print( "\n\n" + element['text'] + "\n" + element['id'] + "\n\n")
                print("The last class was: " + url+"\n")
                lastClassId = element['id']
                break
        else:
            continue
        break


def recheck():

    global lastClassId
    results = service.courses().announcements().list(courseId=316240260843).execute()
    extractor = URLExtract()
    for element in results['announcements']:
        urls = extractor.find_urls(element['text'])
        for url in urls:
            if url.find("meet.google") != -1:
                if element['id'] == lastClassId:
                    print("Found new class with meeting link:"+url+" with id:"+element['id'])
                    print("\n\n" + element['text'] + "\n" + element['id'] + "\n\n")
                    meet(url)
                else:
                    print("No new class as of now. Retrying in 3 minutes.")
                break
        else:
            continue
        break


def meet(link):
    print("Joining meet room...")
    driver = webdriver.Chrome('../../../../../../home/arag/PycharmProjects/AutoClass/chromedriver', options=chromeOptions)
    driver.get("https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount?redirect_uri=https%3A%2F%2Fdevelopers.google.com%2Foauthplayground&prompt=consent&response_type=code&client_id=407408718192.apps.googleusercontent.com&scope=email&access_type=offline&flowName=GeneralOAuthFlow")
    driver.find_element_by_xpath('//*[@id="identifierId"]').send_keys("ashutosh.29957@ges.edu.in")
    driver.find_element_by_xpath('//*[@id="identifierNext"]/div/button/div[2]').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input').send_keys("IXdByGes09")
    driver.find_element_by_xpath('//*[@id="passwordNext"]/div/button/div[2]').click()
    #driver.find_element_by_xpath('//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div/div/ul/li[1]/div').click()
    time.sleep(5)
    driver.get(link)
    time.sleep(5)
    #driver.find_element_by_xpath('//*[@id="yDmH0d"]/div[3]/div/div[2]/div[3]/div/span').click()
    #time.sleep(3)
    driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[9]/div[3]/div/div/div[2]/div/div[1]/div[1]/div[1]/div/div[4]/div[1]/div/div/div/span').click()
    driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[9]/div[3]/div/div/div[2]/div/div[1]/div[1]/div[1]/div/div[4]/div[2]/div/div').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[9]/div[3]/div/div/div[2]/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/span/span').click()
    #to be continued
    print("Meet room Joined, will be closed after 50 minutes.")
    #wait until class gets over
    time.sleep(60*50)
    driver.quit()
    print("Meet room closed.")
firstTime()

while 1>0:

    print("\nRechecking...")
    recheck()
    time.sleep(180)