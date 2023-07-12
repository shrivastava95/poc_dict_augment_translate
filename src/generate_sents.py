import openai
import os
from dotenv import load_dotenv
import html
import json

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY_GAUTAM')

def get_sentences_chatgpt(source, translation):
    """"
    generates k sentences using the following prompt template:"""

    messages = [
        {
            "role": "user", 
            "content": f"""{{Answer as succinctly as possible}}
Generate sentences in Odia containing the word {source} assuming it means the word {translation} in an agricultural context. The word must be in different positions in the sentence(middle beggining, end etc). Also provide translations for each sentence to english. Give the output in this format:
[["sentence1", "translation1"],
["sentence2", "translation2"],
.
.
.
["sentenceN", "translationN"]]"""
        }
    ]
    completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        temperature = 0.5,
        max_tokens = 3500,
        messages = messages
    )
    print(completion)

    gpt_text = html.unescape(completion.choices[0].message['content'])
    gpt_text = ''.join(gpt_text.split('\n'))
    print(gpt_text)
    sentence_translations = json.loads(gpt_text)
    return sentence_translations

# translations = get_sentences_chatgpt("ଖଡ଼", "Aphid")
# print(len(translations))
# for translation in translations:
#     print(translation)
