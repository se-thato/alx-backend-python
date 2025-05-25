import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator that yields user data in batches from the user_data table.

    Args:
        batch_size (int): Number of rows per batch.
    """
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='theplanetisflat',
        database='ALX_prodev'
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        yield rows  # yield a batch of rows

    cursor.close()
    connection.close()

def batch_processing(batch_size):
    """
    Processes batches of user data, printing only users older than 25.

    Args:
        batch_size (int): Number of rows per batch to process.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)
