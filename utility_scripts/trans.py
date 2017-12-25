from googletrans import Translator

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

def conversion(languageTo, string_from):
    languageTo = languageTo[0].upper() + languageTo[1:].lower()
    translator = Translator()
    codeLanguageTo = mapping_values[languageTo]

    translatedObject = translator.translate(string_from, src='en', dest=codeLanguageTo)
    return translatedObject.text


if __name__ == '__main__':
    answer = conversion('Hindi',"""Hello World""")
    print(answer)
