#!/bin/bash

for YEAR in `find . -type d -maxdepth 1 -name '2*'` ; do
	cd $YEAR
	for MONTH in `find . -type d -maxdepth 1 -regex '..[0-9][0-9]'` ; do
		cd $MONTH
		if [ -f month.xml ]; then
			echo "Testing $YEAR/$MONTH/month.xml"
			xmllint --noout --dtdvalid ../../month.dtd month.xml
			RC=$?
			if [ $RC -ne 0 ]; then
				echo "Badly formed XML in $YEAR-$MONTH"
				exit 1
			fi
			echo " + conforms to DTD"
			for HREF in `cat month.xml | grep href | grep -v http:// | sed 's/.*href="//' | sed 's/".*//'` ; do
				if [ ! -f "$HREF" ] ; then
					echo " - Referenced file $HREF is missing."
					exit 1
				fi
			done
			echo " + href files exist"
			for HREF in `cat month.xml | grep href | grep http:// | sed 's/.*href="//' | sed 's/".*//'` ; do
                echo " = Note: not checking offsite href $HREF"
            done
		fi
		cd ..
	done
	cd ..
done
