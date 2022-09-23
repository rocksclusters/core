#!/usr/bin/env python3
from sqlalchemy import create_engine
from sqlalchemy import Table,Column,Integer 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///rocks.db', echo=True)
Base = declarative_base(engine)
########################################################################
class Nodes(Base):
    """"""
    __tablename__ = 'nodes'
    __table_args__ = {'autoload':True}

class Netdevs(Base):
    """"""
    __tablename__ = 'netdevs'
    __table_args__ = {'autoload':True}

class NodesView(Base):
    """"""
    __table__ = Table( 'nodesview', Base.metadata, Column('id',Integer, primary_key=True), 
                         autoload=True, autoload_with=engine)
class NetdevsView(Base):
    """"""
    __table__ = Table( 'netdevsview', Base.metadata, Column('id',Integer, primary_key=True), 
                         autoload=True, autoload_with=engine)


#----------------------------------------------------------------------
def loadSession():
    """"""
    metadata = Base.metadata
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
    
if __name__ == "__main__":
    session = loadSession()
    nodes = session.query(NetdevsView).filter(NetdevsView.node == 'frontend-0-0').all()
    for i in range(0,len(nodes)):
        print (nodes[i].node, nodes[i].device, nodes[i].addr, nodes[i].prefix, nodes[i].mac)
