import os
import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseUpload

# Enter the credentials of the Google account with access to the Drive API
creds = service_account.Credentials.from_service_account_file('path/to/credentials.json')

# Create a Google Drive API client
drive_service = build('drive', 'v3', credentials=creds)

# Set the name of the new folder
folder_name = 'My New Folder'

# Create the folder
folder_metadata = {'name': folder_name, 'mimeType': 'application/vnd.google-apps.folder'}
folder = drive_service.files().create(body=folder_metadata, fields='id').execute()

# Set the ID of the new folder
folder_id = folder.get('id')

# Set the path of the directory containing the files to be uploaded
directory_path = 'path/to/directory'

# Get the list of files in the directory
files = os.listdir(directory_path)

# Upload each file to the new folder
for file_name in files:
    file_path = os.path.join(directory_path, file_name)
    file_metadata = {'name': file_name, 'parents': [folder_id]}
    media = MediaFileUpload(file_path, resumable=True)
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f'File ID: {file.get("id")} has been uploaded to the folder.')
