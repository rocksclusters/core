#!/bin/bash 
# Tutorial https://www.daimto.com/how-to-get-a-google-access-token-with-curl/
# YouTube video https://youtu.be/hBC_tVJIx5w
# Client id from Google Developer console
# Client Secret from Google Developer console
# Scope this is a space seprated list of the scopes of access you are requesting.

# Authorization link.  Place this in a browser and copy the code that is returned after you accept the scopes.
# 

# Environment Variables
#  GSAPICLIENTCONF - File that hold Services configuration
#  TOKENFILE - name of file that hold the token information
#  
# Format of GSAIPCLIENTCONF
# CLIENT_ID="<id from google developers console>"
# CLIENT_SECRET="<generated password from google developers console>"

if [[ "${TOKENFILE-x}" == "x" ]]; then echo "Please define TOKENFILE"; exit -2; fi
if [[ "${GSAPICLIENTCONF-x}" == "x" ]]; then echo "Please define GSAPICLIENTCONF"; exit -2; fi

source ${GSAPICLIENTCONF}
echo "You will grant 'read-only' download access to your Google drive. The companion"
echo "gget.sh only downloads from known google file IDs, and cannot discover any of your drive data"
echo -e "\nAsking Firefox to open the following URL into your browser to authenticate to Google:\n"
echo "https://accounts.google.com/o/oauth2/auth?client_id=${CLIENT_ID}&redirect_uri=http://localhost:9000&scope=https://www.googleapis.com/auth/drive.readonly&response_type=code"
firefox "https://accounts.google.com/o/oauth2/auth?client_id=${CLIENT_ID}&redirect_uri=http://localhost:9000&scope=https://www.googleapis.com/auth/drive.readonly&response_type=code" &

## Start the local webserver
MY_PATH=$(dirname "$0")
AUTHCODE=$(python3 ${MY_PATH}/webserver.py)

# read -p "Paste the provided authentication code: " AUTHCODE

# 
echo -e "\nNow generating your access and refresh tokens. These will be stored in the file"
echo "  ${TOKENFILE}"

# Exchange Authorization code for an access token and a refresh token.
curl \
--request POST \
--data "code=${AUTHCODE}&client_id=${CLIENT_ID}&client_secret=${CLIENT_SECRET}&redirect_uri=http://localhost:9000&grant_type=authorization_code" \
https://accounts.google.com/o/oauth2/token | grep _token | sed -e 's/ //g' -e 's/:/=/' -e 's/,$//' -e 's/"//' -e 's/"//' | tee ${TOKENFILE}  


#read -p "Cut and paste the refresh token: " REFRESH 
# Exchange a refresh token for a new access token.
#curl \
#--request POST \
#--data "client_id=${CLIENT_ID}&client_secret=${CLIENT_SECRET}&refresh_token=${REFRESH}&grant_type=refresh_token" \
#https://accounts.google.com/o/oauth2/token
