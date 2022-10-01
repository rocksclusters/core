#!/bin/bash
SCHEMA=new-rocks-schema.sql
TABLETEMPLATE="\
class %s(Base): \n \
    __tablename__ = '%s' \n \
    __table_args__ = {'autoload':True}\n  
"
VIEWTEMPLATE="\
class %s(Base): \n \
    __table__ = Table( '%s', Base.metadata, Column('id',Integer, primary_key=True), \n \
                         autoload=True, autoload_with=engine) \n
"
for t in $(grep "CREATE TABLE" $SCHEMA  | awk -F TABLE '{print $NF}' | awk '{print $1}'); do
  T=$(echo "$t" | sed 's/./\u&/')
  printf "$TABLETEMPLATE" "$T" "$t"
done
for t in $(grep "CREATE VIEW" $SCHEMA  | awk -F VIEW '{print $NF}' | awk '{print $1}'); do
  T=$(echo "$t" | sed 's/./\u&/')
  printf "$VIEWTEMPLATE" "$T" "$t"
done
