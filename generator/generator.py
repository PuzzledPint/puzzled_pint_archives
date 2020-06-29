#!/usr/bin/env python3

import os
import sys

from month import Years, Months, Month
from puzzle import Puzzle

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

all_years = Years(source_folder)
all_years.debug_print()