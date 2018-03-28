from __future__ import print_function
import httplib2
import os
import json

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    #home_dir = os.path.expanduser('~')
    home_dir = os.getcwd()
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials



def main():

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)


    FILEID = '1aB1CFZ_KRdwabWIctMLqoimG3Fn1dnuBelKanLNjfP8'
    PAGESIZE = 2

    has_all_revisions = False
    result_nextPageToken = ''

    while not has_all_revisions:

        #Call the Revision.List function to get a list of all revisions for the file
        #results is a dict containing the return fields specified in the API documentations
        if result_nextPageToken is '':
            results = service.revisions().list(
                fileId = FILEID,
                pageSize = PAGESIZE
                ).execute() 
        else:
             results = service.revisions().list(
                fileId = FILEID,
                pageSize = PAGESIZE,
                pageToken = result_nextPageToken
                ).execute()
        #print(json.dumps(results, sort_keys=True, indent=4))
        
        for rev in results['revisions']:
            print(rev['id'], rev['modifiedTime'])

            dl_url = 'https://docs.google.com/document/u/0/d/{}/export?format=docx&revision={}'.format(FILEID ,rev['id']) 
            dl_response, dl_content = http.request(dl_url)
            print(dl_response.status)


            output_fname = rev['id'] + '.docx'
            with open(output_fname, 'wb') as f:
                f.write(dl_content)

        #Prepare for the next iteration, if there are still revision pages remaining to fetch
        if not 'nextPageToken' in results:
            has_all_revisions = True
        else:
            result_nextPageToken = results['nextPageToken']


if __name__ == '__main__':
    main()