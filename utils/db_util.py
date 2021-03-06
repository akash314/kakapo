import sqlite3


def create_connection(db_file):
    """
    Create a database connection to the SQLite database specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)

    return None


def get_all_people(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute('''SELECT full_name, name, n_number,auid, articles FROM person;''')
    rows = cur.fetchall()

    return rows


def update_author(conn, values):
    """
    Update author with new journal ids
    :param conn: the Connection object
    :param values: update params
    :return:
    """
    cur = conn.cursor()
    cur.execute('''UPDATE person SET articles = ? WHERE n_number = ?''', values)
    conn.commit()


def add_uploaded_articles(conn, values):
    """
    Store existing articles pubmed_id and n_number
    :param conn: the Connection object
    :param values: list of pubmed_id, n_number pairs
    :return:
    """
    cur = conn.cursor()
    cur.executemany('''INSERT INTO article ('n_number', 'pubmed_id') VALUES (?, ?)''', values)
    conn.commit()
