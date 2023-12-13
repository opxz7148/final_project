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
                return [user["username"], user["ID"], user["role"]]
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
        try:
            result = int(result)
        except ValueError:
            if result.strip() == "":
                continue
            return result

        continue


def print_get_choice(choice_lst):

    print("")
    for choice in range(len(choice_lst)):
        print(f"    [{choice + 1}] {choice_lst[choice]}")
    print("")

    ans = get_int("Select your action: ", 1, len(choice_lst))
    return ans

