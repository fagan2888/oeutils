###############################################
# -*- coding: utf-8 -*-
# Kéba ! na libossooo !! ngué ké diata farata 
###############################################

import xmlrpclib
import inspect

class Openerp(object):
    '''
    Attributs:
       host : server hostname, default is 'localhost', i.e 'preprod.myserver.cg'
       login : user login
       pwd : password
       dbname : database to use
       port : server port i.e 8069

    Usage:
      >>>from oeutils import Openerp
      >>>oe = Openerp(login,pwd,dbname)
      >>>oe.connect()

      Now you ready to go
    '''
    
    _DEFAULT_HOST_ = 'localhost'
    _DEFAULT_LOGIN_ = 'admin'
    _DEFAULT_PASSWORD_ = 'admin'
    _DEFAULT_DBNAME_ = 'openerp'
    _DEFAULT_PORT_ = 8069
    
    def __init__(self, login=_DEFAULT_LOGIN_, pwd=_DEFAULT_PASSWORD_, dbname=_DEFAULT_DBNAME_, host=_DEFAULT_HOST_, port=_DEFAULT_PORT_):
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

    #########################################################
    # CLIENT
    ########################################################
        
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

    def execute(self, model, method, *args, **kwargs):
        result = self.sock.execute(self.dbname, self.uid, self.pwd, model, method, args, kwargs)
        return result
        
    ########################################################
    # METHODS       
    ########################################################

    def search(self,model,attrs=[]):
        '''
        Returns the list ids matching the filters
        attrs is list.
        Example:
        >>>ids = o.search('family.family',[])
        >>>ids
        [1, 2]
        '''
        ids = self.sock.execute(self.dbname, self.uid, self.pwd, model, 'search', attrs)
        return ids

    def create(self,model,attrs):
        '''Create a new record object
        'attrs' is dictionary
        return the id of the object created
        Example:
        >>> famliy = {
        ... 'name': 'kouka',
        ... }
        >>> o.create('family.family',famliy)
        2
        '''
        id = self.sock.execute(self.dbname, self.uid, self.pwd, model, 'create', attrs)
        return id

    def read(self, model, ids, attrs=[]):
        '''Returns list of records matching the search ids
           according to filters.
        Example:
        >>>m = 'family.family'
        >>>o.read(m,ids,[])
        [{'member_ids': [1], 'name': 'loking', 'id': 1}, {'member_ids': [], 'name': 'kouka', 'id': 2}]
        '''
        elts = self.sock.execute(self.dbname, self.uid, self.pwd, model, 'read', ids, attrs)
        return elts

    def edit(self, model, ids, attrs):
        '''Updates records and return True of records updated
           attrs is dictionary
        Example:
        >>>m = 'family.family'
        >>> o.edit(m,2,{'name':'koukson'})
        True
        >>> o.read(m,o.search(m,[]),[])
        [{'member_ids': [1], 'name': 'loking', 'id': 1}, {'member_ids': [], 'name': 'koukson', 'id': 2}]
        '''
        ids = self.sock.execute(self.dbname, self.uid, self.pwd, model, 'write', ids, attrs)
        return ids
        
    def delete(self, model, ids):
        '''Delete records and returns True if deleted
        Example:
        >>>m = 'family.family'
        >>> o.read(m,o.search(m,[]),[])
        [{'member_ids': [1], 'name': 'loking', 'id': 1}, {'member_ids': [], 'name': 'koukson', 'id': 2}, {'member_ids': [], 'name': 'kim', 'id': 3}]
        >>> o.delete(m,3)
        True
        >>> o.read(m,o.search(m,[]),[])
        [{'member_ids': [1], 'name': 'loking', 'id': 1}, {'member_ids': [], 'name': 'koukson', 'id': 2}]
        >>> 
        '''
        ids = self.sock.execute(self.dbname, self.uid, self.pwd, model, 'unlink', ids)
        return ids


    #########################################################
    # Maybe the only interesting part, not clean and clear
    # though
    ########################################################
    def models(self, modelname):
        '''Search a model and return matching model or models
        Example:
        >>> o.models('family.family')
        ['family.family']
        '''
        ids = self.search('ir.model', [('model', 'ilike', modelname)])
        results = [ m['model'] for m in self.read('ir.model', ids, ['model','name'])]
        return results

    def keys(self, modelname):
        '''Returns list of fields of a model
        Example:
        >>> m = 'family.family'
        >>> o.keys(m)
        ['member_ids', 'name']
        >>> 
        '''
        ids = self.search('ir.model.fields', [('model','=',modelname)])
        results = [ m['name'] for m in self.read('ir.model.fields', ids, ['name'])]
        return results

    #Will i be able to implement a browse method ?
 
    ########################################################
    ########################################################
        
if __name__ == '__main__':
    openerp = Openerp()