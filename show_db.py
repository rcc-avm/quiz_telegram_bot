import sqlite3

def show_table_contents():
    conn = sqlite3.connect('quiz_bot.db')
    cursor = conn.cursor()
    
    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    for table in tables:
        table_name = table[0]
        print(f"\nTable: {table_name}")
        print("-" * 50)
        
        # Get all rows from the table
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        # Get column names
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        print("Columns:", ", ".join(column_names))
        
        # Print all rows
        for row in rows:
            print(row)
    
    conn.close()

if __name__ == "__main__":
    show_table_contents()
