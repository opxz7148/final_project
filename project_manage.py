# BEGIN part 1

# import database module
from database import Database, Table
# define a funcion called initializing

def initializing():
    pass

# here are things to do in this function:

    # create an object to read an input csv file, persons.csv

    # create a 'persons' table

    # add the 'persons' table into the database

    # create a 'login' table

    # the 'login' table has the following keys (attributes):
        # person_id
        # username
        # password
        # role

    # a person_id is the same as that in the 'persons' table

    # let a username be a person's fisrt name followed by a dot and the first letter of that person's last name

    # let a password be a random four digits string

    # let the initial role of all the students be Member

    # let the initial role of all the faculties be Faculty

    # create a login table by performing a series of insert operations; each insert adds a dictionary to a list

    # add the 'login' table into the database

# define a funcion called login

def login():
    pass

# here are things to do in this function:
   # add code that performs a login task
        # ask a user for a username and password
        # returns [person_id, role] if valid, otherwise returning None

# make calls to the initializing and login functions defined above

initializing()
val = login()

# END part 1

# CONTINUE to part 2 (to be done for the next due date)

# based on the return value for login, activate the code that performs activities according to the role defined for that person_id

# if val[1] = 'admin':
    # do admin related activities
# elif val[1] = 'advisor':
    # do advisor related activities
# elif val[1] = 'lead':
    # do lead related activities
# elif val[1] = 'member':
    # do member related activities
# elif val[1] = 'faculty':
    # do faculty related activities
