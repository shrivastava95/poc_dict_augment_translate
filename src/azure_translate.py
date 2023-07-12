# -*- coding:utf-8 -*-
import io
import requests
import json
import os
import uuid
from dotenv import load_dotenv
import re

load_dotenv()

sample_text = "ତୁମର କୋଡ୍ ରିଫାକ୍ଟର୍ କରିବାକୁ ଯାହା ଦ୍ you ାରା ତୁମେ ଲୁପ୍ ପାଇଁ ପ୍ରତିକ୍ରିୟାକୁ ଅପେକ୍ଷା କରୁନାହଁ, ତୁମେ ଏକାସାଙ୍ଗରେ ଇନ୍ଫରେନ୍ସ ଫଙ୍କସନ୍ ର ଏକାଧିକ ଉଦାହରଣ ଚଲାଇବାକୁ ବ୍ୟବହାର କରିପାରିବ | ଏଠାରେ ଅପଡେଟ୍ କୋଡ୍ ଅଛି |"

# wrapper function to wrap every instance of original word to its target translation
# example:       <mstrans:dictionary translation=target>original</mstrans:dictionary>
def wrap_phrases(sentence, phrases, pattern):
    result = pattern.sub(lambda x: '<mstrans:dictionary translation=' + phrases[x.group()] + '>' + x.group() + '</mstrans:dictionary>', sentence)
    return result

def azure_translate(target_language, source_sentence):
    endpoint = 'https://api.cognitive.microsofttranslator.com/translate?api-version=3.0'
    params = '&to=' + target_language
    headers = {
        'Ocp-Apim-Subscription-Key': os.getenv("AZURE_API_KEY_GAUTAM"),
        'Content-type': 'application/json',
        'Ocp-Apim-Subscription-Region': 'southeastasia',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    body = [{'text': source_sentence}]
    response = requests.post(endpoint + params, headers=headers, data=json.dumps(body))
    response = response.json()
    translated_text = response[0]['translations'][0]['text']
    return translated_text

def augmented_azure_translate(target_language, source_sentence, data_dict):# precompute the pattern to match using the noun translation dictionary
    keys = (re.escape(k) for k in data_dict.keys())
    pattern = re.compile('|'.join(keys))
    wrapped_sentence = wrap_phrases(source_sentence, data_dict, pattern)
    return azure_translate(target_language, wrapped_sentence)

# print(azure_translate('en', sample_text))

