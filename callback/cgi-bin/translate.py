# -*- coding: utf-8 -*-

__author__ = 'jcgregorio@google.com (Joe Gregorio)'

from apiclient.discovery import build
import os, sys
import unicodedata


def main(text):

  if is_russiun(text):
	target_lang = 'ja'
  elif is_japanese(text):
	target_lang = 'ru'
  else:
	target_lang = 'ja'
	

  # Build a service object for interacting with the API. Visit
  # the Google APIs Console <http://code.google.com/apis/console>
  # to get an API key for your own application.
  service = build('translate', 'v2',
            developerKey='AIzaSyBuSULnkiXrBrQ_eMeCAKOdbn0YK0Jv3TI')
  result = service.translations().list(
      source='',
      target=target_lang,
      q=text
    ).execute()

  print result["translations"][0]["translatedText"].encode('utf-8')


def is_russiun(string):
    string = string.replace("'","").decode('utf-8')
    for ch in string:
        name = unicodedata.name(unicode(ch)) 
        if "CYRILLIC" in name:
            return True
    return False


def is_japanese(string):
    string = string.replace("'","").decode('utf-8')
    for ch in string:
        name = unicodedata.name(ch) 
        if "CJK UNIFIED" in name \
        or "HIRAGANA" in name \
        or "KATAKANA" in name:
            return True
    return False


if __name__ == '__main__':

  main(sys.argv[1])

