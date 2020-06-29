#!/usr/bin/env python3

import os
import re
import sys
import xml.etree.ElementTree as ET
from puzzle import Puzzle


class Month:
    """
    A month represents all resources for a given month's Puzzled Pint event. This includes:
    - folder : The folder housing all of this month's resources.
    - year : The year of this month's event.
    - month : The month of this event.
    - title : The title of this event.
    - icon : Path to an icon file for the month. Typically referred to as “The Polaroid.”
    - notes : Freeform Markdown introducing the month, the author(s), and anything else relevant to a solver.
    - location_puzzle : A Puzzle object representing the location puzzle.
    - location_answer_word : The solution to the location puzzle (all lowercase, stripped of all but letters+numbers).
    - puzzles : An ordered array of Puzzle objects representing that month's puzzles, meta, bonus, etc.
    - all_puzzles : File path to a PDF containing “all puzzles” (frequently absent the bonus, sometimes absent the meta).
    - answer_sheet : File path to a PDF of the answer sheet for that month.
    - answer_sheet_solutions : File path to a PDF of the answer sheet with solutions filled in (rarely seen)
    """
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
        if root.find('./notes') is not None:
            self.notes = root.find('./notes').text.strip()
        self.location_answer_word = root.find('./location/answerword').text.strip().lower()
        self.location_puzzle = Puzzle(root.find('./location/puzzle'))
        self.puzzles = []
        for puzzle_element in root.findall('./puzzle'):
            self.puzzles.append(Puzzle(puzzle_element))
        self.all_puzzles = None
        self.answer_sheet = None
        self.answer_sheet_solutions = None
        if root.find('./allPuzzles') is not None:
            self.all_puzzles = root.find('./allPuzzles').get('href').strip()
        if root.find('./answerSheet') is not None:
            self.answer_sheet = root.find('./answerSheet').get('href').strip()
        if root.find('./answerSheetSolution') is not None:
            self.answer_sheet_solutions = root.find('./answerSheetSolution').get('href').strip()

    def debug_print(self):
        print("    {0}-{1} : {2} : {3}".format(self.year, self.month, self.title, self.icon))
        print("    {0}...".format(str(self.notes)[0:30].replace("\n", "")))
        self.location_puzzle.debug_print()
        for puzzle in self.puzzles:
            puzzle.debug_print()


class Months:
    """
    A collection of all `Month` objects for a given year.
    """
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
            if not (self._year == 2011 and month == '07'): # Delete me and fix month.xml for this month.
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

    def debug_print(self):
        for key in sorted(self._months.keys(), reverse=True):
            self._months[key].debug_print()


class Years:
    """
    A collection of all years of events, each mapped to a `Months` collection for that given year.
    """
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

    def debug_print(self):
        for key in sorted(self._years.keys(), reverse=True):
            print("{0}".format(key))
            self._years[key].debug_print()