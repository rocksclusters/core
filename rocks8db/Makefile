ROCKSDB=$(PWD)/rocks8.db
SCHEMA=$(PWD)/new-rocks-schema.sql
TESTDATA=$(PWD)/populate.txt


initialize:
	cat $(SCHEMA) | sqlite3 $(ROCKSDB)
	cat $(TESTDATA) | sqlite3 $(ROCKSDB)

clean:
	- /bin/rm $(ROCKSDB)
