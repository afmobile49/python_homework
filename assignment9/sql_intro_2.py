import sqlite3
import pandas as pd


try:
    with sqlite3.connect("../db/lesson.db") as conn:
        sql_query = """
        SELECT
            line_items.line_item_id,
            line_items.quantity,
            products.product_id,
            products.product_name,
            products.price
        FROM line_items
        JOIN products
            ON line_items.product_id = products.product_id
        """

        df = pd.read_sql_query(sql_query, conn)

        print("--- First 5 Rows ---")
        print(df.head())

        df["total"] = df["quantity"] * df["price"]

        print("\n--- First 5 Rows with Total ---")
        print(df.head())

        summary_df = (
            df.groupby("product_id")
            .agg({
                "line_item_id": "count",
                "total": "sum",
                "product_name": "first"
            })
            .reset_index()
        )

        print("\n--- Product Summary ---")
        print(summary_df.head())

        summary_df = summary_df.sort_values(by="product_name")

        print("\n--- Product Summary Sorted by Name ---")
        print(summary_df.head())

        summary_df.to_csv("order_summary.csv", index=False)

        print("\norder_summary.csv created successfully.")

except sqlite3.Error as e:
    print(f"Database error: {e}")
except Exception as e:
    print(f"Error: {e}")
