#!/usr/bin/env python3

import os
import re
import sys
import xml.etree.ElementTree as ET
from puzzle import Puzzle


class Month:
    def __init__(self, month_directory):
        print("Loading {0}".format(month_directory))
        tree = ET.parse(os.path.join(month_directory, 'month.xml'))
        root = tree.getroot()
        self.folder = month_directory
        self.year = root.find('./year').text.strip()
        self.month = root.find('./month').text.strip()
        self.title = root.find('./title').text.strip()
        self.icon = root.find('./icon').get('href').strip()
        self.notes = None
        if root.find('./notes'):
            self.notes = root.find('./notes').text.strip()
        self.location_answer_word = root.find('./location/answerword').text.strip().lower()
        self.location_puzzle = Puzzle(root.find('./location/puzzle'))
        self.puzzles = []
        for puzzle_element in root.findall('./puzzle'):
            self.puzzles.append(Puzzle(puzzle_element))
        self.all_puzzles = None
        self.answer_sheet = None
        self.answer_sheet_solutions = None
        if root.find('./allPuzzles'):
            self.all_puzzles = root.find('./allPuzzles').get('href').strip()
        if root.find('./answerSheet'):
            self.answer_sheet = root.find('./answerSheet').get('href').strip()
        if root.find('./answerSheetSolution'):
            self.answer_sheet_solutions = root.find('./answerSheetSolution').get('href').strip()


class Months:
    def __init__(self, top_directory, year):
        self._months = {}
        self._top_directory = top_directory
        self._year = int(year)
        self._load_months_from_disk()

    def _load_months_from_disk(self):
        months = []
        month_regex = re.compile('^[0-9]{2}$')
        year_directory = os.path.join(self._top_directory, str(self._year))
        subfolders = [f for f in os.listdir(year_directory) if os.path.isdir(os.path.join(year_directory, f))]
        for subfolder in subfolders:
            if month_regex.match(subfolder) is not None:
                months.append(subfolder)
        months = sorted(months)
        for month in months:
            self._months[int(month)] = Month(os.path.join(year_directory, month))
        pass

    def first_month(self):
        months = sorted(self._months.keys())
        if len(months) == 0:
            return 0
        return months[0]

    def last_month(self):
        months = sorted(self._months.keys())
        if len(months) == 0:
            return 0
        return months[-1]


class Years:
    def __init__(self, top_directory):
        self._years = {}
        self._top_directory = top_directory
        self._load_years_from_disk()

    def _load_years_from_disk(self):
        years = []
        year_regex = re.compile('^[0-9]{4}$')
        subfolders = [f for f in os.listdir(self._top_directory) if os.path.isdir(os.path.join(self._top_directory, f))]
        for subfolder in subfolders:
            if year_regex.match(subfolder) is not None:
                years.append(subfolder)
        years = sorted(years)
        for year in years:
            self._years[int(year)] = Months(self._top_directory, int(year))
        pass

    def first_year(self):
        years = sorted(self._years.keys())
        if len(years) == 0:
            return 0
        return years[0]

    def last_year(self):
        years = sorted(self._years.keys())
        if len(years) == 0:
            return 0
        return years[-1]