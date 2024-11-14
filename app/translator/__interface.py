from .language_detector import LanguageDetector

from app.config import SUPPORTED_LANGUAGES

class Translator:
    def translate(text: str, src: str='vi', dst: str='en') -> str:
        raise NotImplementedError
    
    @staticmethod
    def need_translation(text: str, src: str, dst: str) -> bool:
        if src not in SUPPORTED_LANGUAGES or dst not in SUPPORTED_LANGUAGES:
            raise ValueError("Unsupported language")
        if src == dst:
            return False
        if LanguageDetector().detect(text) == dst:
            return False
        return True
