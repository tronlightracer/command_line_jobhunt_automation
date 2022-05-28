import argparse
import psycopg2

#create argument parser to add entries via command line DONE for the most part
#create table with psycopg2 for postgres experience

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
    password="IB_jCFj_1SDyLeRlMasIq5bQV2x3UpEJ",
    host="heffalump.db.elephantsql.com",
    port="5432",
)
print("Database connected successfully")

cur = conn.cursor()

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
    password="IB_jCFj_1SDyLeRlMasIq5bQV2x3UpEJ",
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

def del_data(column_name, item):
    conn = psycopg2.connect(
    database="zougyhdf",
    user="zougyhdf",
    password="IB_jCFj_1SDyLeRlMasIq5bQV2x3UpEJ",
    host="heffalump.db.elephantsql.com",
    port="5432",
    )
    cur = conn.cursor()
    #deletes a row where the condition is true. 'WHERE' is the condition or if statement essentially
    cur.execute(f"DELETE FROM jobhunt WHERE {column_name}='{item}'")
    print(f"The rows affected are: {cur.rowcount}")
    conn.commit()

del_data("COMPANY", "Google")
print("Data deleted successfully")
#the function above does the same thing but dynamically
# cur.execute(f"SELECT COMPANY, POSITION, MOVED_ON, FOLLOW_UP, REACHED_OUT FROM jobhunt WHERE COMPANY='Aevum'")
# conn.commit()

# # one way to get the info though I'd prefer to find a more controllable way
# rows = cur.fetchall()
# for row in rows:
#     print(f"Company name: {row[0]}")
#     print(f"Position: {row[1]}")
#     print(f"Moved on or not: {row[2]}")
#     print(f"If you've followed up with the company: {row[3]}")
#     print(f"Reached out or not: {row[4]}")


# cur.execute("SELECT * FROM jobhunt")
# conn.commit()
conn.close()