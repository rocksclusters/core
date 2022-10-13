#!/usr/bin/env python3
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select
from sqlalchemy import or_, and_

from mapping import *
from database import *
if __name__ == "__main__":
    db = Database()
    db.setVerbose(True)
    db.connect()
    session = db.getSession()
    print (db)
    TAV=t_attrsview
    query = select([TAV.c.attr,TAV.c.value,TAV.c.resname]).where(TAV.c.reskey == "compute-0-2")

    for a in db.engine.execute(query).fetchall():
        print (a)

    node = Node.loadOne(session, name='compute-0-0')

    # Let's add a node to the cluster called compute-1-0
    caid = Appliance.loadOne(session,name='compute').ID
    cnode = Node(name='compute-1-0',rack=1,rank=0,boot='install',appliance=caid)
    print ("adding node to db")
    session.add(cnode)
    print ("committing changes")
    session.commit()

    #for i in range(0,len(attrs)):
    #    print (attrs[i].node, attrs[i].attr, attrs[i].value, attrs[i].shadow, attrs[i].resname,attrs[i].level)
