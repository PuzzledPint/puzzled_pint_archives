#!/usr/bin/env python3

import markdown # pip3 install markdown
import os
import sys

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
        month_names = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June',
                       7:'July', 8:'August', 9:'September', 10:'October', 11:'November', 12:'December'}
        for year in self._all_years.years():
            months_object = self._all_years.months(year)
            months = months_object.months()
            for month in months:
                m = months_object.month(month)
                month_folder = os.path.join(self._destination_folder, m.year, "{0:02d}".format(int(m.month)))
                print("Generating {year}-{month:02d}\n".format(year=m.year, month=int(m.month)))
                template = Template('month.html')
                template.replace('title', m.title)
                template.replace('year', m.year)
                template.replace('month', "{0:02d}".format(int(m.month)))
                template.replace('month_name', month_names[int(m.month)])
                template.replace('notes', markdown.markdown(normalize(m.notes)))
                template.replace('location_title', normalize(m.location_puzzle.title))
                template.replace('location_notes', markdown.markdown(normalize(m.location_puzzle.notes)))
                if m.location_puzzle.solution_file is not None:
                    template.replace('location_solution', m.location_puzzle.solution_file)
                else:
                    pass # TODO: implement solution text
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

                # TODO: Write location.html

