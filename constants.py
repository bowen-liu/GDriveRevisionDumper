#Missing API KEY message
MISSING_API_KEY_TUT = 'To obtain your own Google Drive API key, please do the following: \n\n\
\tStep 1: Go to \"https://console.developers.google.com/start/api?id=drive\" to create or select a project in the Google Developers Console and automatically turn on the API. Click Continue, then Go to credentials. \n \
\tStep 2: On the Add credentials to your project page, click the Cancel button. \n \
\tStep 3: At the top of the page, select the OAuth consent screen tab. Select an Email address, enter a Product name if not already set, and click the Save button. \n \
\tStep 4: Select the Credentials tab, click the Create credentials button and select OAuth client ID. \n \
\tStep 5: Select the application type Other, enter the name \"Drive API Quickstart\", and click the Create button. \n \
\tStep 6: Click OK to dismiss the resulting dialog. \n \
\tStep 7: Click the Download JSON button (downwards arrow icon) to the right of the client ID. \n \
\tStep 8: Move this file in the same directory as the main script and rename it \"client_secret.json\" \n\n \
Source: https://developers.google.com/drive/v3/web/quickstart/python#step_1_turn_on_the_api_name'


#MimeTypes for Google Doc files (and similar derivatives)
GDOC_MIMETYPE = 'application/vnd.google-apps.document'
GSHEET_MIMETYPE = 'application/vnd.google-apps.spreadsheet'
GSLIDE_MIMETYPE = 'application/vnd.google-apps.presentation'
GDRAWING_MIMETYPE = 'application/vnd.google-apps.drawing'
GFOLDER_MIMETYPE = 'application/vnd.google-apps.folder'


#Available Export Formats for Google Doc
GDOC_EXPORT_FORMATS = {
    'rtf' : 'application/rtf',
    'odt' : 'application/vnd.oasis.opendocument.text',
    'html' : 'text/html',
    'epub' : 'application/epub+zip',
    'docx' : 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'pdf' : 'application/pdf',
    'zip' : 'application/zip',
    'txt' : 'text/plain',
}


#Available Export Formats for Google Sheet
GSHEET_EXPORT_FORMATS = {
    'xods' : 'application/x-vnd.oasis.opendocument.spreadsheet',
    'tsv' : 'text/tab-separated-values',
    'xlsx' : 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'csv' : 'text/csv',
    'ods' : 'application/vnd.oasis.opendocument.spreadsheet',
    'pdf' : 'application/pdf',
    'zip' : 'application/zip',
    'txt' : 'text/plain',
}


#Available Export Formats for Google Slides
GSLIDE_EXPORT_FORMATS = {
    'odp' : 'application/vnd.oasis.opendocument.presentation',
    'pptx' : 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'pdf' : 'application/pdf',
}


#Available Export Formats for Google Drawing (Also available: EXPORT_PDF)
GDRAWING_EXPORT_FORMATS = {
    'svg' : 'image/svg+xml',
    'png' : 'image/png',
    'jpeg' : 'image/jpeg',
    'pdf' : 'application/pdf',
}


#Default exporting formats
GDOC_DEFAULT_FORMAT = 'docx'
GSHEET_DEFAULT_FORMAT = 'xlsx'
GSLIDE_DEFAULT_FORMAT = 'pptx'
GDRAWING_DEFAULT_FORMAT = 'jpeg'