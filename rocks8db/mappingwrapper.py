from sqlalchemy import and_,or_
class RocksBase(object):
    """Additional base class of Rocks ORM hierarchy which includes some
    helper methods for all classes"""

    @property
    def session(self):
        """Singelton which return the session of the object"""
        return sqlalchemy.orm.session.object_session(self)


    def delete(self):
        """instance method to autodelete the instance which calls it

        so you can use
        node.delete()"""
        self.session.delete(self)

    @classmethod
    def loadOne(cls, session, **kwargs):
        """ """
        return cls.load(session, **kwargs).one()


    @classmethod
    def load(cls, session, **kwargs):
        """
        this method allow us to run query on all the mapping objects
        simply using 

        e.g.::

          node = Nodes.load(session, Name='compute-0-0', Cpus=2)
          nic = Network.load(session, Name='compute-0-0', Interface='eth0')

        taken from:
        http://petrushev.wordpress.com/2010/06/22/sqlalchemy-base-model/
        """
        q = session.query(cls)
        filters = [getattr(cls, field_name)==kwargs[field_name] \
                for field_name in kwargs]
        return q.filter(and_(*filters))


