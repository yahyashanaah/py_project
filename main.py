import sqlite3

# Connect to SQLite database (it will create a database file if it doesn't exist)
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# Create a table
def create_table():
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        age INTEGER NOT NULL,
                        email TEXT UNIQUE NOT NULL)''')
    conn.commit()

# Insert data (Create)
def insert_user(name, age, email):
    try:
        cursor.execute("INSERT INTO users (name, age, email) VALUES (?, ?, ?)", (name, age, email))
        conn.commit()
        print(f"User '{name}' added successfully.")
    except sqlite3.IntegrityError as e:
        print(f"Error: {e}")

# Read data
def read_users():
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    print("Users:")
    for row in rows:
        print(row)

# Update data
def update_user(user_id, name=None, age=None, email=None):
    fields = []
    values = []
    if name:
        fields.append("name = ?")
        values.append(name)
    if age:
        fields.append("age = ?")
        values.append(age)
    if email:
        fields.append("email = ?")
        values.append(email)
    
    if fields:
        query = f"UPDATE users SET {', '.join(fields)} WHERE id = ?"
        values.append(user_id)
        cursor.execute(query, values)
        conn.commit()
        print(f"User ID '{user_id}' updated successfully.")

# Delete data
def delete_user(user_id):
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    print(f"User ID '{user_id}' deleted successfully.")

# Example usage:
create_table()
insert_user("Alice", 30, "alice@example.com")
insert_user("Bob", 25, "bob@example.com")
read_users()
update_user(1, age=31)  # Update Alice's age
read_users()
delete_user(2)  # Delete Bob
read_users()

# Close the connection when done
conn.close()
