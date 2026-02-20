import db.odoo_connection as odoo_connection

def getQtdByQuery(query, application):
    return findByQuery(query, application).count()

def findByQuery(query, application):
    client = odoo_connection.connect()
    return client[application]["users"].find(query)

def getSomeAtributesByQuery(query, atributes, application):
    client = odoo_connection.connect()
    return client[application]["users"].find(query, atributes)
