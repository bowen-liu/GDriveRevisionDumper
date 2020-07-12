from __future__ import print_function

from constants import *             #link constants.py

import argparse
import os
import httplib2
import json
import sys

from datetime import datetime
from apiclient import errors
from apiclient import discovery
from googleapiclient.http import MediaIoBaseDownload



#########################################################
#          Initialization and Authentication
#########################################################

def get_input_args():
    parser = argparse.ArgumentParser(description='Downloads all individual revisions for a file on Google Drive.')

    parser.add_argument('operation', choices=["revdump", "download"],
        help='Operation to be performed by the script.\n\
        ')

    parser.add_argument('file_id',
        help='ID of the file to be downloaded')

    parser.add_argument('-i', '--import-bypass', default=False, action='store_true',
        help='Bypass a file\'s download limit by temporarily importing it to your own drive first.')

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
    # at .credentials/drive-python-quickstart.json
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly', 'https://www.googleapis.com/auth/drive.file']

    flags=tools.argparser.parse_args(args=[])   #mimics no args specified

    home_dir = os.getcwd()
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'client_credentials.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        try:
            flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        except:
            print('\n*******************************************************\n')
            print('ERROR: \"client_secret.json\" was not found or invalid.')
            print('A valid Google Drive API key is needed to continue.')
            print('\n*******************************************************\n')
            print(MISSING_API_KEY_TUT)
            print('\n')
            exit()

        flow.user_agent = 'GDriveRevisionDumper'

        credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)

    return credentials




#########################################################
#          Helper Functions for the main script
#########################################################

def identify_filetype(fileMimeType, fileName, args_format):

    if fileMimeType == GDOC_MIMETYPE:
        print('Identified \"{}\" as a Google Docs file'.format(fileName))

        if not args_format:
            args_format = GDOC_DEFAULT_FORMAT
            print('Exporting as .' +GDOC_DEFAULT_FORMAT +" (default)")

        elif not args_format in GDOC_EXPORT_FORMATS:
            print('Invalid export format \"{}\" for Google Docs.'.format(args_format))
            print('Available Export Formats for Google Docs: rtf, odt, html, epub, docx, pdf, zip, txt')
            return

        exportFormat = GDOC_EXPORT_FORMATS[args_format]
        exportExtension = args_format

    elif fileMimeType == GSHEET_MIMETYPE:
        print('Identified \"{}\" as a Google Docs file'.format(fileName))

        if not args_format:
            args_format = GSHEET_DEFAULT_FORMAT
            print('Exporting as .' +GSHEET_DEFAULT_FORMAT +" (default)")

        elif not args_format in GSHEET_EXPORT_FORMATS:
            print('Invalid export format \"{}\" for Google Sheets.'.format(args_format))
            print('Available Export Formats for Google Sheets: ods, tsv, xlsx, csv, pdf, zip, txt')
            return

        exportFormat = GSHEET_EXPORT_FORMATS[args_format]
        exportExtension = args_format

    elif fileMimeType == GSLIDE_MIMETYPE:
        print('Identified \"{}\" as a Google Slides file'.format(fileName))

        if not args_format:
            args_format = GSLIDE_DEFAULT_FORMAT
            print('Exporting as .' +GSLIDE_DEFAULT_FORMAT +" (default)")

        elif not args_format in GSLIDE_EXPORT_FORMATS:
            print('Invalid export format \"{}\" for Google Slides.'.format(args_format))
            print('Available Export Formats for Google Slides: odp, pptx, pdf')
            return

        exportFormat = GSLIDE_EXPORT_FORMATS[args_format]
        exportExtension = args_format

    elif fileMimeType == GDRAWING_MIMETYPE:
        print('Identified \"{}\" as a Google Drawing file'.format(fileName))

        if not args_format:
            args_format = GDRAWING_DEFAULT_FORMAT
            print('Exporting as .' +GDRAWING_DEFAULT_FORMAT +" (default)")

        elif not args_format in GDRAWING_EXPORT_FORMATS:
            print('Invalid export format \"{}\" for Google Drawing.'.format(args_format))
            print('Available Export Formats for Google Drawing: svg, png, jpeg, pdf')
            return

        exportFormat = GDRAWING_EXPORT_FORMATS[args_format]
        exportExtension = args_format

    elif fileMimeType == GFOLDER_MIMETYPE:
        print('Identified \"{}\" as a folder'.format(fileName))
        exportExtension = ''
        exportFormat = ''

    else:
        print('Identified \"{}\" as a regular file ({})'.format(fileName, fileMimeType))
        filename_split = fileName.split('.')
        if (len(filename_split) <= 1):
            exportExtension = ''
        else:
            exportExtension = filename_split[-1]
        exportFormat = exportExtension

    return exportFormat, exportExtension


