#!/usr/bin/env python3

import hashlib
import markdown # pip3 install markdown
import os
import re

from month import Years, Months, Month
from puzzle import Puzzle
from template import Template


def normalize(s):
    if s is not None:
        return s
    return ''


class GeneratorMonth:
    def __init__(self, source_folder, destination_folder, year):
        self._source_folder = source_folder
        self._destination_folder = destination_folder
        self._all_years = year

    def generate(self):
        for year in self._all_years.years():
            months_object = self._all_years.months(year)
            months = months_object.months()
            for month in months:
                m = months_object.month(month)
                month_folder = os.path.join(self._destination_folder, m.year, "{0:02d}".format(int(m.month)))
                print("Generating {year}-{month:02d}\n".format(year=m.year, month=int(m.month)))
                template = Template('month.html')
                template.replace('notes', markdown.markdown(normalize(m.notes)))
                self._set_basic_template_parameters(template, m)
                if m.location_puzzle.solution_file is not None:
                    template.replace('location_solution', m.location_puzzle.solution_file)
                else:
                    self._generate_location_solution(m, month_folder)
                    template.replace('location_solution', '00-location-solution.html')
                if m.answer_sheet is not None:
                    template.replace('answer_sheet', "<li><a href=\"{0}\">Answer Sheet</a> (to collect your answers)</li>\n".format(m.answer_sheet))
                else:
                    template.replace('answer_sheet', '')
                if m.all_puzzles is not None:
                    template.replace('all_puzzles', "<li><a href=\"{0}\">All puzzles in one pdf</a></li>\n".format(m.all_puzzles))
                else:
                    template.replace('all_puzzles', '')
                if m.answer_sheet_solutions is not None:
                    template.replace('answer_sheet_solved', "<li><a href=\"{0}\">Filled-in answer sheet</a></li>\n".format(m.answer_sheet_solutions))
                else:
                    template.replace('answer_sheet_solved', '')
                template.write(month_folder, 'index.html')
                self._generate_location(m, month_folder)

                # TODO: Write location.html

    def _generate_location_solution(self, m, month_folder):
        template = Template('location-solution.html')
        self._set_basic_template_parameters(template, m)
        template.replace('notes', markdown.markdown(normalize(m.location_puzzle.solution_text)))
        template.write(month_folder, '00-location-solution.html')

    def _generate_location(self, m, month_folder):
        puzzle = m.location_puzzle
        template = Template('location.html')
        self._set_basic_template_parameters(template, m)
        template.replace('puzzle_link', normalize(puzzle.file))
        template.replace('puzzle_title', normalize(puzzle.title))
        if puzzle.notes is not None:
            template.replace('notes', markdown.markdown(puzzle.notes.strip()) + '<br /><br />')
        else:
            template.replace('notes', '')
        hints = ''
        for hint in puzzle.hints:
            if hint.text is not None:
                hints += "<li><span class=\"clickme\">Click to reveal.</span><span class=\"text\">{0}</span></li>\n".format(hint.text)
            else:
                hints += "<li><span class=\"clickme\">Click to reveal.</span><span class=\"text\"><a href=\"{0}\">{0}</a></span></li>\n".format(hint.file)
        template.replace('hints', hints)
        answer_word = m.location_answer_word.lower()
        answer_word = re.sub('[^a-z]', '', answer_word)
        template.replace('answer_hash', hashlib.md5(answer_word.encode('utf-8')).hexdigest())
        template.write(month_folder, 'location.html')

    def _set_basic_template_parameters(self, template, m):
        month_names = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June',
                       7:'July', 8:'August', 9:'September', 10:'October', 11:'November', 12:'December'}
        template.replace('title', m.title)
        template.replace('year', m.year)
        template.replace('month', "{0:02d}".format(int(m.month)))
        template.replace('month_name', month_names[int(m.month)])
        template.replace('location_title', normalize(m.location_puzzle.title))
        template.replace('location_notes', markdown.markdown(normalize(m.location_puzzle.notes)))

