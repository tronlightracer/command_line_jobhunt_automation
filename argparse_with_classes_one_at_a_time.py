import argparse
import psycopg2


def argparsed():
    parser = argparse.ArgumentParser(description="get db entries")
    parser.add_argument("--company_name", help="the company name of the job you just applied to")
    parser.add_argument("--position", help="the position applied to")
    parser.add_argument("--moved_on", help="whether the company has said they've moved on with other candidates")
    parser.add_argument("--follow_up", help="whether you've done a followup with the company")
    parser.add_argument("--reached_out", help="whether the company has reached out to me or not")
    args = parser.parse_args()

    company_name = args.company_name
    position = args.position
    moved_on = args.moved_on
    follow_up = args.follow_up
    reached_out = args.reached_out

    return company_name, position, moved_on, follow_up, reached_out


argparser = argparsed()


class DataBase:
    conn = None
    cur = None

    def __init__(self):
        if DataBase.conn is None:
            try:

                DataBase.conn = psycopg2.connect(
                    database="zougyhdf",
                    user="zougyhdf",
                    password="IB_jCFj_1SDyLeRlMasIq5bQV2x3UpEJ",
                    host="heffalump.db.elephantsql.com",
                    port="5432",
                )
                DataBase.cur = DataBase.conn.cursor()
            except Exception as error:
                print(f"Error: Connection not established {error}")
            else:
                print("Connection Established")

    def drop_table(self):
        DataBase.cur.execute("DROP TABLE IF EXISTS jobhunt")
        DataBase.conn.commit()
        print("Table Dropped")
    
    def create_table(self):
        DataBase.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS jobhunt(
            COMPANY TEXT UNIQUE,
            POSITION TEXT,
            MOVED_ON BOOL,
            FOLLOW_UP BOOL,
            REACHED_OUT BOOL
        )"""
        )
        DataBase.conn.commit()
        print("Table Created")

    def insert_data(self):
        DataBase.cur.execute(
            "INSERT INTO jobhunt (COMPANY, POSITION, MOVED_ON, FOLLOW_UP, REACHED_OUT) VALUES(%s, %s, %s, %s, %s)",
            (
                argparser[0],
                argparser[1],
                argparser[2],
                argparser[3],
                argparser[4],
            ),
        )
        DataBase.conn.commit()
        print("Data inserted successfully")
    
    def get_all_data(self):
        DataBase.cur.execute("SELECT * FROM jobhunt")
        print("Data Got")
    
    def get_data(self, company_name):
        # for whatever reason you need to put single qoutes around the format curly braces
        DataBase.cur.execute(
            f"SELECT COMPANY, POSITION, MOVED_ON, FOLLOW_UP, REACHED_OUT FROM jobhunt WHERE COMPANY='{company_name}'"
        )
        DataBase.conn.commit()
        rows = DataBase.cur.fetchall()
        for row in rows:
            print(f"Company name: {row[0]}")
            print(f"Position: {row[1]}")
            print(f"Moved on or not: {row[2]}")
            print(f"If you've followed up with the company: {row[3]}")
            print(f"Reached out or not: {row[4]}")
    
    def update_data(
        self, column_name, company_name, position, moved_on, follow_up, reached_out
    ):
        if position:
            DataBase.cur.execute(
                f"UPDATE jobhunt SET POSITION='{position}' WHERE {column_name}='{company_name}'"
            )
            print(f"updated position for row {company_name}")
        elif moved_on:
            DataBase.cur.execute(
                f"UPDATE jobhunt SET MOVED_ON={moved_on} WHERE {column_name}='{company_name}'"
            )
            print(f"updated moved_on column for  row {company_name}")
        elif follow_up:
            DataBase.cur.execute(
                f"UPDATE jobhunt SET FOLLOW_UP={follow_up} WHERE {column_name}='{company_name}'"
            )
            print("updated follow_up column for row {company_name}")
        elif reached_out:
            DataBase.cur.execute(
                f"UPDATE jobhunt SET REACHED_OUT={reached_out} WHERE {column_name}='{company_name}'"
            )
            print("updated reached out column for row {company_name}")
    
    def del_data(self, column_name, company_name):
        # deletes a row where the condition is true. 'WHERE' is the condition or if statement essentially
        DataBase.cur.execute(f"DELETE FROM jobhunt WHERE {column_name}='{company_name}'")
        print(f"The rows affected are: {DataBase.cur.rowcount}")
        DataBase.conn.commit()


database = DataBase()
database.drop_table()
database.create_table()
database.insert_data()
database.get_all_data()
# must either have Trevor as a company name or if dropping the table beforehand
# call "Trevor" as a company name
database.get_data("Trevor")
database.update_data("COMPANY", "Trevor", "trev", "trev", None, None)
database.del_data("COMPANY", "Trevor")