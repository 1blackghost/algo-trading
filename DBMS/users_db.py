import sqlite3


def reset_back_to_start() -> None:
    """
    Reset the database to the initial state.

    This function drops the existing 'users' table and recreates it.

    Note:
        This action requires admin privilege.

    Returns:
        None
    """
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    print("[WARNING!] You need admin privilege to clear and reset the data! Are you sure? (y/n/yes/no)")
    a = input()
    c.execute("DROP TABLE IF EXISTS users")
    if a in ("y", "yes"):
        c.execute('''CREATE TABLE IF NOT EXISTS users
                    (uid INTEGER PRIMARY KEY AUTOINCREMENT,
                     business_name TEXT NOT NULL,
                     email TEXT NOT NULL,
                     mobile_number TEXT NOT NULL,
                     password TEXT NOT NULL,
                     verified INTEGER DEFAULT 0,
                     broker TEXT,
                     method TEXT
                     )''')

    conn.commit()
    c.close()
    conn.close()


def insert_user(business_name="", email="", mobile_number="", password="", verified=0, broker="", method="") -> int:
    """
    Insert a new user into the database.

    Args:
        business_name: Business name of the user.
        email: Email address of the user.
        mobile_number: Mobile number of the user.
        password: Password of the user.
        verified: Verification status of the user.
        broker: Broker of the user (optional).
        method: Method of the user (optional).

    Returns:
        int: ID of the inserted user.
    """
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    if verified != 0:
        verified = 1

    c.execute("INSERT INTO users (business_name, email, mobile_number, password, verified, broker, method) "
              "VALUES (?, ?, ?, ?, ?, ?, ?)",
              (business_name, email, mobile_number, password, verified, broker, method))
    uid = c.lastrowid
    conn.commit()
    c.close()
    conn.close()

    return uid


def update_user(uid, business_name=None, email=None, mobile_number=None, password=None, verified=None, broker=None, method=None) -> None:
    """
    Update user information in the database.

    Args:
        uid: User ID of the user to update.
        business_name: New business name (optional).
        email: New email address (optional).
        mobile_number: New mobile number (optional).
        password: New password (optional).
        verified: New verification status (optional).
        broker: New broker (optional).
        method: New method (optional).

    Returns:
        None
    """
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    update_fields = []

    if business_name is not None:
        update_fields.append(("business_name", business_name))
    if email is not None:
        update_fields.append(("email", email))
    if mobile_number is not None:
        update_fields.append(("mobile_number", mobile_number))
    if password is not None:
        update_fields.append(("password", password))
    if verified is not None:
        update_fields.append(("verified", verified))
    if broker is not None:
        update_fields.append(("broker", broker))
    if method is not None:
        update_fields.append(("method", method))

    if len(update_fields) > 0:
        update_query = "UPDATE users SET "
        update_query += ", ".join(f"{field} = ?" for field, _ in update_fields)
        update_query += " WHERE uid = ?"
        values = [value for _, value in update_fields]
        values.append(uid)
        c.execute(update_query, values)

    conn.commit()
    c.close()
    conn.close()



def read_user(uid=-1) -> list:
    """
    Read user details from the database.

    Args:
        uid: User ID to retrieve. If -1, retrieve all users.

    Returns:
        list: User details as a list of tuples.
    """
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    if uid != -1:
        c.execute("SELECT * FROM users WHERE uid = ?", (uid,))
        result = c.fetchone()
    else:
        c.execute("SELECT * FROM users")
        result = c.fetchall()

    c.close()
    conn.close()

    return result
