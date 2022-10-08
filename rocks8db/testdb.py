#!/usr/bin/env python3
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select

from mapping import *
from database import *
if __name__ == "__main__":
    db = Database()
    db.setVerbose(True)
    db.connect()
    print (db)
    TAV=t_attrsview
    query = select([TAV.c.attr,TAV.c.value,TAV.c.resname]).where(TAV.c.reskey == "compute-0-2")

    for a in db.engine.execute(query).fetchall():
        print (a)
    #for i in range(0,len(attrs)):
    #    print (attrs[i].node, attrs[i].attr, attrs[i].value, attrs[i].shadow, attrs[i].resname,attrs[i].level)
