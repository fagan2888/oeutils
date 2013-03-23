import xmlrpclib

class Openerp(object):
    '''
    Attributs:
       host : server hostname, default is 'localhost', i.e 'preprod.myserver.cg'
       login : user login
       pwd : password
       dbname : database to use
       port : server port i.e 8069

    Usage:
      >>>from oetuils import Openerp
      >>>oe = Openerp(login,pwd,dbname)
      >>>oe.connect()

      Now you ready to go
    '''
    
    def __init__(self, login, pwd, dbname, host='localhost', port=8069):
        self.host = host
        self.dbname = dbname
        self.login = login
        self.pwd = pwd
        self.port = port
        self.common = None
        self.uid = None
        self.sock = None

    def __unicode__(self,):
        return "Connected on %s with user %s " %(self.host,self.login)

    def sock_common(self,):
        self.common = xmlrpclib.ServerProxy('http://%s:%s/xmlrpc/common' %(self.host,self.port))
        return self.common

    def sock_object(self,):
        self.sock = xmlrpclib.ServerProxy('http://%s:%s/xmlrpc/object' %(self.host,self.port))
        return self.sock

    def connect(self,):
        self.common = self.sock_common()
        self.sock = self.sock_object()
        self.uid = self.common.login(self.dbname, self.login, self.pwd)
        return self.uid

    def getUid(self,):
        return self.uid

    ########################################################
    # OPERATIONS       
    ########################################################

    def search(self,model,attrs):
        '''
        Returns the list ids matching the filters
        attrs is list.
        '''
        ids = self.sock.execute(self.dbname, self.uid, self.pwd, model, 'search', attrs)
        return ids

    def create(self,model,attrs):
        '''Create a new record object
        'attrs' is dictionary
        return the id of the object created
        '''
        id = self.sock.execute(self.dbname, self.uid, self.pwd, model, 'create', attrs)
        return id

    def read(self, model, ids, attrs):
        '''
        '''
        elts = self.sock.execute(self.dbname, self.uid, self.pwd, model, 'read', ids, attrs)
        return elts

    def edit(self, model, attrs):
        '''
        '''
        ids = self.sock.execute(self.dbname, self.uid, self.pwd, model, 'write', ids, attrs)
        return ids
        
    def delete(self, model, ids, attrs):
        '''
        '''
        ids = self.sock.execute(self.dbname, self.uid, self.pwd, model, 'unlink', ids)
        return ids

    def model(self, model):
        '''Search a model and return matching model or models
        '''
        
    ########################################################

    


if __name__ == '__main__':
    openerp = Openerp()