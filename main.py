from __future__ import print_function
import httplib2
import os
import json

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from get_credentials import get_credentials               #link get_credential.py


#Parse input args, if any
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


#Constants
GDOC_MIMETYPE = 'application/vnd.google-apps.document'
GSHEET_MIMETYPE = 'application/vnd.google-apps.spreadsheet'
GSLIDE_MIMETYPE = 'application/vnd.google-apps.presentation'


#Setup an authenticated http and GDrive REST API object
http = get_credentials().authorize(httplib2.Http())
service = discovery.build('drive', 'v3', http=http)


def main():

    """
    #docrevtest
    REQUEST_FILEID = '1aB1CFZ_KRdwabWIctMLqoimG3Fn1dnuBelKanLNjfP8'     
    EXPORT_FORMAT = 'docx'
    """

    """
    #sheetrevtest
    REQUEST_FILEID = '1S5vUsWEmnV-uLb7-7m-jOdcBxAKo_834us9x56s7xnw'     
    EXPORT_FORMAT = 'xlsx'
    """

    """
    #sliderevtest
    REQUEST_FILEID = '1_f_abGgeI4CruG72Yjjicrce9rk0NRcc4_4vYjd5JNQ'     
    EXPORT_FORMAT = 'pptx'
    #https://docs.google.com/presentation/u/0/d/1_f_abGgeI4CruG72Yjjicrce9rk0NRcc4_4vYjd5JNQ/export?format=pptx&revision=1
    """

    #User file in google drive
    REQUEST_FILEID = '1tG6oBCtgMfqrXa34Rk1HWrudLMzEjZ84'
    EXPORT_FORMAT = 'png'


    fileInfo = service.files().get(
        fileId = REQUEST_FILEID
        ).execute()

    #Determine what type of file this is
    fileMimeType = fileInfo['mimeType']
    if fileMimeType == GDOC_MIMETYPE:
        DOCTYPE = 'document'
    elif fileMimeType == GSHEET_MIMETYPE:
        DOCTYPE = 'spreadsheets'
    elif fileMimeType == GSLIDE_MIMETYPE:
        DOCTYPE = 'presentation'
    else:
        DOCTYPE = ''
    
    #Create a folder with the file's name as its download destination
    fileName = fileInfo['name']
    fileDLPath = os.path.join(os.getcwd(), fileName)
    if not os.path.exists(fileDLPath):
        os.makedirs(fileDLPath)

    print('Downloading all revisions of \"{}\"'.format(fileName))

    #Begin downloading all revisions
    hasAllRevisions = False
    result_nextPageToken = ''

    while not hasAllRevisions:

        #Call the Revision.List function to get a list of all revisions for the file
        #results is a dict containing the return fields specified in the API documentations
        if result_nextPageToken is '':
            revResponse = service.revisions().list(
                fileId = REQUEST_FILEID,
                pageSize = 2
                ).execute() 
        else:
             revResponse = service.revisions().list(
                fileId = REQUEST_FILEID,
                pageSize = 2,
                pageToken = result_nextPageToken
                ).execute()
        #print(json.dumps(results, sort_keys=True, indent=4))
        
        for rev in revResponse['revisions']:
            print(rev['id'], rev['modifiedTime'])

            #Generic user file
            if DOCTYPE is '':
                pass
            
            #Google Docs related files
            else:
                dl_url = 'https://docs.google.com/{}/u/0/d/{}/export?format={}&revision={}'.format(DOCTYPE, REQUEST_FILEID , EXPORT_FORMAT, rev['id']) 
                dl_response, dl_content = http.request(dl_url)
                print(dl_response.status)

                output_path = '{}\{}.{}'.format(fileDLPath, rev['id'], EXPORT_FORMAT)
                with open(output_path, 'wb') as f:
                    f.write(dl_content)

        #Prepare for the next iteration, if there are still revision pages remaining to fetch
        if not 'nextPageToken' in revResponse:
            hasAllRevisions = True
        else:
            result_nextPageToken = revResponse['nextPageToken']


if __name__ == '__main__':
    main()