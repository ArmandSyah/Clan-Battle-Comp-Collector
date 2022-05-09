import logging

from deep_translator import (GoogleTranslator,
                             MicrosoftTranslator,
                             MyMemoryTranslator,
                             YandexTranslator,
                             DeepL)

class TranslationService:
    def __init__(self, config) -> None:
        self.logger = logging.getLogger('dataExtractorLogger')

        # Translation api keys
        self.deepl_api_key = config["deepl_api_key"]
        self.yandex_api_key = config["yandex_api_key"]
        self.microsoft_api_key = config["microsoft_api_key"]
        
        self.translation_apis = dict()

        google_translate = config["usedtranslationapis"]["google_translate"]
        mymemory_translate = config["usedtranslationapis"]["mymemory_translate"]
        deepl_translate = config["usedtranslationapis"]["deepl_translate"]
        yandex_translate = config["usedtranslationapis"]["yandex_translate"]
        microsoft_translate = config["usedtranslationapis"]["microsoft_translate"]
        
        if (bool(google_translate)):
            self.translation_apis['google_translate'] = lambda text_to_translate: self._call_google_translate_api(text_to_translate)
            
        if (bool(mymemory_translate)):
            self.translation_apis['mymemory_translate'] = lambda text_to_translate: self._call_mymemory_translate_api(text_to_translate)
            
        if (bool(deepl_translate)):
            self.translation_apis['deepl_translate'] = lambda text_to_translate: self._call_deepl_translate_api(text_to_translate)
            
        if (bool(yandex_translate)):
            self.translation_apis['yandex_translate'] = lambda text_to_translate: self._call_yandex_translate_api(text_to_translate)
            
        if (bool(microsoft_translate)):
            self.translation_apis['microsoft_translate'] = lambda text_to_translate: self._call_microsoft_translate_api(text_to_translate)
            
    def translate(self, text_to_translate) -> str:     
        for translation_api_call in self.translation_apis.values():
            try:
                self.logger.debug('starting translation')
                translated_text = translation_api_call(text_to_translate)
                self.logger.debug(f'translation successful: {translated_text}')
                return translated_text
            except:
                self.logger.debug('translation failed, moving onto the next one')
            
        return ''
    
    def _call_google_translate_api(self, text_to_translate):
        return GoogleTranslator(source='ja', target='en').translate(text_to_translate)
    
    def _call_mymemory_translate_api(self, text_to_translate):
        return MyMemoryTranslator(source='ja', target='en').translate(text_to_translate)
    
    def _call_deepl_translate_api(self, text_to_translate):
        return DeepL(api_key=self.deepl_api_key, source='ja', target='en').translate(text_to_translate)
    
    def _call_yandex_translate_api(self, text_to_translate):
        return YandexTranslator(self.yandex_api_key).translate(source='ja', target='en', text=text_to_translate)
    
    def _call_microsoft_translate_api(self, text_to_translate):
        return MicrosoftTranslator(api_key=self.microsoft_api_key, target='en').translate(text=text_to_translate)
    