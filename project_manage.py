# import database module
from database import Database
from helper import login, record_change, get_name, wait_for_enter
from project_class import Student, Lead, Member, Faculty, Advisor, Admin

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


# make calls to the initializing and login functions defined above
initializing()

line_len = len('=====================================================')

print("\n=====================================================")
print(f"|{'Welcome to senior project manager.':^{line_len-2}}|")
print(f"|{'Please login with your username and password.':^{line_len-2}}|")
print("=====================================================\n")

val = login(db1)

print("\n=====================================================")
print(f"|{'Welcome ' + get_name(val[1], db1):^{line_len-2}}|")
print(f"|{'ID: ' + val[1]:^{line_len-2}}|")
print(f"|{'Role: ' + val[2].title():^{line_len-2}}|")
print("=====================================================")

wait_for_enter()

# based on the return value for login, activate the code that performs activities according to the role defined for that person_id
user = ""

if val[2] == "student":
    user = Student(val[0], val[1], db1)
elif val[2] == "lead":
    user = Lead(val[0], val[1], db1)
elif val[2] == "member":
    user = Member(val[0], val[1], db1)
elif val[2] == "faculty":
    user = Faculty(val[0], val[1], db1)
elif val[2] == "advisor":
    user = Advisor(val[0], val[1], db1)
elif val[2] == "admin":
    user = Admin(val[0], val[1], db1)

user.menu()

# once everyhthing is done, make a call to the exit function
record_change(db1)
exit()
