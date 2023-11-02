import datetime, os, json, logging
from datetime import date
from googleapiclient.discovery import build
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from django.shortcuts import render, redirect, HttpResponse
from .models import *
from .forms import *
from googleapiclient.errors import HttpError
from django.http import JsonResponse


def student_list(request):
    students = Student.objects.all()
    return render(request,'student_list.html',{'students': students})


def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'student_create.html', {'form': form})


def batch_list(request):
    batch = Batch.objects.all()
    return render(request, 'batch_list.html', {'batch': batch})


def batch_create(request):
    if request.method == 'POST':
        form = BatchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('batch_list')
    else:
        form = BatchForm(request.POST)
    return render(request, 'batch_create.html', {'form': form})


def index(request):
    return render(request, 'index.html')


def get_recording(request):
    if request.method == 'POST':
        stud_name = request.POST.get('stud_name')
        target_video_name = request.POST.get('rec_name')
        selected_folder = request.POST.get('selected_folder')

        # Load your Google Drive credentials from the specified path
        credentials_path = os.path.join('C:\\Users\\Admin\\django\\AI', 'ai-coaching-399821-60e6e97480fe.json')
        creds = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=['https://www.googleapis.com/auth/drive.readonly'],
            subject='ai-coaching@ai-coaching-399821.iam.gserviceaccount.com'  # Replace with the actual service account email
        )

        # Build the Drive API service
        service = build('drive', 'v3', credentials=creds)

        try:
            # List folders in Google Drive
            folders = []
            folder_query = "mimeType='application/vnd.google-apps.folder'"
            results = service.files().list(q=folder_query).execute()
            items = results.get('files', [])

            for item in items:
                folders.append(item['name'])

            # Get the ID of the selected folder
            selected_folder_id = None
            for item in items:
                if item['name'] == selected_folder:
                    selected_folder_id = item['id']
                    break

            if not selected_folder_id:
                return HttpResponse(f'Selected folder not found: {selected_folder}')

            # Iterate through the selected folder to find the video
            results = service.files().list(
                q=f"'{selected_folder_id}' in parents",
                pageSize=10, fields="nextPageToken, files(id, name)").execute()
            items = results.get('files', [])

            # Search for a specific video file by name
            target_video_id = None
            for item in items:
                if item['name'] == target_video_name:
                    target_video_id = item['id']
                    break

            # Update the student's recordings_given and last_recording_date fields
            student = Student.objects.get(name=stud_name)
            student.recordings_given += 1
            student.last_recording_date = datetime.date.today()
            student.save()
            # Check if the student has already taken 3 recordings in the past week 
            #and recordings can only be given on wednesday
            #if a student took 3 recordings in the past week , they may no longer be given more this week
            if student.recordings_given == 3 and student.last_recording_date.isocalendar()[2] < 7 and student.recordings_given.weekday() == 2:
                return HttpResponse(f'Student {stud_name} has already taken 3 recordings in the past week.')
            else:
                    
                

                if target_video_id:
                    # Retrieve the webViewLink of the specific video file
                    file_metadata = service.files().get(
                        fileId=target_video_id, fields="webViewLink").execute()
                    webViewLink = file_metadata.get('webViewLink')

                    if webViewLink:
                        # Return the Google Drive link to the video as an HTTP response with an anchor tag
                        return render(request, 'recording.html', {'recording_link': webViewLink})
                    else:
                        return HttpResponse(f'No webViewLink found for the video: {target_video_name}')
                else:
                    return render(request, 'recording.html', {'recording_link': None})

        except Exception as error:
            # Handle errors from Drive API
            logging.error(f'An error occurred: {error}')
            return HttpResponse(f'An error occurred: {error}')

    else:
        # Fetch the list of folders and pass it to the template
        try:
            credentials_path = os.path.join('C:\\Users\\Admin\\django\\AI', 'ai-coaching-399821-60e6e97480fe.json')
            creds = service_account.Credentials.from_service_account_file(
                credentials_path,
                scopes=['https://www.googleapis.com/auth/drive.readonly'],
                subject='ai-coaching@ai-coaching-399821.iam.gserviceaccount.com'  # Replace with the actual service account email
            )

            # Build the Drive API service
            service = build('drive', 'v3', credentials=creds)

            # List folders in Google Drive
            folders = []
            folder_query = "mimeType='application/vnd.google-apps.folder'"
            results = service.files().list(q=folder_query).execute()
            items = results.get('files', [])

            for item in items:
                if item['name'] == 'Recordings':
                    continue  # Skip the "Recordings" 
                folders.append(item['name'])

            return render(request, 'get_recordings.html', {'available_folders': folders})

        except Exception as error:
            # Handle errors from Drive API
            logging.error(f'An error occurred: {error}')
            return HttpResponse(f'An error occurred: {error}')



