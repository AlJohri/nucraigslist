#!/usr/bin/env python
import os
import sys
import environment
import nltk
nltk.data.path.append('nltk_data')
# http://stackoverflow.com/questions/13965823/resource-corpora-wordnet-not-found-on-heroku

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "freeandforsale.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
