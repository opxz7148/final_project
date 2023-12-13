import csv

def login(db):

    while True:
        # ask a user for a username and password
        username = input("Username: ")

        # Check that username and password are exist or not.
        login_table = db.search("login.csv").table
        for user in login_table:
            if username == user["username"]:
                password = input("Password: ")
                if user["password"] == password:
                    # returns [ID, role] if valid
                    return [user["username"], user["ID"], user["role"]]
                else:
                    # otherwise returning None
                    print("Password incorrect")
                    continue
        print("Username Invalid")
        continue

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


def get_int(msg, start=0, stop=10000):
    in_range = list(range(start, stop+1))
    while True:
        result = input(msg)
        try:
            result = int(result)
        except ValueError:
            continue

        if result not in in_range:
            continue
        return result


def get_str(msg):

    while True:
        result = input(msg)
        if result.strip() == "":
            continue
        return result


def print_get_choice(choice_lst,exit_choice="Exit"):

    print("")
    for choice in range(len(choice_lst)):
        print(f"    [{choice + 1}] {choice_lst[choice]}")
    print(f"    [0] {exit_choice}")
    print("")

    ans = get_int("Select your action: ", 0, len(choice_lst))
    return ans

def wait_for_enter():
    input("Press enter to continue")

