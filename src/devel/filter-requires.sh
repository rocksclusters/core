#! /bin/bash
#
# remove requirement that rocks-devel requires /opt/rocks/python
# this is for bootstrapping
logger -t build "Args to filter-requires: $*"
output=`/usr/lib/rpm/find-requires $* | sed -e '/\/opt\/rocks/d' -e '/\/bin\/python/d'` 
logger -t filter $output
echo -n $output

