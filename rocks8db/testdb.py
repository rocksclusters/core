#!/usr/bin/env python3
from sqlalchemy import create_engine
from sqlalchemy import Table,Column,Integer 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///rocks.db', echo=True)
Base = declarative_base(engine)
########################################################################
class Bootactions(Base): 
     __tablename__ = 'bootactions' 
     __table_args__ = {'autoload':True}
  
class Distributions(Base): 
     __tablename__ = 'distributions' 
     __table_args__ = {'autoload':True}
  
class Netgens(Base): 
     __tablename__ = 'netgens' 
     __table_args__ = {'autoload':True}
  
class Reslevels(Base): 
     __tablename__ = 'reslevels' 
     __table_args__ = {'autoload':True}
  
class Rolls(Base): 
     __tablename__ = 'rolls' 
     __table_args__ = {'autoload':True}
  
class Subnets(Base): 
     __tablename__ = 'subnets' 
     __table_args__ = {'autoload':True}
  
class Vlans(Base): 
     __tablename__ = 'vlans' 
     __table_args__ = {'autoload':True}
  
class Appliances(Base): 
     __tablename__ = 'appliances' 
     __table_args__ = {'autoload':True}
  
class Attrs(Base): 
     __tablename__ = 'attrs' 
     __table_args__ = {'autoload':True}
  
class Firewalls(Base): 
     __tablename__ = 'firewalls' 
     __table_args__ = {'autoload':True}
  
class Nodegroups(Base): 
     __tablename__ = 'nodegroups' 
     __table_args__ = {'autoload':True}
  
class Nodes(Base): 
     __tablename__ = 'nodes' 
     __table_args__ = {'autoload':True}
  
class Partitions(Base): 
     __tablename__ = 'partitions' 
     __table_args__ = {'autoload':True}
  
class Routes(Base): 
     __tablename__ = 'routes' 
     __table_args__ = {'autoload':True}
  
class Bootflags(Base): 
     __tablename__ = 'bootflags' 
     __table_args__ = {'autoload':True}
  
class Groupmembers(Base): 
     __tablename__ = 'groupmembers' 
     __table_args__ = {'autoload':True}
  
class Hwinventory(Base): 
     __tablename__ = 'hwinventory' 
     __table_args__ = {'autoload':True}
  
class Netdevs(Base): 
     __tablename__ = 'netdevs' 
     __table_args__ = {'autoload':True}
  
class Ipaddrs(Base): 
     __tablename__ = 'ipaddrs' 
     __table_args__ = {'autoload':True}
  
class Allattrsview(Base): 
     __table__ = Table( 'allattrsview', Base.metadata, Column('id',Integer, primary_key=True), 
                          autoload=True, autoload_with=engine) 

class Attrsview(Base): 
     __table__ = Table( 'attrsview', Base.metadata, Column('id',Integer, primary_key=True), 
                          autoload=True, autoload_with=engine) 

class Firewallsview(Base): 
     __table__ = Table( 'firewallsview', Base.metadata, Column('id',Integer, primary_key=True), 
                          autoload=True, autoload_with=engine) 

class Groupmembersview(Base): 
     __table__ = Table( 'groupmembersview', Base.metadata, Column('id',Integer, primary_key=True), 
                          autoload=True, autoload_with=engine) 

class Hwinventoryview(Base): 
     __table__ = Table( 'hwinventoryview', Base.metadata, Column('id',Integer, primary_key=True), 
                          autoload=True, autoload_with=engine) 

class Netdevsview(Base): 
     __table__ = Table( 'netdevsview', Base.metadata, Column('id',Integer, primary_key=True), 
                          autoload=True, autoload_with=engine) 

class Nodesview(Base): 
     __table__ = Table( 'nodesview', Base.metadata, Column('id',Integer, primary_key=True), 
                          autoload=True, autoload_with=engine) 

class Partitionsview(Base): 
     __table__ = Table( 'partitionsview', Base.metadata, Column('id',Integer, primary_key=True), 
                          autoload=True, autoload_with=engine) 

class Routesview(Base): 
     __table__ = Table( 'routesview', Base.metadata, Column('id',Integer, primary_key=True), 
                          autoload=True, autoload_with=engine) 

class Vlansview(Base): 
     __table__ = Table( 'vlansview', Base.metadata, Column('id',Integer, primary_key=True), 
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
