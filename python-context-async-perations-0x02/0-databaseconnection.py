import sqlite3
import os


class DatabaseConnection:
    """
    A context manager class for handling database connections.
    
    This class implements the context manager protocol using __enter__ and __exit__
    methods to automatically handle opening and closing database connections.
    """
    
    def __init__(self, db_name="example.db"):
        """
        Initialize the DatabaseConnection with a database name.
        
        Args:
            db_name (str): Name of the database file. Defaults to "example.db"
        """
        self.db_name = db_name
        self.connection = None
        self.cursor = None
    
    def __enter__(self):
        """
        Enter the context manager and establish database connection.
        
        Returns:
            sqlite3.Cursor: Database cursor for executing queries
        """
        try:
            # Create connection to the database
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            print(f"Database connection established to {self.db_name}")
            return self.cursor
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            raise
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if self.cursor:
                self.cursor.close()
                print("Database cursor closed")
            
            if self.connection:
                # Commit any pending transactions
                self.connection.commit()
                self.connection.close()
                print("Database connection closed")
        
        except sqlite3.Error as e:
            print(f"Error closing database connection: {e}")
        
        # Return False to propagate any exceptions that occurred in the with block
        return False


def setup_sample_database():
    """
    Set up a sample database with a users table for demonstration.
    """
    with sqlite3.connect("example.db") as conn:
        cursor = conn.cursor()
        
        # Create users table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                age INTEGER
            )
        ''')
        
        # Insert sample data if table is empty
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            sample_users = [
                ("Alice Johnson", "alice@example.com", 28),
                ("Bob Smith", "bob@example.com", 35),
                ("Charlie Brown", "charlie@example.com", 22),
                ("Diana Prince", "diana@example.com", 30)
            ]
            
            cursor.executemany(
                "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
                sample_users
            )
            print("Sample users data inserted")
        
        conn.commit()


def main():
    """
    Main function demonstrating the usage of DatabaseConnection context manager.
    """
    # Set up sample database
    setup_sample_database()
    
    print("\n" + "="*50)
    print("Using DatabaseConnection Context Manager")
    print("="*50)
    
    # Use the context manager with the 'with' statement
    try:
        with DatabaseConnection("example.db") as cursor:
            # Perform the query SELECT * FROM users
            print("\nExecuting query: SELECT * FROM users")
            cursor.execute("SELECT * FROM users")
            
            # Fetch and print all results
            results = cursor.fetchall()
            
            print("\nQuery Results:")
            print("-" * 40)
            print(f"{'ID':<5} {'Name':<15} {'Email':<20} {'Age':<5}")
            print("-" * 40)
            
            for row in results:
                print(f"{row[0]:<5} {row[1]:<15} {row[2]:<20} {row[3]:<5}")
            
            print(f"\nTotal users found: {len(results)}")
    
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()