from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from pytube import YouTube
from django.conf import settings
import os
import assemblyai as aai
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def index(request):
    return render(request,'index.html')

@csrf_exempt
def generate_blog(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            yt_link =data['link']
            return JsonResponse({'content':yt_link})

        except(KeyError,json.JSONDecodeError):
            return JsonResponse({'erorr':'Invalid data sent'},status=400)
        # title = yt_title(yt_link)

        # transcription = get_transcript(yt_link)
        # if not transcription:
        #     return JsonResponse({'erorr':'Invalid data sent'},status=400)
            

    
    else:
        return JsonResponse({'erorr':'Invalid request method'},status=405)
    

def yt_title(link):
    yt = YouTube(link)
    title = yt.title
    return title
def download_audio(link):
    yt =YouTube(link)
    video =yt.streams.filter(only_audio=True).first()
    out_file =video.download(output_path=settings.MEDIA_ROOT)
    base ,ext =os.path.splitext(out_file)
    new_file =base + '.mp3'
    os.rename(out_file,new_file)
    return new_file

def get_transcript(link):
    audio_file =download_audio(link)
    aai.settings.api_key = ""
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file)

    return transcript.text
def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user =authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            error_message = "Invalid username or password"
            return render(request,'login.html',{'error_message':error_message})

    return render(request,'login.html')
def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repeatPassword = request.POST['repeatPassword']
        if password == repeatPassword:
            try:
                user = User.objects.create_user(username,email,password)
                user.save()
                login(request,user)
                return redirect('/')
            except:
                error_message = "Error creating account" 
                return render(request ,'signup.html',{'error_message':error_message})
        else:
            error_message ="Password don't matach   "
            return render(request ,'signup.html',{'error_message':error_message})
    return render(request,'signup.html')

def user_logout(request):
    logout(request)
    return redirect('/')