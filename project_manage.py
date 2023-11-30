# import database module
from database import Database, Table
from helper import login, write_csv
import csv
# define a funcion called initializing

# Initialize database for collect information
db1 = Database("db1")
def initializing():

    # Add all necessary table from csv file
    db1.add_csv_table("persons.csv")
    db1.add_csv_table("login.csv")
    db1.add_csv_table("project.csv")
    db1.add_csv_table("pending_advisor.csv")
    db1.add_csv_table("pending_member.csv")
    db1.add_csv_table("pending_approve.csv")
    db1.add_csv_table("pending_eval.csv")




# define a function called exit
def exit():

    # Write each table back to csv file to update new information for each session.
    write_csv("persons.csv", list(db1.search("persons.csv").table[0].keys()), db1.search("persons.csv").table)
    write_csv("login.csv", list(db1.search("login.csv").table[0].keys()), db1.search("login.csv").table)
    write_csv("project.csv", list(db1.search("project.csv").table[0].keys()), db1.search("project.csv").table)
    write_csv("pending_advisor.csv", list(db1.search("pending_advisor.csv").table[0].keys()), db1.search("pending_advisor.csv").table)
    write_csv("pending_member.csv", list(db1.search("pending_member.csv").table[0].keys()), db1.search("pending_member.csv").table)
    write_csv("pending_approve.csv", list(db1.search("pending_approve.csv").table[0].keys()), db1.search("pending_approve.csv").table)
    write_csv("pending_eval.csv", list(db1.search("pending_eval.csv").table[0].keys()), db1.search("pending_eval.csv").table)


# make calls to the initializing and login functions defined above
initializing()


db1.search("login.csv").print_table()
# val = login(db1)
# print(val)
#

# based on the return value for login, activate the code that performs activities according to the role defined for that person_id

# if val[1] = 'admin':
    # see and do admin related activities
# elif val[1] = 'student':
    # see and do student related activities
# elif val[1] = 'member':
    # see and do member related activities
# elif val[1] = 'lead':
    # see and do lead related activities
# elif val[1] = 'faculty':
    # see and do faculty related activities
# elif val[1] = 'advisor':
    # see and do advisor related activities

# once everyhthing is done, make a call to the exit function
exit()
