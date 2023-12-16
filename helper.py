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


def record_change(db1):

    # Write each table back to csv file to update new information for each session.
    write_csv("persons.csv", list(db1.search("persons.csv").table[0].keys()), db1.search("persons.csv").table)
    write_csv("login.csv", list(db1.search("login.csv").table[0].keys()), db1.search("login.csv").table)
    write_csv("project.csv", list(db1.search("project.csv").table[0].keys()), db1.search("project.csv").table)
    write_csv("pending_advisor.csv", list(db1.search("pending_advisor.csv").table[0].keys()), db1.search("pending_advisor.csv").table)
    write_csv("pending_member.csv", list(db1.search("pending_member.csv").table[0].keys()), db1.search("pending_member.csv").table)
    write_csv("pending_approve.csv", list(db1.search("pending_approve.csv").table[0].keys()), db1.search("pending_approve.csv").table)
    write_csv("pending_eval.csv", list(db1.search("pending_eval.csv").table[0].keys()), db1.search("pending_eval.csv").table)



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


def print_get_choice(choice_lst, exit_choice="Exit", prompt="Select your action: "):

    print()
    print("=====================================================")
    for choice in range(len(choice_lst)):
        print(f"    [{choice + 1}] {choice_lst[choice]}")
    print(f"    [0] {exit_choice}")
    print("=====================================================")
    print()

    ans = get_int(prompt, 0, len(choice_lst))
    return ans


def wait_for_enter():
    print()
    input("Press enter to continue: ")


def print_project(project):
    # Print project detail
    print()
    print("=====================================================")
    print(f"Project name: {project['name']}")
    member = project['member'].split("/")
    print(f"Member 1: {member[0]}")
    print(f"Member 2: {member[1]}")
    print(f"advisor: {project['advisor']}")
    print(f"Detail: {project['detail']}")
    print(f"Lead: {project['lead']}")
    print(f"status: {project['status']}")
    print(f"Proposal: {project['proposal']}")
    print(f"Report: {project['report']}")
    print("=====================================================")




