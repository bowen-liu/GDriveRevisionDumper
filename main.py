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
service = discovery.build('drive', 'v2', http=http)


def main():


    #docrevtest
    #REQUEST_FILEID = '1aB1CFZ_KRdwabWIctMLqoimG3Fn1dnuBelKanLNjfP8'     

    #sheetrevtest
    #REQUEST_FILEID = '1S5vUsWEmnV-uLb7-7m-jOdcBxAKo_834us9x56s7xnw'     

    #sliderevtest
    #REQUEST_FILEID = '1_f_abGgeI4CruG72Yjjicrce9rk0NRcc4_4vYjd5JNQ'     

    #User file in google drive
    REQUEST_FILEID = '1tG6oBCtgMfqrXa34Rk1HWrudLMzEjZ84'

    fileInfo = service.files().get(
        fileId = REQUEST_FILEID
        ).execute()

    #Determine what type of file this is
    fileMimeType = fileInfo['mimeType']
    if fileMimeType == GDOC_MIMETYPE:
        export_extension = 'docx'
        export_format = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    elif fileMimeType == GSHEET_MIMETYPE:
        export_extension = 'xlsx'
        export_format = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    elif fileMimeType == GSLIDE_MIMETYPE:
        export_extension = 'pptx'
        export_format = 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
    else:
        export_extension = 'png'        #temporary
        export_format = ''
    
    #Create a folder with the file's name as its download destination
    fileName = fileInfo['title']
    fileDLPath = os.path.join(os.getcwd(), fileName)
    if not os.path.exists(fileDLPath):
        os.makedirs(fileDLPath)

    print('Downloading all revisions of \"{}\"'.format(fileName))

    #Begin downloading all revisions
    hasAllRevisions = False
    result_pageToken = ''

    while not hasAllRevisions:

        #Call the Revision.List function to get a list of all revisions for the file
        #results is a dict containing the return fields specified in the API documentations
        #https://developers.google.com/drive/v2/reference/revisions/list
        if result_pageToken is '':
            revResponse = service.revisions().list(
                fileId = REQUEST_FILEID,
                maxResults = 2
                ).execute() 
        else:
             revResponse = service.revisions().list(
                fileId = REQUEST_FILEID,
                maxResults = 2,
                pageToken = result_pageToken
                ).execute()
        #print(json.dumps(results, sort_keys=True, indent=4))
        
        for rev in revResponse['items']:
            print(rev['id'], rev['modifiedDate'])

            if not 'downloadUrl' in rev:
                dl_url = rev['exportLinks'][export_format]          #file is from google doc 
            else:
                dl_url = rev['downloadUrl']                         #any other files in google drive

            dl_response, dl_content = http.request(dl_url)
            print(dl_response.status)

            output_path = '{}\{}.{}'.format(fileDLPath, rev['id'], export_extension)
            with open(output_path, 'wb') as f:
                f.write(dl_content) 

        #Prepare for the next iteration, if there are still revision pages remaining to fetch
        if not 'nextPageToken' in revResponse:
            hasAllRevisions = True
        else:
            result_pageToken = revResponse['nextPageToken']


if __name__ == '__main__':
    main()