#!/bin/bash
## This file repacks a restore roll created on 6 and makes is compatible for
## 7.  It also removes creation of /etc/pki files since (policywise) these 
## are not compatible with 7.
## 
ISONAME=$1
VERSION_MK=version.mk
LISTISOFILES=/opt/rocks/sbin/listisofiles
SRCDIR=src
AWKPROG=awk.prog
RPMFILES=rpmfiles
FILESLIST=fileslist


function packrpm() {
	rpmname=$1
	if [ -d ${SRCDIR} ]; then 
		/bin/rm -rf ${SRCDIR}
	fi
	mkdir ${SRCDIR}

## Create a version file for this RPM
	cat > ${SRCDIR}/${AWKPROG} << 'EOF'
/^Name/{print "NAME = " $NF} 
/^Version/{print "VERSION = " $NF} 
/^Release/ {print "RELEASE = " $NF} 
/^Relocat/ {  if (index($0,"(not") == 0) 
		 print "RPM.EXTRAS = Prefix: ",$NF}
EOF

## Create a Makefile to remake this RPM
	cat > ${SRCDIR}/Makefile << 'EOF2'
REDHAT.ROOT     = $(CURDIR)/..
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk
RAWFILES=$(shell find rpmfiles -type f)

build:
	( for f in $(RAWFILES); do  \
		/bin/sed -i -e "s/<file name=\".*pki.*\/>//"  -e "s/touch.*pem//" $$f; \
	done; \
	)
install::
	(cd rpmfiles; tar cf - *) | (cd $(ROOT); tar xvf -)
EOF2
	if [ -d ${SRCDIR}/${RPMFILES} ]; then /bin/rm -rf ${SRC}/${RPMFILES}; fi 
	mkdir -p ${SRCDIR}/${RPMFILES}
	rpm2cpio $rpmname | (cd ${SRCDIR}/${RPMFILES}; cpio -i --make-directories )
	name=$(rpm -qip $rpmname | awk '/Name/{print $3}') 
	if [ ! -d RPMS/x86_64 ]; then mkdir -p RPMS/x86_64; fi
	rpm -qip $rpmname | awk -f ${SRCDIR}/${AWKPROG} > ${SRCDIR}/${VERSION_MK}
	echo "RPM.FILESLIST = ${FILESLIST}" >> ${SRCDIR}/${VERSION_MK}
	echo "" >> ${SRCDIR}/${VERSION_MK}
	find ${SRCDIR}/${RPMFILES} -type f | sed -e "s#${SRCDIR}/${RPMFILES}##"  >> ${SRCDIR}/${FILESLIST}
	echo "" >> ${SRCDIR}/${FILESLIST}
	echo "Repacking RPM: $rpmname"
	make -C src rpm
}

TEMPDIR=$(mktemp -d)
echo /bin/cp $ISONAME $TEMPDIR
/bin/cp $ISONAME $TEMPDIR
SHORTISONAME=$(basename $ISONAME)
SHORTISOBASENAME=$(basename -s .iso $SHORTISONAME) 
CWD=$(pwd)
pushd $TEMPDIR
for f in `$LISTISOFILES $SHORTISONAME`; do
	echo $f
	fname=$(basename $f)
	iso-read -e $f -i $1 -o $fname
	echo $fname | grep -q 'rpm$'
	if [ $? -eq 0 ]; then
		packrpm $fname
	fi
done
ROLLXML=roll*xml
if [ -f $ROLLXML ]; then
	mv ${SHORTISONAME} ${SHORTISONAME}.orig
	rocks create roll $ROLLXML
	mv ${SHORTISONAME} ${CWD}/${SHORTISOBASENAME}.repacked.iso
fi
popd
echo $TEMPDIR

