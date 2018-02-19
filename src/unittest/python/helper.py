from __future__ import absolute_import
import json
import os.path


def alexa_skills_request(json_file):
    return read(find(json_file))


def session(json_file):
    return read(find(json_file))['session']


def request(json_file):
    return read(find(json_file))['request']


def read(json_file):
    with open(json_file) as data_file:
        return json.load(data_file)


def find(json_file):
    prefixes = ["src/unittest/python/sample/", "../sample/", "./sample/"]

    for prefix in prefixes:
        if os.path.isfile(prefix + json_file):
            return prefix + json_file

    raise Exception("File not found: " + json_file)
