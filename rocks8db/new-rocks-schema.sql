CREATE TABLE bootactions ( 
	ID                   INTEGER NOT NULL  PRIMARY KEY  ,
	action               VARCHAR(128)     ,
	kernel               VARCHAR(256)     ,
	ramdisk              VARCHAR(256)     ,
	Flags                VARCHAR(1025)     
 );

CREATE TABLE firewalls ( 
	ID                   INTEGER NOT NULL  PRIMARY KEY  ,
	Rulename             VARCHAR(128) NOT NULL    ,
	Rulesrc              VARCHAR(16) NOT NULL    ,
	InSubnet             INTEGER     ,
	OutSubnet            INTEGER     ,
	Service              VARCHAR(256)     ,
	Protocol             VARCHAR(256)     ,
	Action               VARCHAR(256)     ,
	Chain                VARCHAR(256)     ,
	flags                VARCHAR(256)     ,
	Comment              VARCHAR(256)     ,
	reslevel             INTEGER     ,
	reskey               VARCHAR(256)     ,
	CONSTRAINT unq_firewalls UNIQUE ( reslevel, Rulename, reskey )
 );

CREATE TABLE ipaddrs ( 
	ID                   INTEGER NOT NULL  PRIMARY KEY  ,
	netdev               INTEGER NOT NULL    ,
	addr                 VARCHAR(256)     ,
	subnet               INTEGER     
 );

CREATE TABLE netdevs ( 
	ID                   INTEGER NOT NULL  PRIMARY KEY  ,
	device               VARCHAR(128)     ,
	mac                  VARCHAR(128)     ,
	module               VARCHAR(32)     ,
	options              VARCHAR(256)     ,
	node                 INTEGER     ,
	VLANID               INTEGER     ,
	devtype              VARCHAR(32)  DEFAULT 'physical'   ,
	CONSTRAINT unq_netdevices_ID UNIQUE ( ID ),
	CHECK ( devtype in ('physical', 'vlan', 'bridge','ipmi') )
 );

CREATE TABLE netgens ( 
	name                 VARCHAR(100) NOT NULL    ,
	INCR                 INTEGER NOT NULL DEFAULT -1   ,
	ID                   INTEGER NOT NULL  PRIMARY KEY  
 );

CREATE TABLE reslevels ( 
	ID                   INTEGER NOT NULL  PRIMARY KEY  ,
	resname              VARCHAR(100) NOT NULL    ,
	level                INTEGER NOT NULL    ,
	CONSTRAINT unq_priorities UNIQUE ( resname, level )
 );

CREATE TABLE routes ( 
	ID                   INTEGER NOT NULL  PRIMARY KEY  ,
	network              VARCHAR(256) NOT NULL    ,
	netmask              VARCHAR(256) NOT NULL    ,
	nettype              VARCHAR(4) NOT NULL DEFAULT 'IPV4'   ,
	gateway              VARCHAR(256)     ,
	device               INTEGER     ,
	reslevel             INTEGER     ,
	reskey               VARCHAR(256)     ,
	CHECK ( nettype in ('IPV4','IPV6','IPMI') )
 );

CREATE TABLE subnets ( 
	name                 VARCHAR(32) NOT NULL    ,
	nettype              VARCHAR(4) NOT NULL DEFAULT 'IPV4'   ,
	network              VARCHAR(256) NOT NULL    ,
	prefix               INTEGER NOT NULL DEFAULT 24   ,
	servedns             BOOLEAN NOT NULL DEFAULT True   ,
	netgen               INTEGER     ,
	ID                   INTEGER NOT NULL  PRIMARY KEY  ,
	nextFree             VARCHAR(256) NOT NULL    ,
	CHECK ( nettype in ('IPV4','IPV6','IPMI') )
 );

CREATE TABLE vlans ( 
	VLANID               INTEGER NOT NULL  PRIMARY KEY  ,
	description          VARCHAR(512)     ,
	subnet               INTEGER  DEFAULT Null   
 );

CREATE TABLE appliances ( 
	ID                   INTEGER NOT NULL  PRIMARY KEY  ,
	name                 VARCHAR(128) NOT NULL    ,
	graphStart           VARCHAR(128)     ,
	description          VARCHAR(512)     ,
	graph                VARCHAR(125)  DEFAULT 'default'   ,
	reslevel             INTEGER     ,
	FOREIGN KEY ( reslevel ) REFERENCES reslevels( ID ) ON DELETE CASCADE ON UPDATE CASCADE
 );

CREATE TABLE attrs ( 
	ID                   INTEGER NOT NULL  PRIMARY KEY  ,
	attr                 VARCHAR(128) NOT NULL    ,
	value                VARCHAR(512)     ,
	shadow               VARCHAR(512)     ,
	reslevel             INTEGER     ,
	reskey               VARCHAR(512)     ,
	FOREIGN KEY ( reslevel ) REFERENCES reslevels( ID ) ON DELETE CASCADE ON UPDATE CASCADE
 );

CREATE UNIQUE INDEX unq_attrs ON attrs ( attr, reslevel );

