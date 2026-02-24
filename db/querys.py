import db.odoo_connection as odoo_connection

def getQtdByQuery(query, application):
    uid, models = odoo_connection.connect()
    user_ids = findByQuery(query, application, uid, models)
    return len(user_ids)


def findByQuery(query, application, uid=None, models=None):
    if not uid or not models:
        uid, models = odoo_connection.connect()

    domain = [[key, '=', value] for key, value in query.items()]

    user_ids = models.execute_kw(
        application,  
        uid,
        odoo_connection.ODOO_PASSWORD,
        'res.users',  
        'search',     
        [domain]
    )
    return user_ids


def getSomeAttributesByQuery(query, attributes, application):
    uid, models = odoo_connection.connect()
    user_ids = findByQuery(query, application, uid, models)

    if not user_ids:
        return []

    records = models.execute_kw(
        application,
        uid,
        odoo_connection.ODOO_PASSWORD,
        'res.users',
        'read',
        [user_ids],
        {'fields': attributes}
    )
    return records