from app.translator.__interface import Translator
from app.config import CLOSE_MODELS

from app.translator.model_closesource import CloseTranslator
from app.translator.model_opensource import OpenTranslator

def get_translator(name) -> Translator:
    if name in CLOSE_MODELS.keys():
        return CloseTranslator()
    else:
        return OpenTranslator()
