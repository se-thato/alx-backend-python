import sqlite3
from typing import Any, Iterable, List, Optional, Sequence, Tuple


class ExecuteQuery:
    """
    Context manager to open a DB connection, execute a query with parameters,
    return the results, and then close the connection automatically.

    Usage:
        with ExecuteQuery(query, params, db_name="example.db") as results:
            # results contains the list of rows
            ...
    """

    def __init__(self, query: str, params: Optional[Sequence[Any]] = None, db_name: str = "example.db") -> None:
        self.query = query
        self.params: Tuple[Any, ...] = tuple(params) if params is not None else tuple()
        self.db_name = db_name
        self.connection: Optional[sqlite3.Connection] = None
        self.cursor: Optional[sqlite3.Cursor] = None
        self._results: Optional[List[Tuple[Any, ...]]] = None

    def __enter__(self) -> List[Tuple[Any, ...]]:
        """
        Open the connection, execute the query, fetch all results, and return them.
        """
        # Establish connection and execute query
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

        # Execute with parameters if provided
        if self.params:
            self.cursor.execute(self.query, self.params)
        else:
            self.cursor.execute(self.query)

        # Fetch all results immediately so they are available after closing
        self._results = self.cursor.fetchall()
        return self._results

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """
        Ensure cursor and connection are closed. Do not suppress exceptions.
        """
        try:
            if self.cursor is not None:
                self.cursor.close()
            if self.connection is not None:
                # Commit in case of non-SELECT operations; harmless for SELECT
                self.connection.commit()
                self.connection.close()
        finally:
            # Returning False lets any exception propagate
            return False


# Demo helpers below: create sample DB if not present

def setup_sample_database(db_name: str = "example.db") -> None:
    """Create a sample users table and seed a few rows if empty."""
    with sqlite3.connect(db_name) as conn:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                age INTEGER
            )
            """
        )
        # Seed sample data only if table is empty
        cur.execute("SELECT COUNT(*) FROM users")
        if cur.fetchone()[0] == 0:
            cur.executemany(
                "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
                [
                    ("Alice Johnson", "alice@example.com", 28),
                    ("Bob Smith", "bob@example.com", 35),
                    ("Charlie Brown", "charlie@example.com", 22),
                    ("Diana Prince", "diana@example.com", 30),
                    ("Eve Adams", "eve@example.com", 26),
                ],
            )
        conn.commit()


def main() -> None:
    # Ensure the database exists with sample data
    setup_sample_database("example.db")

    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    # Use the ExecuteQuery context manager
    with ExecuteQuery(query, params, db_name="example.db") as results:
        # Print results from the query
        print("Query:", query)
        print("Params:", params)
        print("Results:")
        for row in results:
            print(row)
        print(f"Total rows: {len(results)}")


if __name__ == "__main__":
    main()
