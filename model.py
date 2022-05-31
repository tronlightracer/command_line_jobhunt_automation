import argparse
import psycopg2

from psycopg2.errors import UniqueViolation

#create argument parser to add entries via command line DONE for the most part
#create table with psycopg2 for postgres experience

#TODO
#add update functionality
#make it so functions arguments are values taken from the command line

#PLAN
# mabye split up the file so if values are trying to be added you can run one program but if 
# you're trying to interact with the database by updating or deleting rows you have a 
# specific program to call command line arguments with to call

parser = argparse.ArgumentParser(description="get db entries")

parser.add_argument("--company-name", help="the company name of the job you just applied to")
parser.add_argument("--position", help="the position applied to")
parser.add_argument("--moved_on", help="whether the company has said they've moved on with other candidates")
parser.add_argument("--follow_up", help="whether you've done a followup with the company")
parser.add_argument("--reached_out", help="whether the company has reached out to me or not")

args = parser.parse_args()
#print(args)
company_name = args.company_name
position = args.position
moved_on = args.moved_on
follow_up = args.follow_up
reached_out = args.reached_out
#print([company_name, position, moved_on, follow_up, reached_out])

conn = psycopg2.connect(
    database="zougyhdf",
    user="zougyhdf",
    password="password",
    host="heffalump.db.elephantsql.com",
    port="5432",
)
print("Database connected successfully")

cur = conn.cursor()

# drop the table
cur.execute("DROP TABLE IF EXISTS jobhunt")

#creates the table
cur.execute(
    #drop the table so the database table is cleared when running the program
    """
        CREATE TABLE IF NOT EXISTS jobhunt(
        COMPANY TEXT,
        POSITION TEXT,
        MOVED_ON BOOL,
        FOLLOW_UP BOOL,
        REACHED_OUT BOOL
    )"""
)
conn.commit()
print("Table created successfully")


#Inserts data taken from the command line into respective columns
cur.execute("INSERT INTO jobhunt (COMPANY, POSITION, MOVED_ON, FOLLOW_UP, REACHED_OUT) VALUES(%s, %s, %s, %s, %s)",
    (company_name, position, moved_on, follow_up, reached_out)
)
conn.commit()
print("Data inserted successfully.. supposedly\n")

def get_data(company_name):
    conn = psycopg2.connect(
    database="zougyhdf",
    user="zougyhdf",
    password="password",
    host="heffalump.db.elephantsql.com",
    port="5432",
    )
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
#if no argument is passed this still works.. sweet
get_data(company_name)

def del_data(column_name, company_name):
    conn = psycopg2.connect(
    database="zougyhdf",
    user="zougyhdf",
    password="password",
    host="heffalump.db.elephantsql.com",
    port="5432",
    )
    cur = conn.cursor()
    #deletes a row where the condition is true. 'WHERE' is the condition or if statement essentially
    cur.execute(f"DELETE FROM jobhunt WHERE {column_name}='{company_name}'")
    print(f"The rows affected are: {cur.rowcount}")
    conn.commit()

#del_data("COMPANY", "Google")

def update_data(column_name, company_name, position, moved_on, follow_up, reached_out):
    conn = psycopg2.connect(
        database="zougyhdf",
        user="zougyhdf",
        password="password",
        host="heffalump.db.elephantsql.com",
        port="5432",
    )
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

#update_data("COMPANY", "Google", "QA-engineer", None, None, None)
update_data("COMPANY", "Google", "QA", True, None, None)

conn.close()