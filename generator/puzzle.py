#!/usr/bin/env python3


class Puzzle:
    def __init__(self, xml_tree):
        self.title = xml_tree.find('./title').text.strip()
        self.notes = None
        if xml_tree.find('./title'):
            self.notes = xml_tree.find('./notes').text.strip()
        self.file = None
        if xml_tree.find('./file'):
            self.file = xml_tree.find('./file').get('href').strip()
        self.hints = []
        # TODO: Parse all the hints which could be text or href
        if xml_tree.find('./solution').get('href'):
            self.solution = xml_tree.find('./solution').get('href')
        else:
            self.solution = xml_tree.find('./solution').text.strip()
        print('Parsing puzzle {0}'.format(self.title))
