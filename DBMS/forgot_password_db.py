import sqlite3


def reset_back_to_start() -> None:
    """
    Reset the database to the initial state.

    This function drops the existing 'forgot_password' table and recreates it.

    Note:
        This action requires admin privilege.

    Returns:
        None
    """
    conn = sqlite3.connect('forgot_password.db')
    c = conn.cursor()

    print("[WARNING!] You need admin privilege to clear and reset the data! Are you sure? (y/n/yes/no)")
    a = input()
    c.execute("DROP TABLE IF EXISTS forgot_password")
    if a in ("y", "yes"):
        c.execute('''CREATE TABLE IF NOT EXISTS forgot_password
                    (uid INTEGER PRIMARY KEY,
                     name TEXT NOT NULL,
                     email TEXT NOT NULL,
                     mobile TEXT NOT NULL,
                     otp TEXT NOT NULL
                     )''')

    conn.commit()
    c.close()
    conn.close()


def update_user(uid, name=None, email=None, mobile=None, otp=None) -> None:
    """
    Update user information in the database.

    Args:
        uid: User ID of the user to update.
        name: New name (optional).
        email: New email address (optional).
        mobile: New mobile number (optional).
        otp: New OTP (optional).

    Returns:
        None
    """
    conn = sqlite3.connect('forgot_password.db')
    c = conn.cursor()
    update_fields = []

    if name is not None:
        update_fields.append(("name", name))
    if email is not None:
        update_fields.append(("email", email))
    if mobile is not None:
        update_fields.append(("mobile", mobile))
    if otp is not None:
        update_fields.append(("otp", otp))

    if len(update_fields) > 0:
        update_query = "UPDATE forgot_password SET "
        update_query += ", ".join(f"{field} = ?" for field, _ in update_fields)
        update_query += " WHERE uid = ?"
        values = [value for _, value in update_fields]
        values.append(uid)
        c.execute(update_query, values)

    conn.commit()
    c.close()
    conn.close()


def insert_user(uid,name="", email="", mobile="", otp="") -> int:
    """
    Insert a new user into the database.

    Args:
        name: Name of the user.
        email: Email address of the user.
        mobile: Mobile number of the user.
        otp: OTP (One-Time Password) of the user.

    Returns:
        int: ID of the inserted user.
    """
    conn = sqlite3.connect('forgot_password.db')
    c = conn.cursor()

    try:
        c.execute("INSERT INTO forgot_password (uid,name, email, mobile, otp) VALUES (?,?, ?, ?, ?)",
              (uid,name, email, mobile, otp))
        conn.commit()
        c.close()
        conn.close()
    except:
        conn.commit()
        c.close()
        conn.close()
        delete_user(uid,name,email,mobile,otp)
    return 


def read_user(uid=-1) -> list:
    """
    Read user details from the database.

    Args:
        uid: User ID to retrieve. If -1, retrieve all users.

    Returns:
        list: User details as a list of tuples.
    """
    conn = sqlite3.connect('forgot_password.db')
    c = conn.cursor()

    if uid != -1:
        c.execute("SELECT * FROM forgot_password WHERE uid = ?", (uid,))
        result = c.fetchone()
    else:
        c.execute("SELECT * FROM forgot_password")
        result = c.fetchall()

    c.close()
    conn.close()

    return result


def delete_user(uid,name,email,mobile,otp):
    """
    Delete a user record from the database.

    Args:
        uid: User ID of the record to delete.

    Returns:
        None
    """
    conn = sqlite3.connect('forgot_password.db')
    c = conn.cursor()

    c.execute("DELETE FROM forgot_password WHERE uid = ?", (uid,))
    conn.commit()

    c.close()
    conn.close()
    insert_user(uid,name,email,mobile,otp)