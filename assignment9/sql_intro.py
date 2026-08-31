import sqlite3


def add_publisher(cursor, name):
    try:
        cursor.execute(
            "INSERT INTO publishers (name) VALUES (?)",
            (name,)
        )
        print(f"Publisher added: {name}")
    except sqlite3.IntegrityError:
        print(f"Publisher already exists: {name}")


def add_magazine(cursor, name, publisher_name):
    try:
        cursor.execute(
            "SELECT publisher_id FROM publishers WHERE name = ?",
            (publisher_name,)
        )
        result = cursor.fetchone()

        if result is None:
            print(f"Publisher not found: {publisher_name}")
            return

        publisher_id = result[0]

        cursor.execute(
            """
            SELECT magazine_id
            FROM magazines
            WHERE name = ? AND publisher_id = ?
            """,
            (name, publisher_id)
        )

        if cursor.fetchone() is not None:
            print(f"Magazine already exists: {name}")
            return

        cursor.execute(
            """
            INSERT INTO magazines (name, publisher_id)
            VALUES (?, ?)
            """,
            (name, publisher_id)
        )

        print(f"Magazine added: {name}")

    except sqlite3.Error as e:
        print(f"Error adding magazine: {e}")


def add_subscriber(cursor, name, address):
    try:
        cursor.execute(
            """
            SELECT subscriber_id
            FROM subscribers
            WHERE name = ? AND address = ?
            """,
            (name, address)
        )

        if cursor.fetchone() is not None:
            print(f"Subscriber already exists: {name}, {address}")
            return

        cursor.execute(
            "INSERT INTO subscribers (name, address) VALUES (?, ?)",
            (name, address)
        )

        print(f"Subscriber added: {name}")

    except sqlite3.Error as e:
        print(f"Error adding subscriber: {e}")


def add_subscription(
    cursor,
    subscriber_name,
    subscriber_address,
    magazine_name,
    expiration_date
):
    try:
        cursor.execute(
            """
            SELECT subscriber_id
            FROM subscribers
            WHERE name = ? AND address = ?
            """,
            (subscriber_name, subscriber_address)
        )

        subscriber = cursor.fetchone()

        if subscriber is None:
            print(f"Subscriber not found: {subscriber_name}")
            return

        subscriber_id = subscriber[0]

        cursor.execute(
            """
            SELECT magazine_id
            FROM magazines
            WHERE name = ?
            """,
            (magazine_name,)
        )

        magazine = cursor.fetchone()

        if magazine is None:
            print(f"Magazine not found: {magazine_name}")
            return

        magazine_id = magazine[0]

        cursor.execute(
            """
            SELECT subscription_id
            FROM subscriptions
            WHERE subscriber_id = ? AND magazine_id = ?
            """,
            (subscriber_id, magazine_id)
        )

        if cursor.fetchone() is not None:
            print(
                f"Subscription already exists: "
                f"{subscriber_name} -> {magazine_name}"
            )
            return

        cursor.execute(
            """
            INSERT INTO subscriptions
            (subscriber_id, magazine_id, expiration_date)
            VALUES (?, ?, ?)
            """,
            (subscriber_id, magazine_id, expiration_date)
        )

        print(
            f"Subscription added: "
            f"{subscriber_name} -> {magazine_name}"
        )

    except sqlite3.Error as e:
        print(f"Error adding subscription: {e}")


def run_queries(cursor):
    print("\n--- All Subscribers ---")
    cursor.execute("SELECT * FROM subscribers")

    for row in cursor.fetchall():
        print(row)

    print("\n--- Magazines Sorted by Name ---")
    cursor.execute(
        "SELECT * FROM magazines ORDER BY name"
    )

    for row in cursor.fetchall():
        print(row)

    publisher_name = "Condé Nast"

    print(f"\n--- Magazines Published by {publisher_name} ---")

    cursor.execute(
        """
        SELECT m.magazine_id, m.name, p.name
        FROM magazines AS m
        JOIN publishers AS p
            ON m.publisher_id = p.publisher_id
        WHERE p.name = ?
        ORDER BY m.name
        """,
        (publisher_name,)
    )

    for row in cursor.fetchall():
        print(row)


try:
    conn = sqlite3.connect("../db/magazines.db")
    conn.execute("PRAGMA foreign_keys = 1")
    cursor = conn.cursor()

    print("Database created and connected successfully.")

    try:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS publishers (
                publisher_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE
            )
            """
        )
    except sqlite3.Error as e:
        print(f"Error creating publishers table: {e}")

    try:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS magazines (
                magazine_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                publisher_id INTEGER NOT NULL,
                FOREIGN KEY (publisher_id)
                    REFERENCES publishers (publisher_id)
            )
            """
        )
    except sqlite3.Error as e:
        print(f"Error creating magazines table: {e}")

    try:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS subscribers (
                subscriber_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                address TEXT NOT NULL
            )
            """
        )
    except sqlite3.Error as e:
        print(f"Error creating subscribers table: {e}")

    try:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS subscriptions (
                subscription_id INTEGER PRIMARY KEY,
                subscriber_id INTEGER NOT NULL,
                magazine_id INTEGER NOT NULL,
                expiration_date TEXT NOT NULL,
                UNIQUE (subscriber_id, magazine_id),
                FOREIGN KEY (subscriber_id)
                    REFERENCES subscribers (subscriber_id),
                FOREIGN KEY (magazine_id)
                    REFERENCES magazines (magazine_id)
            )
            """
        )
    except sqlite3.Error as e:
        print(f"Error creating subscriptions table: {e}")

    print("Tables created successfully.")

    # Add publishers
    add_publisher(cursor, "Condé Nast")
    add_publisher(cursor, "Hearst Communications")
    add_publisher(cursor, "National Geographic Partners")

    # Add magazines
    add_magazine(
        cursor,
        "The New Yorker",
        "Condé Nast"
    )

    add_magazine(
        cursor,
        "Cosmopolitan",
        "Hearst Communications"
    )

    add_magazine(
        cursor,
        "National Geographic",
        "National Geographic Partners"
    )

    # Add subscribers
    add_subscriber(
        cursor,
        "Alice Johnson",
        "100 Main Street"
    )

    add_subscriber(
        cursor,
        "Bob Smith",
        "200 Oak Avenue"
    )

    add_subscriber(
        cursor,
        "Carol Davis",
        "300 Pine Road"
    )

    # Add subscriptions
    add_subscription(
        cursor,
        "Alice Johnson",
        "100 Main Street",
        "The New Yorker",
        "2027-08-30"
    )

    add_subscription(
        cursor,
        "Bob Smith",
        "200 Oak Avenue",
        "Cosmopolitan",
        "2027-09-15"
    )

    add_subscription(
        cursor,
        "Carol Davis",
        "300 Pine Road",
        "National Geographic",
        "2027-10-01"
    )

    conn.commit()
    print("Data committed successfully.")

    run_queries(cursor)

except sqlite3.Error as e:
    print(f"Database error: {e}")

finally:
    if "conn" in locals():
        conn.close()
        print("Database connection closed.")