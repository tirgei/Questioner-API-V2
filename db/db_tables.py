from werkzeug.security import generate_password_hash

tables = [
    'users',
    'meetups',
    'questions',
    'comments',
    'rsvps',
    'votes',
    'revoked_tokens'
]

create_table_queries = [
    """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY NOT NULL,
        firstname VARCHAR(250) NOT NULL,
        lastname VARCHAR(250) NOT NULL,
        othername VARCHAR(250) NULL,
        username VARCHAR(250) NOT NULL,
        phonenumber VARCHAR(250) NULL,
        email VARCHAR(250) NOT NULL,
        password VARCHAR(250) NOT NULL,
        registered TIMESTAMP WITHOUT TIME ZONE \
        DEFAULT (NOW() AT TIME ZONE 'utc'),
        admin BOOLEAN NOT NULL DEFAULT FALSE
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS meetups (
        id SERIAL PRIMARY KEY NOT NULL,
        topic VARCHAR(250) NOT NULL,
        description VARCHAR(250) NOT NULL,
        location VARCHAR(250) NOT NULL,
        happening_on VARCHAR(250) NOT NULL,
        tags VARCHAR [],
        created_at TIMESTAMP WITHOUT TIME ZONE \
        DEFAULT (NOW() AT TIME ZONE 'utc'),
        modified_at TIMESTAMP WITHOUT TIME ZONE \
        DEFAULT (NOW() AT TIME ZONE 'utc')
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS questions (
        id SERIAL PRIMARY KEY NOT NULL,
        title VARCHAR(250) NULL,
        body VARCHAR(250) NOT NULL,
        votes INTEGER NOT NULL DEFAULT 0,
        meetup_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        created_at TIMESTAMP WITHOUT TIME ZONE \
        DEFAULT (NOW() AT TIME ZONE 'utc'),
        modified_at TIMESTAMP WITHOUT TIME ZONE \
        DEFAULT (NOW() AT TIME ZONE 'utc'),
        FOREIGN KEY (meetup_id) REFERENCES meetups(id),
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS comments (
        id SERIAL PRIMARY KEY NOT NULL,
        body VARCHAR(250) NULL,
        question_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        created_at TIMESTAMP WITHOUT TIME ZONE \
        DEFAULT (NOW() AT TIME ZONE 'utc'),
        modified_at TIMESTAMP WITHOUT TIME ZONE \
        DEFAULT (NOW() AT TIME ZONE 'utc'),
        FOREIGN KEY (question_id) REFERENCES questions(id),
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS rsvps (
        meetup_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        response VARCHAR(10),
        created_at TIMESTAMP WITHOUT TIME ZONE \
        DEFAULT (NOW() AT TIME ZONE 'utc'),
        modified_at TIMESTAMP WITHOUT TIME ZONE \
        DEFAULT (NOW() AT TIME ZONE 'utc'),
        PRIMARY KEY (meetup_id, user_id)
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS votes (
        question_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        vote VARCHAR(10),
        PRIMARY KEY (question_id, user_id)
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS revoked_tokens (
        id SERIAL PRIMARY KEY NOT NULL,
        jti VARCHAR NOT NULL
    )
    """
]


def truncate(connection):
    """ Function to truncate database tables """

    cur = connection.cursor()
    cur.execute('TRUNCATE TABLE ' + ','.join(tables) + ' CASCADE')
    connection.commit()


def drop_tables(connection):
    """ Function to drop tables """

    cur = connection.cursor()
    for table in tables:
        cur.execute('DROP TABLE IF EXISTS {} CASCADE'.format(table))

    connection.commit()


def create_tables(connection):
    """ Function to create tables """

    cur = connection.cursor()
    for query in create_table_queries:
        cur.execute(query)

    connection.commit()


def seed(connection):
    cur = connection.cursor()

    user_query = "SELECT * FROM users WHERE username = 'tirgei'"
    cur.execute(user_query)
    result = cur.fetchone()

    if not result:
        cur.execute("INSERT INTO users (firstname, lastname, username, email, password, admin)\
        VALUES ('Vincent', 'Tirgei', 'tirgei', 'admin@app.com', '{}', True)\
        ".format(generate_password_hash('asf8$#Er0')))
        connection.commit()
