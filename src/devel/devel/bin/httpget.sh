#!/bin/bash
# Get file from URL using curl 
# usage:
#    httpget.sh [-B baseurl] [-F Folder] -n <filename>  [-o outputfile]
#	 if outputfile is not specified, the filename is the outputfile
#
# requires:
#	curl
#	grep
#	sed
#
# example:
#   ./httpget.sh -B https://s3.us-west-1.wasabisys.com/admix-sources -F rust-admix -n rustc-1.62.0-src.tar.gz 
#
# Note: this object has sha1sum
#    995429ede16c4b6c1f193819a3a6ae0037486c2e  rustc-1.62.0-src.tar.gz
#

## Clean up any left-overs
function cleanup
{
	if [ -f $COOKIE ]; then
		/bin/rm $COOKIE
	fi
	if [ -f $TMPFILE ]; then
		/bin/rm $TMPFILE
	fi
}
trap cleanup EXIT
#!/bin/bash

CWD=$(pwd)
COOKIE=$(mktemp --tmpdir=$CWD)
TMPFILE=$(mktemp --tmpdir=$CWD)

BASEURL=https://sources.rocksclusters.org
FOLDER=core
FILENAME=""
OUTFILE=""
while getopts 'B:F:n:o:' OPTION; do
  case "$OPTION" in
    B)
      BASEURL="$OPTARG"
      ;;

    F)
      FOLDER="$OPTARG"
      ;;

    n)
      FILENAME="$OPTARG"
      ;;

    o)
      OUTFILE="$OPTARG"
      ;;
    ?)
      echo "Usage: $(basename $0) [-B baseurl] [-F folder] -n filename [ -o outputfile]"
      exit 1
      ;;
  esac

done
# Parse Arguments
### Download 
if [ "x$FILENAME" == "x" ]; then
        >&2 echo "Filename not specified with -n arg" 
        exit 1
fi
if [ "x$OUTFILE" == "x" ]; then
	OUTFILE=$FILENAME
fi
echo "$BASEURL/$FOLDER/$FILENAME  --> $OUTFILE"

## Retrieve the file
DLPATH="$BASEURL/$FOLDER/$FILENAME"
#wget -O $TMPFILE --save-cookie $COOKIE --load-cookie $COOKIE "$DLPATH"
curl --remote-time -f --cookie-jar $COOKIE -o $TMPFILE -L "$DLPATH" 
## Handle the case where curl returned an error
if [ $? -ne 0 ]; then
	exit $?
fi

OUTDIR=$(dirname $OUTFILE)
if [ ! -d $OUTDIR ]; then mkdir -p $OUTDIR; fi
mv $TMPFILE $OUTFILE
