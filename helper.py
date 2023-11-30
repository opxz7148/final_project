import csv

def login(db):

    # ask a user for a username and password
    username = input("Username: ")
    password = input("Password: ")

    # Check that username and password are exist or not.
    login_table = db.search("login.csv").table
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

def write_csv(filename, listofhead, listofdict):

    # Open file correspond to file name param.
    file = open(filename, 'w')

    # Create a writer and set field name for each field
    writer = csv.DictWriter(file, fieldnames=listofhead)

    # Write a header to file.
    writer.writeheader()

    # Write each row of information to file
    writer.writerows(listofdict)
    file.close()

