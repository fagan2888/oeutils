##OEUTILS

__oeutils__ is a small python wrapper of the xml-rpc API for OpenERP. It is usefull to manipulate your OpenERP objects.
It is not as powerful as __erppeek__ yet but i hope that with your help one day it will ^_^

###Features
With __oeutils__ you are able to :

. Create objects
. Read objects
. Update objects
. Delete objects
. Search objects
. Search models
. Get models fields


###How to

####Connexion

	:::python

	>>>from oeutils import Openerp
  	>>>o = Openerp(login,pwd,dbname)
  	>>>o.connect()

####Methods

	:::python
	>>>m = 'family.family'
	>>>ids = o.search(m,[]) # or juste o.search(m)
	>>>ids
	[1, 2]
	>>>
	>>> famliy = {
	... 'name': 'kouka',
	... }
    >>> o.create('family.family',famliy)
    2
    >>>m = 'family.family'
    >>>o.read(m,ids,[])
    [{'member_ids': [1], 'name': 'loking', 'id': 1}, {'member_ids': [], 'name': 'kouka', 'id': 2}]
	>>>m = 'family.family'
    >>> o.edit(m,2,{'name':'koukson'})
    True
    >>> o.read(m,o.search(m,[]),[])
    [{'member_ids': [1], 'name': 'loking', 'id': 1}, {'member_ids': [], 'name': 'koukson', 'id': 2}]
	>>>m = 'family.family'
    >>> o.read(m,o.search(m,[]),[])
    [{'member_ids': [1], 'name': 'loking', 'id': 1}, {'member_ids': [], 'name': 'koukson', 'id': 2}, {'member_ids': [], 'name': 'kim', 'id': 3}]
    >>> o.delete(m,3)
    True
    >>> o.read(m,o.search(m,[]),[])
    [{'member_ids': [1], 'name': 'loking', 'id': 1}, {'member_ids': [], 'name': 'koukson', 'id': 2}]
     >>> o.models('family')
	['family.family', 'family.member']
	>>> o.keys(m)
    ['member_ids', 'name']

That's all, thanks in advance for your feebacks
