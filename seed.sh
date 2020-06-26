#!/bin/bash

XMLSTAR=`which xmlstarlet`

if [ -z "$XMLSTAR" ]; then
    echo "The xmlstarlet application is required to run this script."
    exit 1
fi

if [ -z "$2" ]; then
    echo "Place year and month on command line"
    echo "Example: ./seed.sh 2020 07"
    exit 1
fi

FOLDER="$1/$2"
mkdir -p "$FOLDER"
cp sample_month.xml "$FOLDER/month.xml"
xmlstarlet ed --pf  -u /PPMonth/year --value "$1" "$FOLDER/month.xml" > "$FOLDER/month2.xml"
mv "$FOLDER/month2.xml" "$FOLDER/month.xml"
xmlstarlet ed --pf  -u /PPMonth/month --value "$2" "$FOLDER/month.xml" > "$FOLDER/month2.xml"
mv "$FOLDER/month2.xml" "$FOLDER/month.xml"
