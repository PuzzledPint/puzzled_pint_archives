#!/usr/bin/env python3

import markdown # pip3 install markdown
import os

from month import Years, Months, Month
from template import Template


def normalize(s):
    if s is not None:
        return s
    return ''


class GeneratorYear:
    def __init__(self, source_folder, destination_folder, years):
        self._source_folder = source_folder
        self._destination_folder = destination_folder
        self._all_years = years

    def generate(self):
        self._generate_index()
        self._copy_content()

    def _generate_index(self):
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

    def _copy_content(self):
        print("Copying content\n")
        command = "cp -r {0}/???? {1}".format(self._source_folder, self._destination_folder)
        os.system(command)