CREATE TABLE nodes ( 
	ID                   INTEGER NOT NULL  PRIMARY KEY  ,
	name                 VARCHAR(100) NOT NULL    ,
	rack                 INTEGER  DEFAULT 0   ,
	rank                 INTEGER NOT NULL    ,
	appliance            INTEGER     ,
	dist                 INTEGER     ,
	installaction        INTEGER     ,
	runaction            INTEGER     ,
	managed              BOOLEAN  DEFAULT True   ,
	reslevel             INTEGER     ,
	FOREIGN KEY ( appliance ) REFERENCES appliances( ID ) ON DELETE SET NULL ,
	FOREIGN KEY ( reslevel ) REFERENCES reslevels( ID ) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY ( installaction ) REFERENCES bootactions( ID )  ON UPDATE CASCADE
 );

CREATE TABLE partitions ( 
	ID                   INTEGER NOT NULL  PRIMARY KEY  ,
	node                 INTEGER NOT NULL    ,
	device               VARCHAR(128)     ,
	mountpoint           VARCHAR(128)     ,
	SectorStart          INTEGER NOT NULL    ,
	SectorSize           INTEGER NOT NULL DEFAULT 512   ,
	PartitionSize        INTEGER NOT NULL    ,
	PartitionID          INTEGER NOT NULL    ,
	FStype               VARCHAR(128) NOT NULL    ,
	PartitionFlags       VARCHAR(128)     ,
	FormatFlags          VARCHAR(128)     ,
	AutoReformat         BOOLEAN NOT NULL DEFAULT FALSE   ,
	FOREIGN KEY ( node ) REFERENCES nodes( ID ) ON DELETE CASCADE ON UPDATE CASCADE
 );

CREATE TABLE hwinventory ( 
	ID                   INTEGER NOT NULL  PRIMARY KEY  ,
	node                 INTEGER NOT NULL    ,
	component            INTEGER NOT NULL    ,
	subtype              VARCHAR(128) NOT NULL DEFAULT 'generic'   ,
	count                INTEGER NOT NULL DEFAULT 1   ,
	comment              VARCHAR(512)     ,
	CONSTRAINT unq_hwinventory UNIQUE ( node, component, subtype ),
	FOREIGN KEY ( node ) REFERENCES nodes( ID ) ON DELETE CASCADE ON UPDATE CASCADE
 );

CREATE VIEW allattrsview AS
select n.name as node, a.attr, a.value, a.shadow, r.resname, r.level from nodes n, attrs a inner join reslevels r
 where a.reslevel=r.id and r.resname='global' 
UNION
select n.name as node, a.attr, a.value, a.shadow, r.resname, r.level from nodes n inner join attrs a on n.reslevel
=a.reslevel inner join reslevels r on a.reslevel=r.id where n.name = a.reskey
UNION
select n.name as node, a.attr, a.value, a.shadow, r.resname, r.level from nodes n inner join appliances ap on n.appliance=ap.id inner join attrs a on ap.reslevel=a.reslevel inner join reslevels r on a.reslevel=r.id where ap.name = a.
reskey
ORDER by node,attr;;

CREATE VIEW attrsview AS SELECT
a.ID,a.attr,a.value,a.shadow,r.resname,a.reskey,r.level
FROM attrs a LEFT JOIN reslevels r on a.reslevel=r.id;;

CREATE VIEW dbs_validate_view AS SELECT n.name, nd.device, nd.mac, nd.module,
 nd.options, net.name as netname, ip.addr, net.prefix, net.type
 FROM nodes n inner join netdevs nd on nd.node = n.id,
 ipaddrs ip inner join networks net on ip.network = net.id where ip.netdev=nd.id;;

CREATE VIEW firewallsview AS SELECT
f.ID,f.rulename,f.rulesrc,si.name as inSubnet, so.name as OutSubnet,
f.service,f.protocol,f.action,f.chain,f.flags,f.comment,rl.resname,f.reskey,rl.level
FROM firewalls f LEFT JOIN subnets si on f.InSubnet=si.ID
LEFT JOIN subnets so on f.OutSubnet=so.ID
LEFT JOIN reslevels rl on f.reslevel=rl.ID;

CREATE VIEW hwinventoryview AS SELECT
hw.id, n.name, hw.component, hw.subtype, hw.count, hw.comment 
FROM hwinventory hw INNER JOIN node n on hw.id=n.id
ORDER BY name,component,subtype;;

CREATE VIEW netdevsview  AS SELECT 
nd.id, n.name as node, nd.device, nd.mac, nd.module, nd.devtype, nd.options,
net.name as netname, ip.addr, net.prefix, net.nettype, nd.vlanid, 
vl.subnet as logicalVLAN FROM netdevs nd 
LEFT JOIN ipaddrs ip ON ip.netdev=nd.id 
LEFT join vlansview vl on vl.vlanid=nd.vlanid 
LEFT JOIN subnets net on ip.subnet=net.id INNER JOIN nodes n on nd.node=n.id;

