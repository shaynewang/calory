from google.cloud import translate

class Translator:
    def __init__(self):
        self.client = translate.Client()
        self.languages = self.client.get_languages()

    def available_languages(self):
        return self.languages

    def translate(self, text, target_language):
        translated = self.client.translate(text, target_language=target_language)
        return translated["translatedText"]
