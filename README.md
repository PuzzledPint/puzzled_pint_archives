#Puzzled Pint Puzzle Archive Format

##Folders

Each month is in a folder: {4 digit year}/{two digit month}/

##month.xml

Each month folder holds a `month.xml` file. This describes the following:

- The month and its description.
- Informational text about the month (theme, authors, etc.)
- All puzzles, including location.
- Location puzzle answer word.
- Hints, if available.
- Answer sheet, if available.

They should all conform to the top level `month.dtd`. Look at the comments there for more info. A `sample_month.xml` file lives at the top level as an example to copy when adding new months.

##Validation

Run the top level `test.sh` script and this will spider into each year/month folder and:

- Validate the XML against the DTD using xmllint.
- Validate that any `href` attributes point to real files.
- Warn of any `href` attributes that point to external domains.

##Assorted Notes

Text fields should be considered [Github-flavored markdown](https://help.github.com/articles/github-flavored-markdown/). They
occasionally make use of links, bold, italics, tables, and occasional code-blocks.

The hint file `./2015/06/00-location-hint1.html` hotlinks images on snout.org.
