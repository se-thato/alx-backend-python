#!/usr/bin/env python3
"""
Run multiple database queries concurrently using asyncio.gather and aiosqlite.

This script defines two asynchronous functions:
- async_fetch_users(): fetches all users
- async_fetch_older_users(): fetches users older than a given age (default: 40)

Both are executed concurrently via asyncio.gather in fetch_concurrently().
The script seeds a sample SQLite database if empty to make the example standalone.
"""

import asyncio
from typing import Any, List, Tuple

import aiosqlite

DB_NAME = "example.db"


async def setup_sample_database(db_name: str = DB_NAME) -> None:
    """Create a sample users table and seed a few rows if the table is empty."""
    async with aiosqlite.connect(db_name) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                age INTEGER
            )
            """
        )
        cur = await db.execute("SELECT COUNT(*) FROM users")
        row = await cur.fetchone()
        await cur.close()
        if row and row[0] == 0:
            # Include some users older than 40 to showcase the second query
            users = [
                ("Alice Johnson", "alice@example.com", 28),
                ("Bob Smith", "bob@example.com", 35),
                ("Charlie Brown", "charlie@example.com", 22),
                ("Diana Prince", "diana@example.com", 30),
                ("Eve Adams", "eve@example.com", 26),
                ("Frank Miller", "frank@example.com", 45),
                ("Grace Hopper", "grace@example.com", 52),
            ]
            await db.executemany(
                "INSERT INTO users (name, email, age) VALUES (?, ?, ?)", users
            )
            await db.commit()


async def async_fetch_users(db_name: str = DB_NAME) -> List[Tuple[Any, ...]]:
    """Fetch all users asynchronously."""
    async with aiosqlite.connect(db_name) as db:
        cur = await db.execute("SELECT * FROM users")
        rows = await cur.fetchall()
        await cur.close()
    return rows


async def async_fetch_older_users(age_threshold: int = 40, db_name: str = DB_NAME) -> List[Tuple[Any, ...]]:
    """Fetch users older than the provided age_threshold asynchronously."""
    async with aiosqlite.connect(db_name) as db:
        cur = await db.execute("SELECT * FROM users WHERE age > ?", (age_threshold,))
        rows = await cur.fetchall()
        await cur.close()
    return rows


async def fetch_concurrently() -> None:
    """Run async_fetch_users and async_fetch_older_users concurrently and print results."""
    await setup_sample_database(DB_NAME)

    all_users_task = async_fetch_users(DB_NAME)
    older_users_task = async_fetch_older_users(40, DB_NAME)

    all_users, older_users = await asyncio.gather(all_users_task, older_users_task)

    print("All users:")
    for row in all_users:
        print(row)
    print(f"Total users: {len(all_users)}")

    print("\nUsers older than 40:")
    for row in older_users:
        print(row)
    print(f"Total older users: {len(older_users)}")


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
