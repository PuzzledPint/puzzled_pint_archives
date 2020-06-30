#!/usr/bin/env python3

import os
import sys

from month import Years, Months, Month
from puzzle import Puzzle
from template import Template

if len(sys.argv) != 3:
    print("Put source folder and destination folder on command line.")
    print("Example: ./generator.py .. ../static")
    sys.exit(1)

source_folder = sys.argv[1]
destination_folder = sys.argv[2]

# Validate source.
if not os.path.isdir(source_folder):
    print("Source folder must be a directory")
    sys.exit(1)
if not os.path.isdir(os.path.join(source_folder, '2010')):
    print("Source folder does not appear to be correct. It needs to contain year subfolders.")
    sys.exit(1)

# Validate destination.
if not os.path.exists(destination_folder):
    os.mkdir(destination_folder)
if not os.path.isdir(source_folder):
    print("Destination folder must be a directory")
    sys.exit(1)


def normalize(s):
    if s is not None:
        return s
    return ''


class Generator:
    def __init__(self, source_folder, destination_folder):
        self._source_folder = source_folder
        self._destination_folder = destination_folder
        self._all_years = Years(source_folder)
        #self._all_years.debug_print()

    def generate_year_page(self):
        text = ''
        for year in self._all_years.years():
            months_object = self._all_years.months(year)
            months = months_object.months()
            text += R"""<div class="year-wrapper">"""
            text += R"""<h1 class="year">{0}</h1>""".format(year)
            text += R"""<div class="month-wrapper">"""
            for month in months:
                month_object = months_object.month(month)
                text += r"""<div class="month">
<a href="{year}/{month:02d}/index.html">
<img src="{year}/{month:02d}/{icon}" class="month-image" alt="{title}"/>
<div class="title">{title}</div>
<div class="date">{year}-{month:02d}</div>
</a>
</div>""".format(year=month_object.year,
                 month=int(month_object.month),
                 icon=month_object.icon,
                 title=month_object.title)
            text += "</div><!-- month-wrapper -->\n\n"
            text += "</div><!-- year-wrapper -->\n\n"
            text += "<div class=\"year-separator\"></div>\n\n"
        print("Generating year archive page\n")
        template = Template('years.html')
        template.replace('years', text)
        template.write(self._destination_folder, 'index.html')

    def copy_content(self):
        print("Copying content\n")
        command = "cp -r {0}/???? {1}".format(self._source_folder, self._destination_folder)
        os.system(command)

    def generate_month_pages(self):
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
                # TODO: Markdown!
                template.replace('notes', normalize(m.notes).replace("\n", "<br/>\n"))
                template.replace('location_title', normalize(m.location_puzzle.title))
                template.replace('location_notes', normalize(m.location_puzzle.notes))
                template.replace('location_solution', m.location_puzzle.solution_file)
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


generator = Generator(source_folder, destination_folder)
generator.generate_year_page()
#generator.copy_content()
generator.generate_month_pages()
