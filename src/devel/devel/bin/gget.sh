#!/bin/bash
# Get an object from google drive (shared public, or any ID where the authenticated user has
# access.) 
#
# 
# usage:
#    gget.sh <objectid> [outputfile]
#	 if outputfile is not specified, the objectid is the outputfile
#
# requires:
#	curl
#
# Environment Variables
#    TOKENFILE - file that contents of user tokens 
#    GSAPICLIENTCONF - file that has the configuration of the google service to utilize. User needs
#    to have authenticated to this service using get-token.sh
#
# Contents of GSAPICLIENTCONF
# CLIENT_ID=
# CLIENT_SECRET=
#
# Contents of TOKENFILE (written with get-token.sh)
# access_token=
# refresh_token=
#
# example:
#    gget.sh 0B0LD0shfkvCRdk1NMVc1NlI2ZUk sage2-1.0.0.tar.bz2
#
# Note: this object has sha1sum
#    783ac71f01bde1c2d4abedf06cf43f99745e1d16  sage2-1.0.0.tar.bz2
#

## Clean up any left-overs
function cleanup
{
	if [ -f $TMPFILE ]; then
		/bin/rm $TMPFILE
	fi
}
trap cleanup EXIT


## Check files and source
if [[ ! -f  ${TOKENFILE} ]]; then echo "Cannot open TOKENFILE \'$TOKENFILE\'"; exit -1; fi
if [[ ! -f  ${GSAPICLIENTCONF} ]]; then echo "Cannot open GSAPICLIENTCONF \'$GSAPICLIENTCONF\'"; exit -1; fi

source $TOKENFILE
source $GSAPICLIENTCONF
### Download 
CWD=$(pwd)
TMPFILE=$(mktemp --tmpdir=$CWD)
OBJECT=$1
if [ "x$2" != "x" ]; then
	OUTFILE=$2
else
	OUTFILE=$1
fi

## Retrieve the file

if [[ "${access_token-x}" == "x" ]]; then echo TOKENFILE must define access_token; exit -2; fi

ENDPOINT=https://www.googleapis.com/drive/v3/files
DLPARAMS="?&alt=media&client_id=${CLIENTID}"
DLPATH="$ENDPOINT/${OBJECT}${DLPARAMS}"
TRIES=2
ERRNO=0
while [ $TRIES -gt 0 ]; do
   let TRIES=TRIES-1
   HEADER="Authorization: Bearer ${access_token}"
   echo "$HEADER"
   echo "$DLPATH"
   curl -f -H "${HEADER}" -o $TMPFILE "$DLPATH" 
   ## Handle the case where curl returned an and attempt a refresh token 
   ERRNO=$?
   if [ $ERRNO -ne 0 ]; then
      echo "Exchanging a refresh token for a new access token."
      access_token=$(curl \
      --request POST \
      --data "client_id=${CLIENT_ID}&client_secret=${CLIENT_SECRET}&refresh_token=${refresh_token}&grant_type=refresh_token" \
      https://accounts.google.com/o/oauth2/token | grep access_token | sed -e 's/ //'g -e 's/,$//' | cut -d : -f 2) 
      echo "saving new access token: ${access_token} to ${TOKENFILE}"
      echo "access_token=${access_token}" > $TOKENFILE
      echo "refresh_token=${refresh_token}" >> $TOKENFILE
   else
     TRIES=0
   fi
done
if [ $ERRNO -ne 0 ]; then echo "Failed to download file $OUTFILE"; exit $ERRNO; fi

mv $TMPFILE $OUTFILE