def download_file_by_url(url, out_fname, http):

    try:
        f = open(out_fname, 'wb')
    except:
        print("Failed to create file \"{}\" for writing! Reason: {}".format(out_fname, sys.exc_info()[0]))
        return

    print("Downloading file \"{}\"...".format(out_fname))

    try:
        http_response, http_content = http.request(url)
        #print('HTTP Response: ' +str(http_response.status))
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
        return

    f.write(http_content)
    f.close()

def download_file_by_id(file_id, out_fname, service):

    try:
        f = open(out_fname, 'wb')
    except:
        print("Failed to create file \"{}\" for writing! Reason: {}".format(out_fname, sys.exc_info()[0]))
        return

    request = service.files().get_media(fileId=file_id)
    media_request = MediaIoBaseDownload(f, request)

    while True:
        try:
            download_progress, done = media_request.next_chunk()
        except errors.HttpError as error:
            print('An error occurred: %s' % error)
            f.close()
            return False

        if download_progress:
            print(' Download Progress: %d%%' % int(download_progress.progress() * 100))
        if done:
            break

    f.close()
    return True



#########################################################
#                   Revision Dumper
#########################################################

#Test cases:
#docrevtest
#python main.py revdump 1aB1CFZ_KRdwabWIctMLqoimG3Fn1dnuBelKanLNjfP8 --format docx

#sheetrevtest
#python main.py revdump 1S5vUsWEmnV-uLb7-7m-jOdcBxAKo_834us9x56s7xnw --format xlsx

#sliderevtest
#python main.py revdump 1_f_abGgeI4CruG72Yjjicrce9rk0NRcc4_4vYjd5JNQ --format pptx

#User file in google drive
#python main.py revdump 1tG6oBCtgMfqrXa34Rk1HWrudLMzEjZ84

def rewrite_datestr(datestr):
    revdate = datetime.strptime(datestr, "%Y-%m-%dT%H:%M:%S.%fZ")
    revdate_str = '{}-{}-{} {}-{}-{}'.format(revdate.year, revdate.month, revdate.day, revdate.hour, revdate.minute, revdate.second)
    return revdate_str

def dump_revisions(params):

    exportFormat = params["exportFormat"]
    exportExtension = params["exportExtension"]
    fileDLPath = params["fileDLPath"]
    http = params["http"]
    service = params["service"]

    hasAllRevisions = False
    result_pageToken = ''

    if (params["is_folder"]):
        print("\'revdump\' cannot work on a folder! Exiting...")
        return

    while not hasAllRevisions:
        #Get a list of all revisions for the file
        #https://developers.google.com/drive/v2/reference/revisions/list
        if result_pageToken is '':
            revResponse = service.revisions().list(
                fileId = params["file_id"],
                maxResults = 1000
                ).execute()
        else:
            revResponse = service.revisions().list(
                fileId = params["file_id"],
                maxResults = 1000,
                pageToken = result_pageToken
                ).execute()
        #print(json.dumps(results, sort_keys=True, indent=4))

        #Download each revision in the current list. For faster downloads, consider parallelizing this loop
        for rev in revResponse['items']:
            print('Downloading revision ' +rev['id'] +', modified on ' +rev['modifiedDate'])
            if not 'downloadUrl' in rev:                    #file is from google doc
                url = rev['exportLinks'][exportFormat]
            else:                                           #any other files in google drive
                url = rev['downloadUrl']

            outputFilename = '{}\{} {}.{}'.format(fileDLPath, rev['id'], rewrite_datestr(rev['modifiedDate']), exportExtension)
            download_file_by_url(url, outputFilename, http)

        #Prepare for the next iteration, if there are still revision pages remaining to fetch
        if not 'nextPageToken' in revResponse:
            hasAllRevisions = True
        else:
            result_pageToken = revResponse['nextPageToken']



#########################################################
#                Recursive Downloader
#########################################################

#Test cases:
#recursive folder download
#python3 main.py download 1hD9vjVFT6QFjAW7EZnk8MX9W5cHplRZa

#single file download
#python3 main.py download 1Jpdo3XXaM6i661Zrcpz8PdmFOx6OAnyf

#import download
#python3 main.py download 1L7PN5ULXnOFaJU0pNE1Tt6LMNjxMTNsb

tmp_folder_fileid = None

