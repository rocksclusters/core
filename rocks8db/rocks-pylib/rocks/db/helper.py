#! /opt/rocks/bin/python
#
# @Copyright@
# 
#                 Rocks(r)
#                  www.rocksclusters.org
#                  version 6.2 (SideWinder)
#                  version 7.0 (Manzanita)
# 
# Copyright (c) 2000 - 2017 The Regents of the University of California.
# All rights reserved.    
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
# notice unmodified and in its entirety, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided 
# with the distribution.
# 
# 3. All advertising and press materials, printed or electronic, mentioning
# features or use of this software must display the following acknowledgement: 
# 
#     "This product includes software developed by the Rocks(r)
#     Cluster Group at the San Diego Supercomputer Center at the
#     University of California, San Diego and its contributors."
# 
# 4. Except as permitted for the purposes of acknowledgment in paragraph 3,
# neither the name or logo of this software nor the names of its
# authors may be used to endorse or promote products derived from this
# software without specific prior written permission.  The name of the
# software includes the following terms, and any derivatives thereof:
# "Rocks", "Rocks Clusters", and "Avalanche Installer".  For licensing of 
# the associated name, interested parties should contact Technology 
# Transfer & Intellectual Property Services, University of California, 
# San Diego, 9500 Gilman Drive, Mail Code 0910, La Jolla, CA 92093-0910, 
# Ph: (858) 534-5815, FAX: (858) 534-7345, E-MAIL:invent@ucsd.edu
# 
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# @Copyright@
#


import rocks.db.database
import rocks
import rocks.util
import string

from rocks.db.mappings.base import *
from sqlalchemy import or_, and_


attr_postfix = "_old"


class DatabaseHelper(rocks.db.database.Database):
    """
    This class extend the Database class with a set of helper methods
    which deal with the new ORM interface (aka the objects from the 
    rocks.db.mappings classes).

    These methods should replace the old methods in :mod:`rocks.commands`
    only methods relative to the command line should remain in the that
    module, all DB functionality should be migrated.
    """

