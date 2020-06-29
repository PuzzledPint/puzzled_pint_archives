#!/usr/bin/env python3


class Hint:
    """
    A hint is typically a block of markdown text offering a single hint in a series
    of progressively more revealing hints. Though it could be a link to a file.
    """
    def __init__(self, xml_node):
        self.file = None
        self.text = None
        if xml_node.get('href'):
            self.file = xml_node.get('href').strip()
        else:
            self.text = xml_node.text.strip()


class Puzzle:
    """
    Puzzle contains everything known about an individual puzzle. This includes:
    - title
    - notes — Freeform Markdown text displayed as an intro to the puzzle.
    - file — Path to the PDF or other file.
    - hints — An ordered list of Hint objects.
    - solution_file — Path to the PDF or other file containing the solution.
    - solution_text — Markdown text containing the solution.
    """
    def __init__(self, xml_tree):
        self.title = xml_tree.find('./title').text.strip()
        self.notes = None
        if xml_tree.find('./title'):
            self.notes = xml_tree.find('./notes').text.strip()
        self.file = None
        if xml_tree.find('./file'):
            self.file = xml_tree.find('./file').get('href').strip()
        self.hints = []
        for hint_element in xml_tree.findall('./hint'):
            self.hints.append(Hint(hint_element))
        self.solution_file = None
        self.solution_text = None
        if xml_tree.find('./solution').get('href'):
            self.solution_file = xml_tree.find('./solution').get('href')
        else:
            self.solution_text = xml_tree.find('./solution').text.strip()
        print('Parsing puzzle {0}'.format(self.title))

    def debug_print(self):
        print("        {0}".format(self.title))
        print("        {0}".format(str(self.notes)[0:40].replace("\n", "")))
