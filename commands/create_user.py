import argparse
from getpass import getpass
from project.database import SESSION
import hashlib
def create_user(email, password):
    if '@' not in email:
        raise Exception(f'Invalid email <{email}>')
    password_encode = hashlib.sha256(password.encode('utf-8'))
    password_digest = password_encode.hexdigest()
    SESSION.execute(f'''
        INSERT INTO
            USERS (
                EMAIL,
                PASSWORD
            )
        VALUES
            (
                '{email}',
                '{password_digest}'
            );
    ''')
    SESSION.commit()
if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description='Process some integers.')
    PARSER.add_argument('-u', dest='email', type=str, required=True)
    PARSER.add_argument('-p', '--password', action='store_true', dest='password', 
                        help='hidden password prompt', default='')
    ARGS=PARSER.parse_args()
    if ARGS.password:
        PASSWORD = getpass()
        ARGS.password = PASSWORD
    create_user(ARGS.email, ARGS.password)