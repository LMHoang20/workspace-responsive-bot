from transformers import pipeline
from functools import lru_cache
from operator import itemgetter

from app.translator.__interface import Translator

from app.config import *
from app.utility import extract_text, unique_string

def get_device():
    import torch
    return (0 if torch.cuda.is_available() else "cpu")

class OpenTranslator(Translator):
    def __init__(self) -> None:
        # pre-load default model
        OpenTranslator.get_model(DEFAULT['source'], DEFAULT['target'])

    @staticmethod
    @lru_cache(maxsize=2)
    def get_model(src: str, dst: str):
        language_option = f"{src}-{dst}"

        if language_option in OPEN_MODELS:
            name, template = itemgetter('name', 'template')(OPEN_MODELS[language_option])
            return pipeline(
                task="translation", 
                model=name,
                device=get_device()
            ), template
        else:
            name, template = itemgetter('name', 'template')(OPEN_MODELS['default'])
            return pipeline(
                task=f"translation_{src}_to_{dst}",
                model=name,
                device=get_device()
            ), template

    def translate(self, text: str, src: str=DEFAULT['source'], dst: str=DEFAULT['target']) -> str:
        if not Translator.need_translation(text, src, dst):
            return text
        translator, template = self.get_model(src, dst)
        lines = map(str.strip, text.split('\n'))
        results = []
        for line in lines:
            if line == "" or not any(c.isalpha() for c in line):
                continue
            result = translator(
                self._encode(line, template, language=src),
                max_length=128
            )[0]['translation_text']
            results.append(self._decode(result, template, language=dst))
        return '\n'.join(results)
    
    def _encode(self, text: str, template: str, language: str=DEFAULT['source']) -> str:
        return template.format(language=language, text=text)
    
    def _decode(self, text: str, template: str, language: str=DEFAULT['target']) -> str:
        mask_1 = text
        mask_2 = template.format(language=language, text=unique_string())
        return extract_text(mask_1, mask_2)
    
if __name__ == "__main__":
    translator = OpenTranslator()
    
    text = "Xin chào, tôi là một con hải cẩu."
    print(text)

    translated = translator.translate(text)
    print(translated)
