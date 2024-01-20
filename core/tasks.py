from celery import shared_task
from .models import *
from gtts import gTTS
import speech_recognition as sr
import os
from time import sleep
import sys 
from hashlib import sha1, md5 
from collections import OrderedDict 
from urllib.parse import urlencode 
import hmac 
import requests 
import base64 
import json
from datetime import datetime, timezone, timedelta
import subprocess

def format_phone(phone):
    format_phone = ''.join(filter(str.isdigit, phone))
    if format_phone[0] == "+":
        pass



def get_current_datetime():

    msk_timezone = timezone(timedelta(hours=3))

    current_datetime_msk = datetime.now(msk_timezone)

    formatted_datetime = current_datetime_msk.strftime("%Y-%m-%d %H:%M:%S")

    return formatted_datetime


def get_hours_ago_datetime():
    msk_timezone = timezone(timedelta(hours=3))

    current_datetime_msk = datetime.now(msk_timezone)

    yesterday_datetime_msk = current_datetime_msk - timedelta(hours=1)

    formatted_yesterday_datetime = yesterday_datetime_msk.strftime("%Y-%m-%d 00:00:00")

    return formatted_yesterday_datetime

class NovofonApi(): 
    def __init__(self, key, secret): 
        self.key = key 
        self.secret = secret 
        self.url_api = "https://api.novofon.com" 

    def call(self, method, params={}, request_type='GET', format='json', is_auth=True):
        request_type = request_type.upper()
        if request_type not in ['GET', 'POST', 'PUT', 'DELETE']:
            request_type = 'GET'
        params['format'] = format
        auth_str = None
        is_nested_data = False
        for k in params.values():
            if not isinstance(k, str):
                is_nested_data = True
                break
        if is_nested_data:
            params_string = self.__http_build_query(OrderedDict(sorted(params.items())))
            params = params_string
        else:
            params_string = urlencode(OrderedDict(sorted(params.items())))

        if is_auth:
            auth_str = self.__get_auth_string_for_header(method, params_string)

        if request_type == 'GET':
            result = requests.get(self.url_api + method + '?' + params_string, headers={'Authorization': auth_str})
        elif request_type == 'POST':
            result = requests.post(self.url_api + method, headers={'Authorization': auth_str}, data=params)
        elif request_type == 'PUT':
            result = requests.put(self.url_api + method, headers={'Authorization': auth_str}, data=params)
        elif request_type == 'DELETE':
            result = requests.delete(self.url_api + method, headers={'Authorization': auth_str}, data=params)
        return result.text

    def __http_build_query(self, data):
        parents = list()
        pairs = dict()

        def renderKey(parents):
            depth, outStr = 0, ''
            for x in parents:
                s = "[%s]" if depth > 0 or isinstance(x, int) else "%s"
                outStr += s % str(x)
                depth += 1
            return outStr

        def r_urlencode(data):
            if isinstance(data, list) or isinstance(data, tuple):
                for i in range(len(data)):
                    parents.append(i)
                    r_urlencode(data[i])
                    parents.pop()
            elif isinstance(data, dict):
                for key, value in data.items():
                    parents.append(key)
                    r_urlencode(value)
                    parents.pop()
            else:
                pairs[renderKey(parents)] = str(data)

            return pairs
        return urlencode(r_urlencode(data))

    def __get_auth_string_for_header(self, method, params_string):
        data = method + params_string + md5(params_string.encode('utf8')).hexdigest()
        hmac_h = hmac.new(self.secret.encode('utf8'), data.encode('utf8'), sha1)
        if sys.version_info.major > 2:
            bts = bytes(hmac_h.hexdigest(), 'utf8')
        else:
            bts = bytes(hmac_h.hexdigest()).encode('utf8')
        auth = self.key + ':' + base64.b64encode(bts).decode()
        return auth
    
# api = NovofonApi(key='631beaed144d4ff61bef', secret='840f35914999a041f306')
# data = json.loads(api.call('/v1/statistics/', {"start": get_hours_ago_datetime(), "end": get_current_datetime()}))
# print(data["stats"][-1]["disposition"])


def get_last():
    dir_list = [os.path.join("/records", x) for x in os.listdir("/records")]

    if dir_list:
        date_list = [[x, os.path.getctime(x)] for x in dir_list]

        sort_date_list = sorted(date_list, key=lambda x: x[1], reverse=True)

    return sort_date_list[0][0]
def speech_to_text(audio_file_path):
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_file_path) as source:
        audio_data = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio_data, language="ru")
            return text
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            return None


def text_to_gsm(text, output_file="/usr/share/asterisk/sounds/custom/temp.gsm", lang="ru"):
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save("temp.mp3")
    os.system(f"sox temp.mp3 -r 8000 -e gsm {output_file}")

    

@shared_task(bind=True)
def call(self, id):
    api = NovofonApi(key=os.getenv('API_KEY'), secret=os.getenv('API_SECRET'))
    route = Route.objects.get(id=id)
    for order in route.orders.all():
        text_to_gsm("Здравствуйте это петровские окна у вас на завтра есть заказ можете принять если нет продиктуйте пожалуйста новую дату и время принятия")
        sleep(5)
        os.system(f'asterisk -rx "channel originate SIP/novofon/{order.phone} extension {order.phone}@novofon-out"')
        sleep(60)

        data = json.loads(api.call('/v1/statistics/', {"start": get_hours_ago_datetime(), "end": get_current_datetime()}))
        order.call_status = data["stats"][-1]["disposition"]

        if data["stats"][-1]["disposition"] == "answered":
            record = get_last()
            text = speech_to_text(record)
            if text == None:
                order.call_text = "Не удалось распознать"
            else:
                order.call_text = text
            path = Path(record)
            with path.open(mode = 'rb') as f:
                order.call_audio = File(f, name = path.name)
            order.save()
        else:
            order.call_text = data["stats"][-1]["disposition"]
    route.is_call = False
    route.save()
    

