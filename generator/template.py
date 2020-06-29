#!/usr/bin/env python3

import os


class Template:
    def __init__(self, filename):
        self._here = os.path.dirname(os.path.realpath(__file__))
        self._template_file = os.path.join(self._here, filename)
        assert(os.path.isfile(self._template_file))
        with open(self._template_file, 'r') as f:
            self._template_text = f.read()
        self._text = self._template_text

    def replace(self, key, value):
        # Assumption that a key used later doesn't appear in a value used earlier...
        self._text = self._text.replace('{{' + key + '}}', value)

    def write(self, destination_folder, filename):
        path = os.path.join(destination_folder, filename)
        directory = os.path.dirname(path)
        os.makedirs(directory, exist_ok=True)
        with open(path, 'w') as f:
            f.write(self._text)
        return
