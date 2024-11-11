from flask import Flask, request, jsonify
import sqlite3
from functools import wraps

app = Flask(__name__)

# Utility function to connect to the database


def get_db_connection():
    conn = sqlite3.connect('example.db')
    conn.row_factory = sqlite3.Row  # Access rows by name
    return conn


# Decorator to check if a user exists by ID
def user_exists(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = kwargs['user_id']
        conn = get_db_connection()
        user = conn.execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()
        conn.close()
        if user is None:
            return jsonify({"error": "User not found"}), 404
        return f(*args, **kwargs)
    return decorated_function


# Create a table (run once to set up the database)

def create_table():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        age INTEGER NOT NULL,
                        email TEXT UNIQUE NOT NULL)''')
    conn.commit()
    conn.close()


# Route to create a new user (POST)


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')
    email = data.get('email')

    if not name or not age or not email:
        return jsonify({"error": "Missing required fields"}), 400

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO users (name, age, email) VALUES (?, ?, ?)",
        (name, age, email)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "User created successfully"}), 201


# Route to read all users (GET)


@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    users = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return jsonify([dict(user) for user in users])


# Route to read a specific user by ID (GET)


@app.route('/users/<int:user_id>', methods=['GET'])
@user_exists
def get_user(user_id):
    conn = get_db_connection()
    user = conn.execute(
        'SELECT * FROM users WHERE id = ?', (user_id,)
    ).fetchone()
    conn.close()
    return jsonify(dict(user))


# Route to update a user (PUT)


@app.route('/users/<int:user_id>', methods=['PUT'])
@user_exists
def update_user(user_id):
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')
    email = data.get('email')

    conn = get_db_connection()
    conn.execute(
        '''UPDATE users SET name = ?, age = ?, email = ? WHERE id = ?''',
        (name, age, email, user_id)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "User updated successfully"}), 200


# Route to delete a user (DELETE)


@app.route('/users/<int:user_id>', methods=['DELETE'])
@user_exists
def delete_user(user_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "User deleted successfully"}), 200


if __name__ == '__main__':
    create_table()  # Only run once to initialize the database
    app.run(debug=True)
