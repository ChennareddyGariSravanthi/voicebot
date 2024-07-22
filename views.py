from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.uploadedfile import UploadedFile
from .sdk import setup, stream_conversation
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request, 'bot/index.html')

@csrf_exempt
def setup_sdk(request):
    if request.method == 'POST':
        stt_key = request.POST.get('stt_key')
        tts_key = request.POST.get('tts_key')
        llm_key = request.POST.get('llm_key')
        setup(stt_key, tts_key, llm_key)
        return JsonResponse({'message': 'SDK setup complete'})
    return render(request, 'bot/index.html')

@csrf_exempt
def start_streaming(request):
    if request.method == 'POST':
        audio_file = request.FILES.get('audio_file')
        if isinstance(audio_file, UploadedFile):
            audio_response = stream_conversation(audio_file)
            response_audio_url = save_audio_file(audio_response)
            return JsonResponse({'audio_url': response_audio_url})
        return JsonResponse({'error': 'Invalid audio file'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def save_audio_file(audio_stream):
    file_path = 'media/response_audio.wav'
    with open(file_path, 'wb') as f:
        f.write(audio_stream.read())
    return file_path
