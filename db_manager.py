import mysql.connector
import hashlib

# TODO: SEPARAR EM OUTRO ARQUIVO
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="secure_pass"
)

db_cursor = conn.cursor()


def user_exists(cursor, username):
    consult = "SELECT COUNT(*) FROM user WHERE username = %s"
    cursor.execute(consult, (username,))
    count = cursor.fetchone()[0]
    return count > 0


def create_user_table(cursor):
    consult = """
        CREATE TABLE IF NOT EXISTS user(
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255),
            password VARCHAR(255)
        )
    """
    cursor.execute(consult)


def hash_password(password):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(password.encode('utf-8'))
    return hash_algorithm.hexdigest()


def create_user(cursor, username, password):
    if user_exists(cursor, username):
        print(f"User '{username}' already exists.")
    else:
        hashed_password = hash_password(password)
        consult = f"INSERT INTO user (username, password) VALUES (%s, %s)"
        cursor.execute(consult, (username, hashed_password))
        print('Created')


def login(cursor, username, password):
    if not user_exists(cursor, username):
        print(f"O usuário '{username}' não existe.")
        return False

    consult = "SELECT password FROM user WHERE username = %s"
    cursor.execute(consult, (username,))
    hashed_password = cursor.fetchone()[0]

    input_hashed_password = hash_password(password)

    if hashed_password == input_hashed_password:
        print("Login bem sucedido.")
        return True
    else:
        print("Senha incorreta.")
        return False


# create_user_table(db_cursor)
login(db_cursor, 'Zenith', 'kae')
conn.commit()
conn.close()
