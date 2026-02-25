from db.odoo_connection import connect, call_kw

def getQtdByQuery(query, application):
    """
    Returns the count of users matching the query.
    """
    connect()  # ensure session authenticated

    user_ids = findByQuery(query)
    return len(user_ids)


def findByQuery(query):
    """
    Returns list of user IDs matching the query.
    Query is a dictionary like {"login": "test@example.com"}
    """
    if not query:
        domain = []
    else:
        domain = [[key, '=', value] for key, value in query.items()]

    user_ids = call_kw("res.users", "search", [domain])
    return user_ids


def getSomeAttributesByQuery(query, attributes):
    """
    Returns selected fields of users matching the query.
    Example: getSomeAttributesByQuery({"login": "test@example.com"}, ["id", "name"])
    """
    connect()  # ensure session authenticated

    user_ids = findByQuery(query)
    if not user_ids:
        return []

    records = call_kw("res.users", "read", [user_ids], {"fields": attributes})
    return records