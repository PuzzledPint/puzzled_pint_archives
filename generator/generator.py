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
            for month in months:
                month_object = months_object.month(month)
                text += r"""<div class="month">
<a href="{year}/{month}">
<img src="{year}/{month}/{icon}" class="month-image"/>
<div class="title">{title}</div>
<div class="date">{year}-{month}</div>
</a>
</div>""".format(year=month_object.year,
                 month=month_object.month,
                 icon=month_object.icon,
                 title=month_object.title)
            text += "</div><!-- year-wrapper -->\n\n"
        print("Generating year archive page\n")
        template = Template('years.html')
        template.replace('years', text)
        template.write(self._destination_folder, 'index.html')

    def copy_content(self):
        print("Copying content\n")
        command = "cp -r {0}/???? {1}".format(self._source_folder, self._destination_folder)
        os.system(command)

    def generate_month_pages(self):
        print("Generating month pages\n")
        pass


generator = Generator(source_folder, destination_folder)
generator.generate_year_page()
generator.copy_content()
generator.generate_month_pages()
