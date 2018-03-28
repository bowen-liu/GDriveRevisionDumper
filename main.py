from __future__ import print_function
import argparse
import httplib2
import os
import json

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from get_credentials import get_credentials                 #link get_credential.py
from constants import *                                     #link constants.py


#Parse input args
parser = argparse.ArgumentParser(description='Downloads all individual revisions for a file on Google Drive.')

parser.add_argument('fileID', help='ID of the file to be downloaded') 
parser.add_argument('--format', 
    help='File Format when exporting files created from Google Docs. This argument will be ignored when exporting regular files from Google Drive.\n \
    Available Export Formats for Google Docs: rtf, odt, html, epub, docx, pdf, zip, txt.\n \
    For Google Sheets: ods, tsv, xlsx, csv, pdf, zip, txt.\n \
    For Google Slides: odp, pptx, pdf. \n \
    For Google Drawing: svg, png, jpeg, pdf. \n')

args = parser.parse_args()



#Setup an authenticated http and GDrive REST API object
http = get_credentials().authorize(httplib2.Http())
service = discovery.build('drive', 'v2', http=http)


def main():


    #docrevtest
    #python main.py 1aB1CFZ_KRdwabWIctMLqoimG3Fn1dnuBelKanLNjfP8 --format docx

    #sheetrevtest
    #python main.py 1S5vUsWEmnV-uLb7-7m-jOdcBxAKo_834us9x56s7xnw --format xlsx 

    #sliderevtest
    #python main.py 1_f_abGgeI4CruG72Yjjicrce9rk0NRcc4_4vYjd5JNQ --format pptx    

    #User file in google drive
    #python main.py 1tG6oBCtgMfqrXa34Rk1HWrudLMzEjZ84

    
    #Retreive the associated file's metadata from the fileId
    fileInfo = service.files().get(
        fileId = args.fileID
        ).execute()
    fileName = fileInfo['title']
    fileMimeType = fileInfo['mimeType']


    #Determine what type of file this is
    if fileMimeType == GDOC_MIMETYPE:
        print('Identified \"{}\" as a Google Docs file'.format(fileName))
        
        if not args.format:
            print('Error: You must specify --format in order to export this file!')
            return
        if not args.format in GDOC_EXPORT_FORMATS:
            print('Invalid export format \"{}\" for Google Docs.'.format(args.format))
            print('Available Export Formats for Google Docs: rtf, odt, html, epub, docx, pdf, zip, txt')
            return
        
        export_format = GDOC_EXPORT_FORMATS[args.format]
        export_extension = args.format
        
    elif fileMimeType == GSHEET_MIMETYPE:
        print('Identified \"{}\" as a Google Docs file'.format(fileName))
        
        if not args.format:
            print('Error: You must specify --format in order to export this file!')
            return

        if not args.format in GSHEET_EXPORT_FORMATS:
            print('Invalid export format \"{}\" for Google Sheets.'.format(args.format))
            print('Available Export Formats for Google Sheets: ods, tsv, xlsx, csv, pdf, zip, txt')
            return
        
        export_format = GSHEET_EXPORT_FORMATS[args.format]
        export_extension = args.format

    elif fileMimeType == GSLIDE_MIMETYPE:
        print('Identified \"{}\" as a Google Slides file'.format(fileName))
        
        if not args.format:
            print('Error: You must specify --format in order to export this file!')
            return
        if not args.format in GSLIDE_EXPORT_FORMATS:
            print('Invalid export format \"{}\" for Google Slides.'.format(args.format))
            print('Available Export Formats for Google Slides: odp, pptx, pdf')
            return
        
        export_format = GSLIDE_EXPORT_FORMATS[args.format]
        export_extension = args.format

    elif fileMimeType == GDRAWING_MIMETYPE:
        print('Identified \"{}\" as a Google Drawing file'.format(fileName))
        
        if not args.format:
            print('Error: You must specify --format in order to export this file!')
            return
        if not args.format in GDRAWING_EXPORT_FORMATS:
            print('Invalid export format \"{}\" for Google Drawing.'.format(args.format))
            print('Available Export Formats for Google Drawing: svg, png, jpeg, pdf')
            return
        
        export_format = GDRAWING_EXPORT_FORMATS[args.format]
        export_extension = args.format

    else:
        print('Identified \"{}\" as a regular file'.format(fileName))
        export_extension = fileName.split('.')[1]



    #Create a folder with the file's name as its download destination
    fileDLPath = os.path.join(os.getcwd(), fileName)
    if not os.path.exists(fileDLPath):
        os.makedirs(fileDLPath) 
    
    print('Downloading all revisions of \"{}\"...\n'.format(fileName))

    #Begin downloading all revisions
    hasAllRevisions = False
    result_pageToken = ''

    while not hasAllRevisions:

        #Get a list of all revisions for the file         #https://developers.google.com/drive/v2/reference/revisions/list
        if result_pageToken is '':
            revResponse = service.revisions().list(
                fileId = args.fileID,
                maxResults = 2
                ).execute() 
        else:
             revResponse = service.revisions().list(
                fileId = args.fileID,
                maxResults = 2,
                pageToken = result_pageToken
                ).execute()
        #print(json.dumps(results, sort_keys=True, indent=4))
        
        #Download each revision in the current list
        for rev in revResponse['items']:
            print(rev['id'], rev['modifiedDate'])

            if not 'downloadUrl' in rev:                                                     #file is from google doc
                dl_url = rev['exportLinks'][export_format]               
            else:                                                                            #any other files in google drive
                dl_url = rev['downloadUrl']                         

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