from lingua import Language, LanguageDetectorBuilder

from app.utility import SingletonMeta
from app.config import SUPPORTED_LANGUAGES

class LanguageDetector(metaclass=SingletonMeta):
    def __init__(self):
        languages = Language.all()
        languages = filter(lambda lang: lang.iso_code_639_1.name.lower() in SUPPORTED_LANGUAGES, languages)
        self.detector = LanguageDetectorBuilder.from_languages(*languages).build()

    def detect(self, text: str) -> str:
        prediction = self.detector.detect_language_of(text)
        if prediction is None:
            return None
        return prediction.iso_code_639_1.name.lower()
    