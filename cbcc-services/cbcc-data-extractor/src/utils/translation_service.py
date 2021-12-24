from collections import namedtuple

from deep_translator import (GoogleTranslator,
                             MicrosoftTranslator,
                             MyMemoryTranslator,
                             YandexTranslator,
                             DeepL)

from src.utils.config_reader import ConfigReader
from src.utils.env_reader import EnvReader

class TranslationService:
    def __init__(self, config_reader: ConfigReader, env_reader: EnvReader) -> None:
        
        self.config_reader = config_reader
        self.env_reader = env_reader
        
        self.translation_apis = dict()
        
        if (bool(self.config_reader.read('translation_apis', 'google_translate'))):
            self.translation_apis['google_translate'] = lambda text_to_translate: self._call_google_translate_api(text_to_translate)
            
        if (bool(self.config_reader.read('translation_apis', 'mymemory_translate'))):
            self.translation_apis['mymemory_translate'] = lambda text_to_translate: self._call_mymemory_translate_api(text_to_translate)
            
        if (bool(self.config_reader.read('translation_apis', 'deepl_translate'))):
            self.translation_apis['deepl_translate'] = lambda text_to_translate: self._call_deepl_translate_api(text_to_translate)
            
        if (bool(self.config_reader.read('translation_apis', 'yandex_translate'))):
            self.translation_apis['yandex_translate'] = lambda text_to_translate: self._call_yandex_translate_api(text_to_translate)
            
        if (bool(self.config_reader.read('translation_apis', 'microsoft_translate'))):
            self.translation_apis['microsoft_translate'] = lambda text_to_translate: self._call_microsoft_translate_api(text_to_translate)
            
    def translate(self, text_to_translate) -> str:     
        for _, translation_api_call in self.translation_apis.items():
            try:
                print('starting translation')
                translated_text = translation_api_call(text_to_translate)
                print(f'translation successful: {translated_text}')
                return translated_text
            except:
                print('translation failed, moving onto the next one')
            
        return ''
    
    def _call_google_translate_api(self, text_to_translate):
        return GoogleTranslator(source='ja', target='en').translate(text_to_translate)
    
    def _call_mymemory_translate_api(self, text_to_translate):
        return MyMemoryTranslator(source='ja', target='en').translate(text_to_translate)
    
    def _call_deepl_translate_api(self, text_to_translate):
        deepl_api_key = self.env_reader.read('DEEPL_API_KEY')
        return DeepL(api_key=deepl_api_key, source='ja', target='en').translate(text_to_translate)
    
    def _call_yandex_translate_api(self, text_to_translate):
        yandex_api_key = self.env_reader.read('YANDEX_API_KEY')
        return YandexTranslator(yandex_api_key).translate(source='ja', target='en', text=text_to_translate)
    
    def _call_microsoft_translate_api(self, text_to_translate):
        microsoft_api_key = self.env_reader.read('MICROSOFT_API_KEY')
        return MicrosoftTranslator(api_key=microsoft_api_key, target='en').translate(text=text_to_translate)
    