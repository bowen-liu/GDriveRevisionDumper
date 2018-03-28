#MimeTypes for Google Doc files (and similar derivatives)
GDOC_MIMETYPE = 'application/vnd.google-apps.document'
GSHEET_MIMETYPE = 'application/vnd.google-apps.spreadsheet'
GSLIDE_MIMETYPE = 'application/vnd.google-apps.presentation'
GDRAWING_MIMETYPE = 'application/vnd.google-apps.drawing'


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


