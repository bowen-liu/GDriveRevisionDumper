from __future__ import print_function
import argparse
import httplib2
import os
import json
from apiclient import discovery


from constants import *                                     #link constants.py


#Test cases:
#docrevtest
#python main.py 1aB1CFZ_KRdwabWIctMLqoimG3Fn1dnuBelKanLNjfP8 --format docx

#sheetrevtest
#python main.py 1S5vUsWEmnV-uLb7-7m-jOdcBxAKo_834us9x56s7xnw --format xlsx 

#sliderevtest
#python main.py 1_f_abGgeI4CruG72Yjjicrce9rk0NRcc4_4vYjd5JNQ --format pptx    

#User file in google drive
#python main.py 1tG6oBCtgMfqrXa34Rk1HWrudLMzEjZ84



#########################################################
#          Initialization and Authentication
#########################################################

def get_input_args():
    parser = argparse.ArgumentParser(description='Downloads all individual revisions for a file on Google Drive.')

    parser.add_argument('fileID', help='ID of the file to be downloaded') 
    parser.add_argument('--format', 
        help='File Format when exporting files created from Google Docs. This argument will be ignored when exporting regular files from Google Drive.\n \
        Available Export Formats for Google Docs: rtf, odt, html, epub, docx, pdf, zip, txt.\n \
        For Google Sheets: ods, tsv, xlsx, csv, pdf, zip, txt.\n \
        For Google Slides: odp, pptx, pdf. \n \
        For Google Drawing: svg, png, jpeg, pdf. \n')
    
    return parser.parse_args()

def get_credentials():

    from oauth2client import client
    from oauth2client import tools
    from oauth2client.file import Storage
    
    # If modifying these scopes, delete your previously saved credentials
    # at ~/.credentials/drive-python-quickstart.json
    SCOPES = 'https://www.googleapis.com/auth/drive.readonly'
    CLIENT_SECRET_FILE = 'client_secret.json'
    APPLICATION_NAME = 'GDriveRevisionDumper'

    flags=tools.argparser.parse_args(args=[])   #mimics no args specified

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
        
        credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
   
    return credentials

args = get_input_args()
http = get_credentials().authorize(httplib2.Http())     #Setup an authenticated http and GDrive service object
service = discovery.build('drive', 'v2', http=http)


#########################################################
#          Helper Functions for the main script
#########################################################

def identify_filetype(fileMimeType, fileName):

    if fileMimeType == GDOC_MIMETYPE:
        print('Identified \"{}\" as a Google Docs file'.format(fileName))
        
        if not args.format:
            args.format = GDOC_DEFAULT_FORMAT
            print('Exporting as .' +GDOC_DEFAULT_FORMAT +" (default)")

        elif not args.format in GDOC_EXPORT_FORMATS:
            print('Invalid export format \"{}\" for Google Docs.'.format(args.format))
            print('Available Export Formats for Google Docs: rtf, odt, html, epub, docx, pdf, zip, txt')
            return 

        exportFormat = GDOC_EXPORT_FORMATS[args.format]
        exportExtension = args.format
        
    elif fileMimeType == GSHEET_MIMETYPE:
        print('Identified \"{}\" as a Google Docs file'.format(fileName))
        
        if not args.format:
            args.format = GSHEET_DEFAULT_FORMAT
            print('Exporting as .' +GSHEET_DEFAULT_FORMAT +" (default)")

        elif not args.format in GSHEET_EXPORT_FORMATS:
            print('Invalid export format \"{}\" for Google Sheets.'.format(args.format))
            print('Available Export Formats for Google Sheets: ods, tsv, xlsx, csv, pdf, zip, txt')
            return
        
        exportFormat = GSHEET_EXPORT_FORMATS[args.format]
        exportExtension = args.format

    elif fileMimeType == GSLIDE_MIMETYPE:
        print('Identified \"{}\" as a Google Slides file'.format(fileName))
        
        if not args.format:
            args.format = GSLIDE_DEFAULT_FORMAT
            print('Exporting as .' +GSLIDE_DEFAULT_FORMAT +" (default)")

        elif not args.format in GSLIDE_EXPORT_FORMATS:
            print('Invalid export format \"{}\" for Google Slides.'.format(args.format))
            print('Available Export Formats for Google Slides: odp, pptx, pdf')
            return
        
        exportFormat = GSLIDE_EXPORT_FORMATS[args.format]
        exportExtension = args.format

    elif fileMimeType == GDRAWING_MIMETYPE:
        print('Identified \"{}\" as a Google Drawing file'.format(fileName))
        
        if not args.format:
            args.format = GDRAWING_DEFAULT_FORMAT
            print('Exporting as .' +GDRAWING_DEFAULT_FORMAT +" (default)")

        elif not args.format in GDRAWING_EXPORT_FORMATS:
            print('Invalid export format \"{}\" for Google Drawing.'.format(args.format))
            print('Available Export Formats for Google Drawing: svg, png, jpeg, pdf')
            return
        
        exportFormat = GDRAWING_EXPORT_FORMATS[args.format]
        exportExtension = args.format

    else:
        print('Identified \"{}\" as a regular file'.format(fileName))
        exportExtension = fileName.split('.')[1]
        exportFormat = exportExtension

    return exportFormat, exportExtension



#########################################################
#                     Main Script
#########################################################

def main():
    
    #Retreive the associated file's metadata from the fileId
    fileInfo = service.files().get(
        fileId = args.fileID
        ).execute()
    fileName = fileInfo['title']
    fileMimeType = fileInfo['mimeType']


    #Determine what type of file this is
    exportFormat, exportExtension = identify_filetype(fileMimeType, fileName)

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
                dlUrl = rev['exportLinks'][exportFormat]               
            else:                                                                            #any other files in google drive
                dlUrl = rev['downloadUrl']                         

            dlResponse, dlContent = http.request(dlUrl)
            print(dlResponse.status)

            output_path = '{}\{}.{}'.format(fileDLPath, rev['id'], exportExtension)
            with open(output_path, 'wb') as f:
                f.write(dlContent) 

        #Prepare for the next iteration, if there are still revision pages remaining to fetch
        if not 'nextPageToken' in revResponse:
            hasAllRevisions = True
        else:
            result_pageToken = revResponse['nextPageToken']



if __name__ == '__main__':
    main()