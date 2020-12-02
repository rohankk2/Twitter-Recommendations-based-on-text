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
    #if you need to change the db path here you go
    database = r"/Users/cesiabulnes/Desktop/CS410/final_project/Twitter-Recommendations-based-on-text/db/pythonsqlite.db"

    sql_original_tweets_table = """CREATE TABLE IF NOT EXISTS originalTweets (
                                        id text PRIMARY KEY,
                                        tweet_text text, 
                                        created_at text,
                                        author_id text,
                                        conversation_id text,
                                        context_annotations text,
                                        context_annotations_domain text,
                                        context_annotations_domain_id text,
                                        context_annotations_domain_name text,
                                        context_annotations_domain_description text,
                                        context_annotations_entity text,
                                        context_annotations_entity_id text,
                                        context_annotations_entity_name text,
                                        context_annotations_entity_description text,
                                        entities text,
                                        entities_annotations text,
                                        entities_annotations_start integer,
                                        entities_annotations_end integer,
                                        entities_annotations_probability real,
                                        entities_annotations_type text,
                                        entities_annotations_normalized_text text,                                
                                        public_metrics text,
                                        public_metrics_retweet_count integer,
                                        public_metrics_reply_count integer,
                                        public_metrics_like_count integer
                                    );"""

    #                       in_reply_to_user_id text, public_metrics_quote_count integer,
    # referenced_tweets text, lang text,possibly_sensitive text,
    #                                         source text,
    #                          referenced_tweets_type text,
    #                          referenced_tweets_id text,
    #                         attachments text,
    #                       attachments_media_keys text,
    #                      attachments_poll_ids text,includes text,
    #                                         includes_tweets text,
    #                                         includes_users text,
    #                                         includes_places text,
    #                                         includes_media text,
    #                                         includes_polls text,
    #                                         errors text,                  promoted_metrics text,
    #                                         promoted_metrics_impression_count integer,
    #                                         promoted_metrics_url_link_clicks integer,
    #                                         promoted_metrics_user_profile_clicks integer,
    #                                         promoted_metrics_retweet_count integer,
    #                                         promoted_metrics_reply_count integer,
    #                                         promoted_metrics_like_count integer,   organic_metrics text,
    #                                         organic_metrics_impression_count integer,
    #                                         organic_metrics_url_link_clicks integer,
    #                                         organic_metrics_user_profile_clicks integer,
    #                                         organic_metrics_retweet_count integer,
    #                                         organic_metrics_reply_count integer,
    #                                         organic_metrics_like_count integer,geo text,
    #                                         geo_coordinates text,
    #                                         geo_coordinates_type text,
    #                                         geo_coordinates_coordinates text,
    #                                         geo_place_id text, non_public_metrics text,
    #                                         non_public_metrics_impression_count integer,
    #                                         non_public_metrics_url_link_clicks integer,
    #                                         non_public_metrics_user_profile_clicks integer,
    #                                        withheld text,
    #                                   withheld_copyright text,
    #                                    withheld_country_codes text,
    #                                   withheld_scope text,entities_cashtags text,
    #                                         entities_cashtags_start integer,
    #                                         entities_cashtags_end integer,
    #                                         entities_cashtags_tag text,entities_urls text,
    #                                         entities_urls_start integer,
    #                                         entities_urls_end integer,
    #                                         entities_urls_url text,
    #                                         entities_urls_expanded_url text,
    #                                         entities_urls_display_url text,
    #                                         entities_urls_unwound_url text,
    #                                         entities_hashtags text,
    #                                         entities_hashtags_start integer,
    #                                         entities_hashtags_end integer,
    #                                         entities_hashtags_tag text,
    #                                         entities_mentions text,
    #                                         entities_mentions_start integer,
    #                                         entities_mentions_end integer,
    #                                         entities_mentions_username text,


    sql_processed_tweets_table = """CREATE TABLE IF NOT EXISTS processedTweets (
                                        id text PRIMARY KEY REFERENCES originalTweets (id),
                                        tweet_text text, 
                                        created_at text,
                                        author_id text,
                                        conversation_id text,
                                        context_annotations text,
                                        context_annotations_domain text,
                                        context_annotations_domain_id text,
                                        context_annotations_domain_name text,
                                        context_annotations_domain_description text,
                                        context_annotations_entity text,
                                        context_annotations_entity_id text,
                                        context_annotations_entity_name text,
                                        context_annotations_entity_description text,
                                        entities text,
                                        entities_annotations text,
                                        entities_annotations_start integer,
                                        entities_annotations_end integer,
                                        entities_annotations_probability real,
                                        entities_annotations_type text,
                                        entities_annotations_normalized_text text,                                
                                        public_metrics text,
                                        public_metrics_retweet_count integer,
                                        public_metrics_reply_count integer,
                                        public_metrics_like_count integer
                                    );"""
    #                                         FOREIGN KEY (id) REFERENCES originalTweets (id)
    sql_user_table = """CREATE TABLE IF NOT EXISTS userTable (
                                            user_id integer PRIMARY KEY,
                                            user_id_str text REFERENCES processedTweets (author_id), 
                                            name text,
                                            screen_name text,
                                            followers_count integer, 
                                            friends_count integer,
                                            statuses_count integer
                                        );"""
#       FOREIGN KEY (user_id_str) REFERENCES processedTweets (author_id)derived text,
    #     #                                             url text,location text,
    #     #                                             description text,
    #     #                                             protected text,verified text,
    #                                             created_at text,
    #                                             profile_banner_url text,
    #                                             profile_image_url_https text,
    #                                             default_profile text,
    #                                             default_profile_image text,
    #                                             withheld_in_countries text,
    #                                             withheld_scope text
    #                                             listed_count integer,
    #                                             favourites_count integer,


    sql_user_category_table = """CREATE TABLE IF NOT EXISTS userCategory (
                                            user_id integer PRIMARY KEY,
                                            id_str text REFERENCES userTable (user_id_str), 
                                            name text,
                                            most_common_cat text,
                                            percentage real,
                                            count_of_tw_in_cat integer
                                            

                                        );"""
    # FOREIGN KEY (id_str) REFERENCES userTable (user_id_str)

    sql_tweet_category_table = """CREATE TABLE IF NOT EXISTS tweetCategory (
                                            category_id integer PRIMARY KEY,
                                            category_id_str text, 
                                            category text REFERENCES processedTweets (context_annotations),
                                            count_of_users_per_cat integer
                                            

                                        );"""
    # FOREIGN KEY (category) REFERENCES processedTweets (context_annotations)
    # for referenced tweets use json encode/decode forgot which one

    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_original_tweets_table)
        create_table(conn, sql_processed_tweets_table)
        create_table(conn, sql_user_table)
        create_table(conn, sql_user_category_table)
        create_table(conn, sql_tweet_category_table)




    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    # create_connection(r"/Users/cesiabulnes/Desktop/CS410/final_project/Twitter-Recommendations-based-on-text/db/pythonsqlite.db")
    main()