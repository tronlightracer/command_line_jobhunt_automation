import argparse
import psycopg2

from psycopg2.errors import UniqueViolation

#create argument parser to add entries via command line DONE for the most part
#create table with psycopg2 for postgres experience

#TODO
#add update functionality DONE
#make it so functions arguments are values taken from the command line

#PLAN
# mabye split up the file so if values are trying to be added you can run one program but if 
# you're trying to interact with the database by updating or deleting rows you have a 
# specific program to call command line arguments with to call

def make_connection():
    conn = "string_data"
    return conn

def drop_table():
    conn = make_connection()
    cur = conn.cursor()
    cur.execute("DROP TABLE jobhunt")

#drop_table()

def create_table():
    conn = make_connection()
    cur = conn.cursor()
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

create_table()


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

def insert_data():
    conn = make_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO jobhunt (COMPANY, POSITION, MOVED_ON, FOLLOW_UP, REACHED_OUT) VALUES(%s, %s, %s, %s, %s)",
        (argparsed()[0], argparsed()[1], argparsed()[2], argparsed()[3], argparsed()[4])
    )
    conn.commit()

insert_data()

def get_all_data():
    conn = make_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM jobhunt")


def get_data(company_name):
    conn = make_connection()
    cur = conn.cursor()
    # for whatever reason you need to put single qoutes around the format curly braces
    cur.execute(f"SELECT COMPANY, POSITION, MOVED_ON, FOLLOW_UP, REACHED_OUT FROM jobhunt WHERE COMPANY='{company_name}'")
    conn.commit()
    rows = cur.fetchall()
    for row in rows:
        print(f"Company name: {row[0]}")
        print(f"Position: {row[1]}")
        print(f"Moved on or not: {row[2]}")
        print(f"If you've followed up with the company: {row[3]}")
        print(f"Reached out or not: {row[4]}")
#if no argument is passed on the command line this still works as there's a placeholder value of None
#get_data(argparsed()[0])

def update_data(column_name, company_name, position, moved_on, follow_up, reached_out):
    conn = make_connection()
    cur = conn.cursor()
    
    if position:
        cur.execute(f"UPDATE jobhunt SET POSITION='{position}' WHERE {column_name}='{company_name}'")
        print(f"updated position for row {company_name}")
    elif moved_on:
        cur.execute(f"UPDATE jobhunt SET MOVED_ON={moved_on} WHERE {column_name}='{company_name}'")
        print(f"updated moved_on column for  row {company_name}")
    elif follow_up:
        cur.execute(f"UPDATE jobhunt SET FOLLOW_UP={follow_up} WHERE {column_name}='{company_name}'")
        print("updated follow_up column for row {company_name}")
    elif reached_out:
        cur.execute(f"UPDATE jobhunt SET REACHED_OUT={reached_out} WHERE {column_name}='{company_name}'")
        print("updated reached out column for row {company_name}")

update_data("COMPANY", argparsed()[0], argparsed()[1], argparsed()[2], argparsed()[3], argparsed()[4])

def del_data(column_name, company_name):
    conn = make_connection()
    cur = conn.cursor()
    #deletes a row where the condition is true. 'WHERE' is the condition or if statement essentially
    cur.execute(f"DELETE FROM jobhunt WHERE {column_name}='{company_name}'")
    print(f"The rows affected are: {cur.rowcount}")
    conn.commit()