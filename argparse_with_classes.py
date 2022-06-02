import argparse
import psycopg2


class ArgParsed:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="get db entries")
        self.parser.add_argument(
            "--company_name", help="The company name you've applied to"
        )
        self.parser.add_argument("--position", help="Position applied to")
        self.parser.add_argument("--moved_on", help="Whether the company has moved on")
        self.parser.add_argument(
            "--follow_up", help="Whether you've done a follow up or not"
        )
        self.parser.add_argument(
            "--reached_out", help="Whether the company has reached out or not"
        )

        args = self.parser.parse_args()
        self.company_name = args.company_name
        self.position = args.position
        self.moved_on = args.moved_on
        self.follow_up = args.follow_up
        self.reached_out = args.reached_out

    def __new__(self):
        return [
            self.company_name,
            self.position,
            self.moved_on,
            self.follow_up,
            self.reached_out,
        ]


argparsed = ArgParsed()


class DataBase:
    conn = None
    cur = None

    def __init__(self):
        if DataBase.conn is None:
            try:
                DataBase.conn = psycopg2.connect(
                    database="zougyhdf",
                    user="zougyhdf",
                    password="password",
                    host="heffalump.db.elephantsql.com",
                    port="5432",
                )
                DataBase.cur = conn.cursor()
            except Exception as error:
                print(f"Error: Connection not established {error}")
            else:
                print("Connection Established")

    def drop_table(self):
        cur.execute("DROP TABLE jobhunt")
        conn.commit()

    def create_table(self):
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS jobhunt(
            COMPANY TEXT UNIQUE,
            POSITION TEXT,
            MOVED_ON BOOL,
            FOLLOW_UP BOOL,
            REACHED_OUT BOOL
        )"""
        )
        conn.commit()

    def insert_data(self):
        cur.execute(
            "INSERT INTO jobhunt (COMPANY, POSITION, MOVED_ON, FOLLOW_UP, REACHED_OUT) VALUES(%s, %s, %s, %s, %s)",
            (
                ArgParsed.__new__()[0],
                ArgParsed.__new__()[1],
                ArgParsed.__new__()[2],
                ArgParsed.__new__()[3],
                ArgParsed.__new__()[4],
            ),
        )
        conn.commit()

    def get_all_data(self):
        cur.execute("SELECT * FROM jobhunt")

    def get_data(self, company_name):
        # for whatever reason you need to put single qoutes around the format curly braces
        cur.execute(
            f"SELECT COMPANY, POSITION, MOVED_ON, FOLLOW_UP, REACHED_OUT FROM jobhunt WHERE COMPANY='{company_name}'"
        )
        conn.commit()
        rows = cur.fetchall()
        for row in rows:
            print(f"Company name: {row[0]}")
            print(f"Position: {row[1]}")
            print(f"Moved on or not: {row[2]}")
            print(f"If you've followed up with the company: {row[3]}")
            print(f"Reached out or not: {row[4]}")

    # if no argument is passed on the command line this still works as there's a placeholder value of None
    # get_data(argparsed()[0])

    def update_data(
        self, column_name, company_name, position, moved_on, follow_up, reached_out
    ):
        if position:
            cur.execute(
                f"UPDATE jobhunt SET POSITION='{position}' WHERE {column_name}='{company_name}'"
            )
            print(f"updated position for row {company_name}")
        elif moved_on:
            cur.execute(
                f"UPDATE jobhunt SET MOVED_ON={moved_on} WHERE {column_name}='{company_name}'"
            )
            print(f"updated moved_on column for  row {company_name}")
        elif follow_up:
            cur.execute(
                f"UPDATE jobhunt SET FOLLOW_UP={follow_up} WHERE {column_name}='{company_name}'"
            )
            print("updated follow_up column for row {company_name}")
        elif reached_out:
            cur.execute(
                f"UPDATE jobhunt SET REACHED_OUT={reached_out} WHERE {column_name}='{company_name}'"
            )
            print("updated reached out column for row {company_name}")

    def del_data(column_name, company_name):
        # deletes a row where the condition is true. 'WHERE' is the condition or if statement essentially
        cur.execute(f"DELETE FROM jobhunt WHERE {column_name}='{company_name}'")
        print(f"The rows affected are: {cur.rowcount}")
        conn.commit()
