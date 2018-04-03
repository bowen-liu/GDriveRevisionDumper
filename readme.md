# Google Drive Revision History Downloader

This python script allows you to download all individual revisions available for a file on Google Drive. While this script was designed primarily for downloading Google Docs type files, regular files works too. 

Note that the script was not designed to handle large files. You may get memory related errors if you specify a large file for download.

## Prerequisites

In order to run the script, you must first have Python 3 installed. The script also requires the Google Client Library, which can be installed with the following command:

>pip install --upgrade google-api-python-client

You must also turn on Google Drive API and generate your own API key in order to use the script. This is needed for the script to _locally_ authenticate your user account to gain permission to read your files. This can be done in the following procedure:

```
Step 1: Go to "https://console.developers.google.com/start/api?id=drive" to create or select a project in the Google Developers Console and automatically turn on the API. Click Continue, then Go to credentials.

Step 2: On the Add credentials to your project page, click the Cancel button. 

Step 3: At the top of the page, select the OAuth consent screen tab. Select an Email address, enter a Product name if not already set, and click the Save button. 

Step 4: Select the Credentials tab, click the Create credentials button and select OAuth client ID.

Step 5: Select the application type Other, enter the name "Drive API Quickstart", and click the Create button.

Step 6: Click OK to dismiss the resulting dialog. 

Step 7: Click the Download JSON button (downwards arrow icon) to the right of the client ID.

Step 8: Move this file in the same directory as the main script and rename it "client_secret.json" 
```

For more information about getting started with Google Drive API in python, please visit: https://developers.google.com/drive/v3/web/quickstart/python#step_1_turn_on_the_api_name' 

## Usage

When running the script, up to two arguments can be specified in the following form:

>python main.py fileID --format FORMAT

**fileID** is a mandatory argument. This is Google's unique identifier for the file you're wanting to download. You can find the identifier from the sharelink for your file.

For example, the share link for a file we want to download is https://drive.google.com/open?id=1aB1CFZ_KRdwabWIctMLqoimG3Fn1dnuBelKanLNjfP8

The fileID would therefore be _1aB1CFZ_KRdwabWIctMLqoimG3Fn1dnuBelKanLNjfP8_

**--format** is an optional argument used when downloading Google Docs files only, as there are many export options available. If this argument is not specified when downloading a Google Doc file, the default export format will be used. 

Below is a list of available export formats for supported Google Docs files. Bolded formats are the defaults.
- For Google Docs: rtf, odt, html, epub, **docx**, pdf, zip, txt
- For Google Sheets: ods, tsv, **xlsx**, csv, pdf, zip, txt
- For Google Slides: odp, **pptx**, pdf
- For Google Drawing: svg, png, **jpeg**, pdf


