import sqlite3


# Task 1: Complex JOINs with Aggregation

conn = sqlite3.connect("../db/lesson.db")
cursor = conn.cursor()

query = """
SELECT o.order_id,
       SUM(p.price * li.quantity) AS total_price
FROM orders AS o
JOIN line_items AS li
    ON o.order_id = li.order_id
JOIN products AS p
    ON li.product_id = p.product_id
GROUP BY o.order_id
ORDER BY o.order_id
LIMIT 5;
"""

cursor.execute(query)
results = cursor.fetchall()

for order_id, total_price in results:
    print(order_id, total_price)



# Task 2: Understanding Subqueries

query = """
SELECT c.customer_name,
       AVG(order_totals.total_price) AS average_total_price
FROM customers AS c
LEFT JOIN (
    SELECT o.customer_id AS customer_id_b,
           SUM(p.price * li.quantity) AS total_price
    FROM orders AS o
    JOIN line_items AS li
        ON o.order_id = li.order_id
    JOIN products AS p
        ON li.product_id = p.product_id
    GROUP BY o.order_id, o.customer_id
) AS order_totals
    ON c.customer_id = order_totals.customer_id_b
GROUP BY c.customer_id, c.customer_name;
"""

cursor.execute(query)
results = cursor.fetchall()

for customer_name, average_total_price in results:
    print(customer_name, average_total_price)


# Task 3: An Insert Transaction Based on Data

conn.execute("PRAGMA foreign_keys = 1")

try:
    # Find the customer_id for Perez and Sons
    cursor.execute(
        """
        SELECT customer_id
        FROM customers
        WHERE customer_name = ?;
        """,
        ("Perez and Sons",),
    )
    customer_id = cursor.fetchone()[0]

    # Find the employee_id for Miranda Harris
    cursor.execute(
        """
        SELECT employee_id
        FROM employees
        WHERE first_name = ?
          AND last_name = ?;
        """,
        ("Miranda", "Harris"),
    )
    employee_id = cursor.fetchone()[0]

    # Find the 5 least expensive products
    cursor.execute(
        """
        SELECT product_id
        FROM products
        ORDER BY price ASC
        LIMIT 5;
        """
    )
    product_ids = [row[0] for row in cursor.fetchall()]

    # Create the new order
    cursor.execute(
        """
        INSERT INTO orders (customer_id, employee_id, date)
        VALUES (?, ?, date('now'))
        RETURNING order_id;
        """,
        (customer_id, employee_id),
    )
    order_id = cursor.fetchone()[0]

    # Add 10 of each of the 5 least expensive products
    for product_id in product_ids:
        cursor.execute(
            """
            INSERT INTO line_items (order_id, product_id, quantity)
            VALUES (?, ?, ?);
            """,
            (order_id, product_id, 10),
        )

    conn.commit()

except Exception:
    conn.rollback()
    raise

# Print the line items for the new order
cursor.execute(
    """
    SELECT li.line_item_id,
           li.quantity,
           p.product_name
    FROM line_items AS li
    JOIN products AS p
        ON li.product_id = p.product_id
    WHERE li.order_id = ?
    ORDER BY li.line_item_id;
    """,
    (order_id,),
)

results = cursor.fetchall()

for line_item_id, quantity, product_name in results:
    print(line_item_id, quantity, product_name)


# Task 4: Aggregation with HAVING

query = """
SELECT e.employee_id,
       e.first_name,
       e.last_name,
       COUNT(o.order_id) AS order_count
FROM employees AS e
JOIN orders AS o
    ON e.employee_id = o.employee_id
GROUP BY e.employee_id, e.first_name, e.last_name
HAVING COUNT(o.order_id) > 5
ORDER BY e.employee_id;
"""

cursor.execute(query)
results = cursor.fetchall()

for employee_id, first_name, last_name, order_count in results:
    print(employee_id, first_name, last_name, order_count)

conn.close()