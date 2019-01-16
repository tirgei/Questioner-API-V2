import argparse
from db.db_config import connect_db
from db.db_tables import create_tables, drop_tables, truncate


def migrate(connection):
    drop_tables(connection)
    create_tables(connection)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Postgres Database management tool for Questioner')

    parser.add_argument(
        '-a', '--action', metavar='[migrate|truncate]', help='Action',
        choices={'migrate', 'truncate'}, const='migrate', nargs='?')

    args = parser.parse_args()

    conn = connect_db()

    if args.action == 'migrate':
        migrate(conn)
    elif args.action == 'truncate':
        truncate(conn)
    else:
        pass

    conn.close()
