#!/bin/bash
# Download packages and install rpms into a particular root directory
# getrpms.sh  <ROOT> <PKG1> [<PKG2>] ....
ROOT=$1
ARCH=$(/bin/arch)
shift
yumdownloader --destdir=. $*
RPMS=`/bin/ls *rpm | grep $ARCH`
/bin/rpm -ivh --force --relocate /=$ROOT --badreloc $RPMS 
