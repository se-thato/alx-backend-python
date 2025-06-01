import time
import sqlite3
import functools

def with_db_connection(func):
    """Decorator that opens and closes a database connection automatically."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("chats.db")
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper

def retry_on_failure(retries=3, delay=2):
    """Decorator that retries a function if it fails due to an exception."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    print(f"Attempt {attempts} failed: {e}")
                    if attempts == retries:
                        print("All retries failed.")
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")  # This will raise an error if table doesn't exist
    return cursor.fetchall()

# Attempt to fetch users with automatic retry on failure
users = fetch_users_with_retry()
print(users)
