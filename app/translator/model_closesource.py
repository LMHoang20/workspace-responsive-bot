from functools import lru_cache

from langchain.chat_models import init_chat_model
from langchain_core.globals import set_verbose, set_debug
set_verbose(False)
set_debug(False)

from app.translator.__interface import Translator
from app.config import *

class CloseTranslator(Translator):
    def __init__(self) -> None:
        pass

    @staticmethod
    @lru_cache(maxsize=2)
    def get_model(src: str, dst: str):
        chosen_model = CLOSE_MODELS[USING_MODEL]
        model = init_chat_model(**chosen_model['config'])
        def translate(text: str) -> str:
            prompt = chosen_model['template'].format(
                src=SUPPORTED_LANGUAGES[src], 
                dst=SUPPORTED_LANGUAGES[dst], 
                text=text
            )
            response = model(prompt)
            return response.content
        return translate
    
    def translate(self, text: str, src: str=DEFAULT['source'], dst: str=DEFAULT['target']) -> str:
        if not Translator.need_translation(text, src, dst):
            return text
        translator = self.get_model(src, dst)
        return translator(text)
        
if __name__ == "__main__":
    translator = CloseTranslator()
    
    text = "Xin chào, tôi là một con hải cẩu."

    translated = translator.translate(text)
    print(translated)
