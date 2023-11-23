# import database module
from database import Database, Table
# define a funcion called initializing

# Initialize database for collect information
db1 = Database("db1")
def initializing():

# here are things to do in this function:

    # create an object to read all csv files that will serve as a persistent state for this program
    # create all the corresponding tables for those csv files
    db1.add_csv_table("persons.csv")
    db1.add_csv_table("login.csv")
    db1.add_csv_table("project.csv")
    db1.add_csv_table("pending_advisor.csv")
    db1.add_csv_table("pending_member.csv")
    db1.add_csv_table("pending_approve.csv")
    db1.add_csv_table("pending_eval.csv")

    # see the guide how many tables are needed
    # add all these tables to the database


# define a function called login
def login():

    # ask a user for a username and password
    username = input("Username: ")
    password = input("Password: ")

    # Check that username and password are exist or not.
    login_table = db1.search("login.csv").table
    for user in login_table:
        if username == user["username"]:
            if user["password"] == password:
                # returns [ID, role] if valid
                return [user["ID"], user["role"]]
            else:
                # otherwise returning None
                print("Password incorrect")
                return None
    return None



# define a function called exit
def exit():
    pass

# here are things to do in this function:
   # write out all the tables that have been modified to the corresponding csv files
   # By now, you know how to read in a csv file and transform it into a list of dictionaries. For this project, you also need to know how to do the reverse, i.e., writing out to a csv file given a list of dictionaries. See the link below for a tutorial on how to do this:
   
   # https://www.pythonforbeginners.com/basics/list-of-dictionaries-to-csv-in-python


# make calls to the initializing and login functions defined above

initializing()
val = login()
print(val)


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
