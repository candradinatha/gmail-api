from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import base64
from gtts import gTTS
import pygame
import vlc
import time

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))

    user_id = 'me'
    label_id_one = 'INBOX'
    label_id_two = 'UNREAD'

    # Call the Gmail API
    results = service.users().messages().list(userId=user_id, labelIds=[label_id_one], maxResults=1).execute()

    msglist = results['messages']

    # print("Total unread messages in inbox: ", str(len(msglist)))


    for mssg in msglist:
        m_id = mssg['id']
        message = service.users().messages().get(userId=user_id, id=m_id).execute()
        print('Message snippet: %s' % message['snippet'])
        payLd = message['payload']

        mssg_parts = payLd['parts']
        part_one = mssg_parts[0]
        part_body = part_one['body']
        part_data = part_body['data']

        clean_one = part_data.replace("-", "+")  # decoding from Base64 to UTF-8
        clean_one = clean_one.replace("_", "/")  # decoding from Base64 to UTF-8
        clean_two = base64.b64decode(bytes(clean_one, 'UTF-8'))  # decoding from Base64 to UTF-8

        msg = str(clean_two)

        print('Message snippet: %s' % msg)

        tts = gTTS(msg)
        tts.save('message.mp3')
        pygame.mixer.init()
        pygame.mixer.music.load("message.mp3")
        pygame.mixer.music.play()
        time.sleep(40)

        # try:
        #     print('Message snippet: %s' % message['snippet'])
        #     # tts = gTTS(message['snippet'])
        #     # tts.save('hello.mp3')
        #     # pygame.mixer.init()
        #     # pygame.mixer.music.load("hello.mp3")
        #     # pygame.mixer.music.play()
        #     # time.sleep(20)
        #
        # except:
        #     pass


if __name__ == '__main__':
    main()