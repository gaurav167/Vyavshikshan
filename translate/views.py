from django.shortcuts import render
from django.http import JsonResponse
from googletrans import Translator

def translate(request):
	if request.method == 'POST':
		from_language = request.POST['from']
		to_language = request.POST['to']
		text = request.POST['text']
		mapping_values={'Telugu': 'te',
		                'Punjabi': 'pa',
		                'Kannada': 'kn',
		                'Hindi': 'hi',
		                'Tamil': 'ta',
		                'Malayalam': 'ml',
		                'English': 'en',
		                'Bengali': 'bn',
		                'Marathi': 'mr',
		                'Gujarati': 'gu',
		                'Urdu': 'ur'}

		to_language = to_language[0].upper() + to_language[1:].lower()
		from_language = from_language[0].upper() + from_language[1:].lower()
		translator = Translator()
		code_to_language = mapping_values[to_language]
		code_from_language = mapping_values[from_language]
		translatedObject = translator.translate(text, src=code_from_language, dest=code_to_language)
		return JsonResponse({'staus':'success','text':translatedObject.text})
	else:
		return JsonResponse({'error':'Only available via POST.','status_code':'400'})