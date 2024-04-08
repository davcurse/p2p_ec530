import sqlite3


def clear_database(db_file):

    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # Get the list of table names in the database
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in c.fetchall()]

    verify = input("Are you sure you want to clean the database? (y/n) ")
    # Iterate over each table and delete all records
    if verify == 'y':
        for table in tables:
            c.execute(f"DELETE FROM {table}")
            if table != "sqlite_sequence":
                print(f"Cleared table: {table}")
        print("Database cleared successfully.")
    else:
        print("Aborting full clean.")

    # Commit the changes and close the connection end the logging
    conn.commit()
    conn.close()


clear_database('chat_database.db')
