ROCKSDB=$(PWD)/rocks8.db
SCHEMA=$(PWD)/new-rocks-schema.sql
TESTDATA=$(PWD)/populate.txt
MAPPINGWRAPPER = mappingwrapper.py
MAPPING = mapping.py


$(ROCKSDB): $(SCHEMA)
	cat $(SCHEMA) | sqlite3 $(ROCKSDB)

initialize: $(ROCKSDB)
	cat $(TESTDATA) | sqlite3 $(ROCKSDB)

$(MAPPING): $(ROCKSDB) $(MAPPINGWRAPPER)
	echo '#! /usr/bin/env python3' > $@
	echo '# generated with sqlacodegen' >> $@
	echo '# class RocksBase added an then sqlacodegen classes modified' >> $@
	sqlacodegen sqlite:///$(ROCKSDB) | sed -e 's/(Base)/(RocksBase, Base)/' -e "/^Base/r $(MAPPINGWRAPPER)" >> $@

clean:
	- /bin/rm $(ROCKSDB) $(MAPPING)
