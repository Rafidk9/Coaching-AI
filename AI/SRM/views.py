import datetime
from googleapiclient.discovery import build
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from django.shortcuts import render, redirect, HttpResponse
from .models import *
from .forms import *
import os, json

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


def get_recording(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        date = request.POST.get('date')
        topic = request.POST.get('topic')
        
        # Load your Google Drive credentials from the specified path
        credentials_path = os.path.join('C:\\Users\\Admin\\django\\AI', 'ai-coaching-399821-60e6e97480fe.json')
        creds = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=['https://www.googleapis.com/auth/drive.readonly']
        )

        # Build the Drive API service
        service = build('drive', 'v3', credentials=creds)

        folder_query = "mimeType='application/vnd.google-apps.folder' and 'Recordings' in parents"
        folder_results = service.files().list(q=folder_query).execute()

        # Check if the 'Recordings' folder exists
        recordings_folder = folder_results.get('files', [])

        if recordings_folder:
            # Assuming 'Recordings' folder exists, now search within 'A2 May 23'
            file_query = f"name='Sniping spots for Nibir' and '{recordings_folder[0]['id']}' in parents"
            file_results = service.files().list(q=file_query).execute()

            # Check if the file exists in 'A2 May 23'
            files_in_a2_may_23 = file_results.get('files', [])

            if files_in_a2_may_23:
                # Assuming you want the link to the first matching file
                recording_link = files_in_a2_may_23[0]['webViewLink']
            
            # Update the student's recordings_given and last_recording_date fields
            student = Student.objects.get(name=name)
            student.recordings_given += 1
            student.last_recording_date = datetime.date.today()
            student.save()
            
            # Return the Google Drive link
            return HttpResponse(f'Here is the Google Drive link for the recording: {recording_link}')
        else:
            return HttpResponse('No matching recording found.')

    else:
        return render(request, 'get_recordings.html')


def homepage(request):
    return render(request, 'index.html')


def facebook_webhook(request):
    if request.method == 'GET':
        # Facebook verification
        verify_token = "123456789"  # Set this to your Verify Token
        if request.GET.get('hub.verify_token') == verify_token:
            return HttpResponse(request.GET.get('hub.challenge'))
        else:
            return HttpResponse("Invalid Verify Token", status=403)
    elif request.method == 'POST':
        # Handle incoming messages
        data = json.loads(request.body.decode('utf-8'))
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                sender_id = messaging_event['sender']['id']
                message_text = messaging_event['message']['text']
                # Implement your logic to process the message and respond
                # Example: Look up student data and generate Google Drive link
        return HttpResponse()
    else:
        return HttpResponse(status=405)

# from fbchat import Client
# from fbchat.models import Message

# def send_google_drive_link(user_id, link):
#     client = Client("Rafid Khan", "matapyk5")
#     message = f"Here's the Google Drive link to the class recording: {link}"
#     client.send(Message(text=message), thread_id=user_id, thread_type=ThreadType=.USER)
#     client.logout()