#Recursively download a folder (DFS)
def recursive_downloader(file_id, dl_path, service, import_bypass=False, fileInfo=None):

    global tmp_folder_fileid
    page_token = None

    #if the import_bypass is enabled, create a temporary folder in the user's gdrive
    if import_bypass and tmp_folder_fileid == None:
        tmp_folder_name = "_tmp_gdrive_downloader"      #TODO: make this name dynamic

        tmp_folder = service.files().insert(body={
                'title': tmp_folder_name,
                'mimeType': GFOLDER_MIMETYPE
            }).execute()

        tmp_folder_fileid = tmp_folder['id']

    # Get the file_id's metadata if it wasn't passed in
    if not fileInfo:
        file_info = service.files().get(
            fileId = file_id
            ).execute()
    else:
        file_info = fileInfo

    # If file_id is a file, download it and return
    if (file_info['mimeType'] != GFOLDER_MIMETYPE):
        if import_bypass:
            #import_bypass: make a copy of the target file into your own drive first
            #todo: check if your drive have enough space first?
            imported_file = service.files().copy(
                fileId = file_id,
                body = {
                    'title': file_info['title'],
                    'parents': [{'id': tmp_folder_fileid}]
                }
            ).execute()

            file_id = imported_file['id']
            file_info = imported_file

        if (not os.path.exists(dl_path)):
            os.makedirs(dl_path)

        file_name = file_info['title']
        save_location = dl_path +"/" +file_name

        print("Downloading \"" +file_name +"\" (" +str(file_info['fileSize']) +" bytes)..."  )
        download_file_by_id(file_id, save_location, service)

        #delete the imported files (if enabled)
        if import_bypass:
            service.files().delete(
                fileId = file_id
            ).execute()
        return


    # if file_id is a folder, recurse into it
    while (True):
        try:
            children = service.children().list(
                folderId = file_id,
                pageToken = page_token
                ).execute()

        except errors.HttpError as error:
            print('An error occurred: %s' % error)
            break

        for child in children.get('items', []):
            child_file_id = child['id']

            #Retreive the current file/folders's metadata
            child_fileInfo = service.files().get(
                fileId = child_file_id
                ).execute()

            child_Name = child_fileInfo['title']
            child_MimeType = child_fileInfo['mimeType']

            #If we find a subdirectory, continue to recurse into it.
            #Otherwise, download any files we've encountered at this level.
            if (child_MimeType == GFOLDER_MIMETYPE):
                child_dl_path = dl_path + "/" + child_Name
                recursive_downloader(child_file_id, child_dl_path, service, fileInfo=child_fileInfo)
            else:
                recursive_downloader(child_file_id, dl_path, service, fileInfo=child_fileInfo)

        # Retrieve the next list of children, if any
        page_token = children.get('nextPageToken')
        if not page_token:
            break

    return

#########################################################
#                     Main Script
#########################################################

def main():

    args = get_input_args()
    http = get_credentials().authorize(httplib2.Http())     #Setup an authenticated http and GDrive service object
    service = discovery.build('drive', 'v2', http=http)

    #Retreive the associated file's metadata from the fileId
    fileInfo = service.files().get(
        fileId = args.file_id
        ).execute()
    fileName = fileInfo['title']
    fileMimeType = fileInfo['mimeType']

    #Determine what type of file this is
    exportFormat, exportExtension = identify_filetype(fileMimeType, fileName, args.format)
    is_folder = (fileMimeType == GFOLDER_MIMETYPE)

    #Create a folder with the file's name as its download destination
    fileDLPath = os.path.join(os.getcwd(), fileName)
    if (is_folder and not os.path.exists(fileDLPath)):
        os.makedirs(fileDLPath)

    params = {
        "file_id": args.file_id,
        "fileInfo" : fileInfo,
        "is_folder" : is_folder,
        "exportFormat" : exportFormat,
        "exportExtension" : exportExtension,
        "fileDLPath" : fileDLPath,
        "http" : http,
        "service" : service,
    }

    if (args.operation == "revdump"):
        print('Downloading all revisions of \"{}\"...\n'.format(fileName))
        dump_revisions(params)
    elif (args.operation == "download"):
        recursive_downloader(args.file_id, fileDLPath, service, import_bypass=args.import_bypass)

    #cleanup:
    #remove the tmp folder in the user's gdrive, if created
    global tmp_folder_fileid
    if tmp_folder_fileid is not None:
        service.files().delete(
            fileId = tmp_folder_fileid
        ).execute()
        tmp_folder_fileid = None

    return

if __name__ == '__main__':
    main()