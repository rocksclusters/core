#!/bin/bash
# Get an object from google drive (shared public)
# usage:
#    gget <objectid> [outputfile]
#
# example:
#    gget 0B0LD0shfkvCRdk1NMVc1NlI2ZUk sage2-1.0.0.tar.bz2
#
CWD=$(pwd)
COOKIE=$(mktemp --tmpdir=$CWD)
TMPFILE=$(mktemp --tmpdir=$CWD)
OBJECT=$1
if [ "x$2" != "x" ]; then
	OUTFILE=$2
else
	OUTFILE=$1
fi

## Retrieve the file
TEMPLATE="https://docs.google.com"
DLPATH="$TEMPLATE/uc?id=$OBJECT&export=download"
wget -O $TMPFILE --save-cookie $COOKIE --load-cookie $COOKIE "$DLPATH"
grep -q "confirm=" $TMPFILE
if [ $? -eq 0 ]; then
## We need to retry the download with the confirm code
	# echo  "Large Download ... retrying"
        REDIRECT=$(grep -o  'href="/uc?[[:alnum:][:punct:]]*confirm[[:alnum:][:punct:]]*"' $TMPFILE | sed -e 's#amp;##g' -e 's#href=##' -e 's#"##g')
	DLPATH="$TEMPLATE$REDIRECT"
	wget -O $TMPFILE --save-cookie $COOKIE --load-cookie $COOKIE "$DLPATH"
fi
mv $TMPFILE $OUTFILE

## Clean up the cookie file
rm $COOKIE






