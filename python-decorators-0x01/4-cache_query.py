import time
import sqlite3 
import functools

# This code demonstrates a caching mechanism for SQL query results using decorators.
query_cache = {}

def with_db_connection(func):
    """Decorator to handle DB connection automatically."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("chats.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

def cache_query(func):
    """Decorator to cache results based on the SQL query string."""
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        if query in query_cache:
            print("🔁 Returning cached result")
            return query_cache[query]
        else:
            print("📡 Executing new query and caching result")
            result = func(conn, query, *args, **kwargs)
            query_cache[query] = result
            return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call: executes query and caches result
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

# Second call: fetches result from cache
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)
