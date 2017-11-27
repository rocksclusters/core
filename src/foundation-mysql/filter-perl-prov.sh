#! /bin/bash
#

/usr/lib/rpm/perl.prov $* |
sed -e 's/perl(/foundation-mysql-perl(/g'

