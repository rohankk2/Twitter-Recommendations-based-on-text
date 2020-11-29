import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = r"/Users/cesiabulnes/Desktop/CS410/final_project/Twitter-Recommendations-based-on-text/db/pythonsqlite.db"

    sql_originaltweets_table = """CREATE TABLE IF NOT EXISTS projects (
                                        id text PRIMARY KEY,
                                        tweet_text text, 
                                        created_at text,
                                        author_id text,
                                        conversation_id text,
                                        in_reply_to_user_id text,
                                        referenced_tweets text,
                                        referenced_tweets.type text,
                                        referenced_tweets.id text,
                                        attachments text,
                                        attachments.media_keys text, 
                                        attachments.poll_ids text,
                                        geo text,
                                        geo.coordinates text,
                                        geo.coordinates.type text,
                                        geo.coordinates.coordinates text, 
                                        geo.place_id text,
                                        context_annotations text,
                                        context_annotations.domain text,
                                        context_annotations.domain.id text,
                                        context_annotations.domain.name text,
                                        context_annotations.domain.description text,
                                        context_annotations.entity text,
                                        context_annotations.entity.id text,
                                        context_annotations.entity.name text,
                                        context_annotations.entity.description text,
                                        entities text,
                                        entities.annotations text,
                                        entities.annotations.probability integer,
                                        entities.annotations.type text,
                                        entities.annotations.normalized_text text,
                                        entities.hashtags text,
                                        entities.hashtags.tag text,
                                        organic_metrics text,
                                        
                        
                                        name text NOT NULL,
                                        begin_date text,
                                        end_date text
                                    );"""

    # for referenced tweets use json encode/decode forgot which one

    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_originaltweets_table)

    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    # create_connection(r"/Users/cesiabulnes/Desktop/CS410/final_project/Twitter-Recommendations-based-on-text/db/pythonsqlite.db")
    main()