### Implementation Note:
### Whenever possible, data read from the database should come from the constructed views

    def __init__(self):
        # we need to call the super class constructor
        super(DatabaseHelper, self).__init__()
        # cache for the list of appliances
        self._appliances_list = None
        # cache for the attributes
        self._attribute = None
        # cache for frontend name
        self._frontend = None
        # dictionary to cache attributes
        self._cacheAttrs = {}


    def getListHostnames(self):
        """
        Return a list of string containing all the current hostnames

        :rtype: list
        :return: a list of strings containing all the nodes names
        """
        list = self.getSession().query(Nodesview.node).all()
        return [item for item, in list]


    def getNodesfromNames(self, names=None, managed_only=0, preload=[]):
        """
        Expands the given list of names to valid set of 
        :class:`rocks.db.mappings.base.Node` entries.
        A name can be a hostname, IP address, our group (membership name), 
        or a MAC address. Any combination of these is valid.
        If the names list is empty a list of all Node in the cluster
        is returned.

        The following groups are recognized:

        - rackN: All non-frontend host in rack N
        - appliancename: All appliances of a given type (e.g. compute)
        - select ...: an SQL statement that returns a list of hosts

        :type names: list
        :param names: a list of string containing the hostname we want to
                  resolve following the naming rules stated above

        :type managed_only: bool
        :param managed_only: if true the list of hosts will *not* contain 
                     hosts that traditionally don't have ssh login
                     shells (for example, the following appliances
                     usually don't have ssh login access: 
                     'Ethernet Switches', 'Power Units',
                     'Remote Management')


        :type preload: list
        :param preload: a list of strings containing the relationships
                        which should be preloaded to avoid sub-query
                        when accessing related tables. If you need to
                access node.membership.name (the node
                membership name) you should pass 
                preload=['membership'] to preload the
                membership table 
                (http://docs.sqlalchemy.org/en/latest/orm/loading.html)

        :rtype: list
        :return: a list of :class:`rocks.db.mappings.base.Node`
        """

        # Handle the simple case first and just return a complete
        # list of hosts in the cluster if no list of names was
        # provided


        list = []
        if not names:
            
                if managed_only:
                list = self.getSession().query(Nodesview.node).filter(Nodesview.managed=True)
                else:
                list = self.getSession().query(Nodesview.node)

            for i in preload:
                list = list.options(sqlalchemy.orm.joinedload(i))
            list = list.all()

            return list

        
        # we start with a false clause and then we add with OR all the other condition
        # while parsing the various names
        clause = sqlalchemy.sql.expression.false()
        query = self.getSession().query(Nodesview.node)

        for name in names:
            if name.find('select ') == 0:    # SQL select
                self.execute(name)
                nodes = [i for i, in self.fetchall()]
                clause = or_(clause, Nodesview.node.in_(nodes))
            elif name.find('%') >= 0:    # SQL % pattern
                clause = or_(clause, Nodesview.node.like(name))
            elif name.startswith('rack'):
                # this is racks
                racknumber = int(name[4:])
                clause = or_(clause, Nodesview.rack == racknumber)
                clause = and_(clause, Nodesview.appliance != 'frontend')
            elif name in self.getAppliancesListText():
                # it is an appliance
                clause = or_(clause, Nodesview.appliance == name)
            else:               
                # it is a host name
                clause = or_(clause, Nodesview.name == self.getHostname(name))
                #import pdb; pdb.set_trace()
        
        # now we register the query on the table Node and append all our clauses on OR
        query = query.filter(clause)
        for i in preload:
            query = query.options(sqlalchemy.orm.joinedload(i))
        return query.all()


    def getAppliancesListText(self):
        """
        Return a list of all the appliances names in the DB.

        This query is run only once, if it is called multiple times it will return 
        always the same results (for obvious preformance reason)

        :rtype: list
        :return: a list of string with the appliances names
        """
        if self._appliances_list:
            return self._appliances_list
        else:
            # first time we invoke it, run the query and cache the results
            self._appliances_list = \
                [a.name for a in self.getSession().query(Appliances.name)]
            return self._appliances_list


    def getApplianceNames(self, args=None, preload=[]):
        """
        Returns a list of :class:`rocks.db.mappings.base.Appliance` instance
        from the database.

        For each arg in the ARGS list find all the appliance
        names that match the arg (assume SQL regexp).  If an
        arg does not match anything in the database we Abort.  If the
        ARGS list is empty return all appliance names.

        
        :type args: list
        :param args: a list of string containing the appliances name
                  we want to resolve (it supports SQL regexp) 

        :type preload: list
        :param preload: a list of strings containing the relationships
                        which should be preloaded to avoid sub-query
                        when accessing related tables. Check 
                :meth:`getNodesfromNames` for some example.

        :rtype: list
        :return: a list of :class:`rocks.db.mappings.base.Appliance`
        """
        clause = sqlalchemy.sql.expression.false()
        query = self.getSession().query(Appliances.name)

        if not args:
            args = [ '%' ] # find all appliances
        for arg in args:
            clause = or_(clause, Appliances.name.like(arg))
        query = query.filter(clause)

        for i in preload:
            query = query.options(sqlalchemy.orm.joinedload(i))

        return query


    def getFrontendName(self):
        """
        return the frontend name and caches it

        :rtype: string
        :return: the frontend name
        """
        if self._frontend :
            return self._frontend

        ##XXX: FIXME
        self._frontend = self.getCategoryAttr('global', 'global', \
                'Kickstart_PrivateHostname')
        return self._frontend



    def getHostname(self, hostname=None):
        """
        Returns the name of the given host as referred to in the
        database. This is used to normalize a hostname before
        using it for any database queries.

        :type hostname: string
        :param hostname: a hostname in a non normalized form

        :rtype: string
        :return: the host name in a normalized form
        """

        # Look for the hostname in the database before trying
        # to reverse lookup the IP address and map that to the
        # name in the nodes table.  This should speed up the
        # installer w/ the restore roll

        arghostname = hostname 

        if hostname:
            matchhost = session.query(Nodes.name).\
             filters(func.lower(Nodes.name) = '%s' % hostname.lower())
            if matchhost is not None:
                return matchhost 

        if not hostname:                    
            hostname = socket.gethostname().split('.')[0]
        try:

            # Do a reverse lookup to get the IP address.
            # Then do a forward lookup to verify the IP
            # address is in DNS.  This is done to catch
            # evil DNS servers (timewarner) that have a
            # catchall address.  We've had several users
            # complain about this one.  Had to be at home
            # to see it.
            #
            # If the resolved address is the same as the
            # hostname then this function was called with
            # an ip address, so we don't need the reverse
            # lookup.
            #
            # For truly evil DNS (OpenDNS) that have
            # catchall servers that are in DNS we make
            # sure the hostname matches the primary or
            # alias of the forward lookup Throw an Except,
            # if the forward failed an exception was
            # already thrown.


            addr = socket.gethostbyname(hostname)
            if not addr == hostname:
                (name, aliases, addrs) = socket.gethostbyaddr(addr)
                if hostname != name and hostname not in aliases:
                    raise NameError

        except:
            if hostname == 'localhost':
                addr = '127.0.0.1'
            else:
                addr = None

        if not addr and self.conn:
            matchhost = session.query(Nodes.name).\
             filters(func.lower(Nodes.name) = '%s' % hostname.lower())
            if matchhost is not None:
                return matchhost 

            #
            # see if this is a MAC address
            # lowercase mac address comparisons
            
            matchhost = session.query(Netdevsview.node).\
                    filters(func.lower(Netdevsview.mac) = '%s' % hostname.lower())
            if matchhost is not None:
                return hostname

            #
            # see if this is a FQDN. 
            #
            n = hostname.split('.')
            matchhost = session.query(Netdevsview.node).\
                    filters(func.lower(Netdevsview.fqdn) = '%s' % hostname.lower())
            if matchhost is not None:
                return hostname

            # Check if the hostname is a basename
            # and the FQDN is in /etc/hosts but
            # not actually registered with DNS.
            # To do this we need lookup the DNS
            # search domains and then do a lookup
            # in each domain.  The DNS lookup will
            # fail (already has) but we might
            # find an entry in the /etc/hosts
            # file.
            #
            # All this to handle the case when the
            # user lies and gives a FQDN that does
            # not really exist.  Still a common
            # case.
            
            try:
                fin = open('/etc/resolv.conf', 'r')
            except:
                fin = None
            if fin:
                domains = []
                for line in fin.readlines():
                    tokens = line[:-1].split()
                    if len(tokens) > 0 and tokens[0] == 'search':
                        domains = tokens[1:]
                for domain in domains:
                    try:
                        name = '%s.%s' % (hostname, domain)
                        addr = socket.gethostbyname(name)
                        hostname = name
                        break
                    except:
                        pass
                if addr and addr != '127.0.0.1':
                    return self.getHostname(hostname)

                fin.close()

            # TODO add phils execption to this
            raise rocks.util.HostnotfoundException(\
                'cannot resolve host "%s"' % hostname)
                
        
        if addr == '127.0.0.1': # allow localhost to be valid
            if arghostname == None:
                # break out of recursive loop
                return 'localhost'
            else:
                return self.getHostname()
            
        # Look up the IP address in the networks table
        # to find the hostname (nodes table) of the node.
        #
        # If the IP address is not found also see if the
        # hostname is in the networks table.  This last
        # check handles the case where DNS is correct but
        # the IP address used is different.
        matchhost = session.query(Netdevsview.node).\
              filters(Netdevsview.addr) = '%s' % hostname)
        if matchhost is not None:
               return hostname

    def checkHostnameValidity(self, hostname):
        """
        check that the given host name is valid

        it checks that the hostname:
        - it does not contain any .
        - it is not already used
        - it is not a appliance name
        - it is not in the form of rack<number>
        - it is not an alias
        - it is not a mac address

        I would like to have this method return true or false but for
        legacy reason I leave it like this.

        :type hostname: string
        :param hostname: a hostname for a new host

        :raises rocks.util.CommandError: if the name does not conform
                         to the rules above mentioned
        """

        # they can not be in the form of rack<number>
        if '.' in hostname:
            raise rocks.util.CommandError('Hostname %s can not contains any dot.'
                    % hostname)
        msg = ''
        if hostname.startswith('rack'):
            number = hostname.split('rack')[1]
            try:
                int(number)
                msg = ('Hostname %s can not be in the form ' \
                    + 'of rack<number>.\n') % hostname
                msg += 'Select a different hostname.'
            except ValueError:
                pass
        if msg:
            raise rocks.util.CommandError(msg)

        # they can not be equal to any appliance name
        if hostname in self.getAppliancesListText():
            msg = 'Hostname %s can not be equal to an appliance'\
                ' name.\n' % (hostname)
            msg += 'Select a different hostname.'
            raise rocks.util.CommandError(msg)

        # check the name is not already in use in the DB
        try:
            # TODO maybe this is not the proper function to check this
            # it does too many tests we just need hostname IP and MAC
            host = self.getHostname(hostname)
            if host:
                msg = 'Node %s already exists.\n' % hostname
                msg += 'Select a different hostname, cabinet '
                msg += 'and/or rank value.'
        except (rocks.util.HostnotfoundException, NameError):
            # good! Host does not exist
            return
        raise rocks.util.CommandError(msg)



    def getHostAttrs(self, hostname, showsource=False):
        """
        it returns a dictionary of {attr_name1: value1, attr_name2: value2}
        for a given hostname. In the dictionary it resolve the attributes values
        following their precendence. If showsource is True the returned attr will
        contains an extra field with the attribute type

        :type hostname: string
        :param hostname: the hostname we want to get the attribute

        :type showsource: bool
        :param showsource: if true the values of the results will be a tuple
                   where the first element is the value of the attr
                   and the second element is the scope of the
                   attribute

        :rtype: dict
        :return: a dictionary with where the key is the name of the attribute
             and the key is the value
        """

        session = self.getSession()

        ### This is a seemingly complicated SELECT
        ### 1. Expand all global attrs for the node
        ### 2. Get node-specific attrs
        ### 3. Get appliance specific 
        ### 4. Get generic group-level 
        ### In can be constructed to resolve attribute 
        ###      "MAX(r.level) as level" with the GROUP BY clause  will get resolved
        ###      r.level will get all attributes for a node at all levels

        commonSelect = "SELECT n.name AS node, a.attr, a.value, a.shadow, r.resname, r.level FROM "
        clauseGlobal = "nodes n INNER JOIN attrs a INNER JOIN reslevels r "
        clauseGlobal += "WHERE a.reslevel=r.id AND r.resname='global' AND n.name='%s' "
        clauseNode ="nodes n INNER JOIN attrs a ON n.reslevel=a.reslevel "
        clauseNode +="INNER JOIN reslevels r ON a.reslevel=r.id WHERE n.name = a.reskey AND n.name='%s' "
        clauseAppliance = "nodes n INNER JOIN appliances ap ON n.appliance=ap.id INNER JOIN attrs a "
        clauseAppliance += "ON ap.reslevel=a.reslevel INNER JOIN reslevels r ON a.reslevel=r.id "
        clauseAppliance += "WHERE ap.name = a.reskey AND n.name='%s'"
        groupSelect = "SELECT r.node,a.attr,a.value,a.shadow,r.resname, r.level FROM "
        clauseGroup = "groupmembersview r INNER JOIN attrsview a ON r.resname=a.resname "
        clauseGroup += "WHERE r.reskey = a.reskey and r.node = '%s'"


        if isinstance(hostname, str):
            nhostname = self.getHostname(hostname)
        elif isinstance(hostname, Nodes):
            nhostname = self.getHostname(hostname.name)
        else:
            assert False, "hostname must be either a string with a hostname or a Nodes"

        # Get a reference to the node we're talking about
        node = session.query(Nodesview).query(Nodeview.node == '%s' % nhostname).one()

        attrs = {}
        # Get the internal attributes
        if showsource:
            attrs['hostname']    = (nhostname, 'I')
            attrs['rack']        = (str(node.rack), 'I')
            attrs['rank']        = (str(node.rank), 'I')
            attrs['appliance']    = (node.appliance, 'I')

        else:
            attrs['hostname']    = nhostname
            attrs['rack']        = str(node.rack)
            attrs['rank']        = str(node.rank)
            attrs['appliance']    = node.appliance

        # Construct the query
       cselect = commonSelect
       gselect = groupSelect

       allhostattrsQ = " UNION ". join( [cselect + clauseGlobal % nhostname,
          cselect + clauseNode % nhostname, cselect + clauseAppliance % nhostname, gselect + clauseGroup % nhostname ] )
       attrquery = "SELECT node,attr,value,shadow,resname,MAX(level) from (%s) GROUP BY node,attr;" % allhostattrsQ

        for (host, attr, value, shadow, restype, level) in self.conn.execute(text(attrquery)):
                host=hostname):
            if showsource:
                attrs[attr]     = (value, restype)
            else:
                attrs[attr]     = value

        # TODO cache attributes tables for speed
        # self._cacheAttrs[node.name] = attrs
        if showsource:
            attrs['arch'] = (rocks.util.getNativeArch(),'G')
            attrs['rocks_release'] = (rocks.release,'G')
            attrs['rocks_version'] = (rocks.version,'G')
            attrs['rocks_version_major'] = (rocks.version_major,'G')
            attrs['version'] = (rocks.version,'G')
        else:
            attrs['arch'] = rocks.util.getNativeArch()
            attrs['rocks_release'] = rocks.release
            attrs['rocks_version'] = rocks.version
            attrs['rocks_version_major'] = rocks.version_major
            attrs['version'] = rocks.version
        return attrs


    def getHostAttr(self, hostname, attr):
        """
        like :meth:`getHostAttrs` but it returns the value of the
        given attr

        :type hostname: string
        :param hostname: the hostname we want to get the attribute

        :type hostname: string
        :param hostname: the name of the attribute

        :rtype: string
        :return: the value of the attribute
        """
        return self.getHostAttrs(hostname).get(attr)




# this query will get all the attribute for a particular host
# the inner select (which goes in the table sub) finds all
# the attr name and maximum precedence (called maxprec)
# corresponding to a host. The outer select will then fetch
# the value for each given attr name and maxprec
#
# this query should be substituted with the tuple
# (host, host)
sql_attribute_query = """
select a.attr, a.value, UPPER(SUBSTRING(c.Name, 1, 1)) as category
from attributes a, resolvechain r, categories c, hostselections hs,
  (select attr, max(precedence) as maxprec
   from attributes a, resolvechain r, hostselections hs
   where a.category = r.category and a.category = hs.category
     and a.catindex = hs.selection and hs.host = :host
     group by attr) as sub
where a.attr = sub.attr and a.category = r.category
 and sub.maxprec = r.precedence and a.category = hs.category 
 and a.catindex = hs.selection and c.id = hs.category
 and hs.host = :host;
"""