CREATE VIEW nodesview AS SELECT
n.id,n.name as node,n.rack,n.rank,ba.action as installaction,
bb.action as runaction,n.managed,app.name as appliance,app.graph FROM nodes n INNER JOIN appliances app
on n.appliance=app.id
LEFT JOIN bootactions ba on n.installaction=ba.ID 
LEFT JOIN bootactions bb on n.runaction=bb.ID;

CREATE VIEW partitionsview AS SELECT
p.id, n.name as node, p.device, p.mountpoint, p.SectorStart, p.SectorSize,
p.PartitionSize, p.PartitionID,p.fstype,p.PartitionFlags,p.formatFlags,
p.AutoReformat from partitions p INNER JOIN nodes n ON p.node=n.id 
ORDER by node,device;

CREATE VIEW routesview AS SELECT
r.id,r.network,r.netmask,r.gateway,r.nettype,d.device,rl.resname,r.reskey,rl.level
FROM routes r LEFT JOIN reslevels rl on r.reslevel=rl.ID
LEFT JOIN netdevs d on r.device=d.ID;;

CREATE VIEW vlansview  AS SELECT VLANS.VLANID,VLANS.description,sub.name as subnet FROM
VLANS LEFT JOIN subnets sub on VLANS.subnet=sub.ID;

CREATE TRIGGER trigger_appliance_insert
AFTER  INSERT ON appliances
BEGIN
  UPDATE appliances set reslevel = (select id from reslevels r where r.resname='appliance') where appliances.id = new.id;
END;

CREATE TRIGGER trigger_appliances_update 
AFTER UPDATE on appliances 
WHEN old.name <> new.name OR
   old.reslevel <> new.reslevel
BEGIN
  UPDATE attrs set reskey=new.name where attrs.reslevel = old.reslevel and attrs.reskey = old.name;
  UPDATE attrs set reslevel=new.reslevel where attrs.reslevel=old.reslevel and attrs.reskey=new.name;
  UPDATE routes set reskey=new.name where routes.reslevel = old.reslevel and routes.reskey = old.name;
  UPDATE routes set reslevel=new.reslevel where routes.reslevel=old.reslevel and routes.reskey=new.name;
  UPDATE firewalls set reskey=new.name where firewalls.reslevel = old.reslevel and firewalls.reskey = old.name;
  UPDATE firewalls set reslevel=new.reslevel where firewalls.reslevel=old.reslevel and firewalls.reskey=new.name;
END;

CREATE TRIGGER trigger_appliance_delete
BEFORE DELETE on appliances
BEGIN
  DELETE FROM attrs where attrs.reslevel=reslevel and attrs.reskey=name;
  DELETE FROM routes where routes.reslevel=reslevel and routes.reskey=name;
  DELETE FROM firewalls where firewalls.reslevel=reslevel and firewalls.reskey=name;
END;

CREATE TRIGGER trigger_firewall_insert
AFTER  INSERT ON firewalls
BEGIN
  UPDATE firewalls set reslevel = (select id from reslevels r where r.resname='global') where firewalls.id = new.id and reslevel is NULL;
END;

CREATE TRIGGER trigger_attr_insert
AFTER  INSERT ON attrs 
BEGIN
  UPDATE attrs set reslevel = (select id from reslevels r where r.resname='global') where attrs.reslevel is NULL;
END;

CREATE TRIGGER trigger_node_insert
AFTER  INSERT ON nodes
BEGIN
  UPDATE nodes set reslevel = (select id from reslevels r where r.resname='node') where nodes.id = new.id;
END;

CREATE TRIGGER trigger_node_update 
AFTER UPDATE on nodes 
WHEN old.name <> new.name OR
   old.reslevel <> new.reslevel
BEGIN
  UPDATE attrs set reskey=new.name where attrs.reslevel = old.reslevel and attrs.reskey = old.name;
  UPDATE attrs set reslevel=new.reslevel where attrs.reslevel=old.reslevel and attrs.reskey=new.name;
  UPDATE routes set reskey=new.name where routes.reslevel = old.reslevel and routes.reskey = old.name;
  UPDATE routes set reslevel=new.reslevel where routes.reslevel=old.reslevel and routes.reskey=new.name;
  UPDATE firewalls set reskey=new.name where firewalls.reslevel = old.reslevel and firewalls.reskey = old.name;
  UPDATE firewalls set reslevel=new.reslevel where firewalls.reslevel=old.reslevel and firewalls.reskey=new.name;
END;

CREATE TRIGGER trigger_node_delete
BEFORE DELETE on nodes
BEGIN
  DELETE FROM attrs where attrs.reslevel=reslevel and attrs.reskey=name;
  DELETE FROM routes where routes.reslevel=reslevel and routes.reskey=name;
  DELETE FROM firewalls where firewalls.reslevel=reslevel and firewalls.reskey=name;
END;

CREATE TRIGGER trigger_route_insert
AFTER  INSERT ON routes
BEGIN
  UPDATE routes set reslevel = (select id from reslevels r where r.resname='global') WHERE routes.reslevel is NULL;
END;

