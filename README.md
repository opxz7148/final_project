# Final project for 2023's 219114/115 Programming I
* Starting files for part 1
  - database.py
  - project_manage.py
  - persons.csv

# List of file
  - #### database.py : This file contain 2 class that necessary for data management.
    - Database: Contain a list of table as a attribute. Able to return a table with table name as a input.
    - Table: Contain a list of dictionary and a name of it. Can filter a table with condition as a lamda function and return new table

  - #### project_class.py: This file contain class for every role.
    - Student : Contain a method that relate to action that student able to perform. Ex: start a project, view member invitation
    - Lead : Contain a method that relate to action that lead student able to perform. Ex: Invite advisor, Invite member, send evaluate request
    - Faculty : Contain a method that relate to action that Faculty member able to perform.


  - #### _helper.py_ : This file doesn't have any class but contain helper function to simplify some complex process.

  - #### _project_manage.py_: This doesn't have any class but contain a main code to start a program.    
    
  - #### _login.csv : csv file_ that contain login information for each user.

  - #### _pending_advisor.csv_ : csv file that contain information to keep track of advisor invitation.

  - #### _pending_approve.csv_ : csv file that contain information to keep track of approving request. Both report and proposal request.

  - #### _pending_evaL.csv_ : csv file that contain information to keep track of evaluation request.

  - #### _pending_advisor.csv_ : csv file that contain information to keep track of member invitation.

  - #### _persons.csv_ : csv file that contain real name of user, type, and user ID of every user.

  - #### _project.csv_ : csv file that contain information about every project and keep track of every change in project.

# How to run a program
    
  - #### Note: If program print "Press enter to continue" you must press enter to continue to next process. But sometime after press enter nothing will happen you must press enter again to continue
  - Just simply run _project_manage.py_ with run button in IDE or run `python project_manage.py` in terminal.
  - Program will greet you with a welcome message
  - Login into program with ID and password in login.csv. | _note : I've change some of username and password in login.csv for easier testing therefore username and password may not same as other people._
  - Program will greet you again with your real name, role and ID and wait for user to press an enter
  - Menu will appear with an action that you able to perform correspond to your role.
  - You can choose which action you want to perform by input number correspond to menu that print beforehand (Apply to all menu in program)

# Role's action table
|  Role   | Action                                                                                                                     | Method                                         | Class   | Completion percentage |
|:-------:|:---------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------|---------|:---------------------:|
| Student | Start a new project and change their role to lead.                                                                         | `def __start_project(self): `                  | Student |         100%          |
|         | View project member invitation and decide to accept which will change role to member or deny invitation to join a project. | `def __accept_invite(self):`                   | Student |         100%          |
|  Lead   | View and edit project.                                                                                                     | `def __view_project(self):`                    | Lead    |         100%          |
|         | Invite candidate member to a project.                                                                                      | `def __invite_member(self):`                   | Lead    |         100%          |
|         | Invite candidate advisor to a project.                                                                                     | `def __invite_advisor(self):`                  | Lead    |         100%          |
|         | Sent proposal approval request to advisor.                                                                                 | `def __ap_request(self, re_type):`             | Lead    |         100%          |
|         | Sent report approval request to advisor.                                                                                   | `def __ap_request(self, re_type):`             | Lead    |         100%          |
|         | Send evaluate request to faculty member and other advisor.                                                                 | `def __eval_request(self):`                    | Lead    |         100%          |
|         | View history and status for each action                                                                                    | `def __show_history(self):`                    | Lead    |         100%          |
| Member  | View and edit project.                                                                                                     | `def __view_project(self):`                    | Lead    |         100%          |
|         | View history and status for each action.                                                                                   | `def __show_history(self):`                    | Lead    |         100%          |
| Faculty | View and decide to accept or deny advisor request.                                                                         | `def __view_advisor_request(self): `           | Faculty |         100%          |
|         | View a evaluate request from lead student and choose to approve or not.                                                    | `def __eval(self):`                            | Faculty |         100%          |
| Advisor | View and decide to accept or deny advisor request.                                                                         | `def __view_advisor_request(self): `           | Advisor |         100%          |
|         | View a evaluate request from lead student and choose to approve or not.                                                    | `def __eval(self):`                            | Advisor |         100%          |
|         | View a project that they're currently advising and edit some detail in project.                                            | `def __view_advising_project(self):`           | Advisor |         100%          |
|         | View proposal and report than decide to approve or not                                                                     | `def __approve_project(self, re_type):`        | Advisor |         100%          |
|  Admin  | View and insert new row of information in every csv file                                                                   | `def __view_and_insert_table(self, filename):` | Admin   |         100%          |
|         | Edit information in certain row                                                                                            | -                                              |         |          0%           |

