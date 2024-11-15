from app.translator.__interface import Translator
from app.config import CLOSE_MODELS

def get_translator(name) -> Translator:
    if name in CLOSE_MODELS.keys():
        from app.translator.model_closesource import CloseTranslator
        return CloseTranslator()
    else:
        from app.translator.model_opensource import OpenTranslator
        return OpenTranslator()
