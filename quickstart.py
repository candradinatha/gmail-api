from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

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
    results = service.users().messages().list(userId=user_id, labelIds=[label_id_one, label_id_two]).execute()

    # print ('Message snippet: %s' % results['messages'])

    msglist = results['messages']

    print("Total unread messages in inbox: ", str(len(msglist)))

    for mssg in msglist:
        m_id = mssg['id']
        message = service.users().messages().get(userId=user_id, id=m_id).execute()

        try:
            print('Message snippet: %s' % message['snippet'])
        except:
            pass

if __name__ == '__main__':
    main()