from helper import get_str, print_get_choice, wait_for_enter, record_change, print_project
import sys


class Student:
    def __init__(self, username, id, db):
        self.__username = username
        self.__id = id
        self.__db = db

    @property
    def id(self):
        return self.__id

    @property
    def username(self):
        return self.__username

    @property
    def db(self):
        return self.__db

    def __start_project(self):
        # Get information about project
        name = get_str("Project name: ")
        detail = get_str("Detail: ")

        # Record project detail to database
        self.db.search("project.csv").insert({
            "name": name,
            "detail": detail,
            "lead": self.id,
            "member": "none/none",
            "member_count": "1",
            "advisor": "none",
            "proposal" : "TODO",
            "report" : "TODO",
            "status": "Writing proposal",
            "approval": "none"
        })

        for invitation in self.db.search('pending_member.csv').table:
            if invitation['pending_member'] == self.id:
                invitation['status'] = 'Decline'

        # Get login table
        login_table = self.db.search("login.csv").table

        # Change user role to lead student.
        for user in login_table:
            if user["ID"] == self.id:
                user["role"] = "lead"

        # Create new object for user as a lead
        user = Lead(self.username, self.id, self.db)
        user.menu()

    def __accept_invite(self):

        # Get necessary table for further action
        pending_member_table = self.db.search('pending_member.csv')
        all_project = self.db.search('project.csv')
        login_table = self.db.search('login.csv')

        if len(pending_member_table.filter(lambda invitation: invitation['pending_member'] == self.id and invitation['status'] == "Pending").table) != 0:

            # Show invitation if there are pending invitation
            my_invitation = pending_member_table.filter(lambda invitation: invitation['pending_member'] == self.id and invitation['status'] == "Pending", new_name="Pending invitation")
            my_invitation.print_table()

            # Ask what user want to do.
            print("Accept or Decline.:")
            ac = print_get_choice(['Accept', 'Decline'], exit_choice="Cancel")

            # If user choose cancel return back to menu
            if ac == 0:
                return

            # If user choose accept let user choose which group to join.
            elif ac == 1:
                # Get list of project name
                project_ls = [project['project'] for project in my_invitation.table]

                print("Choose a project to join:")
                choose_project = print_get_choice(project_ls, exit_choice="Cancel")

                if choose_project == 0:
                    return

                choose_project = project_ls[choose_project - 1]

                # Change status in pending member table
                for invitation in pending_member_table.table:
                    if invitation['pending_member'] == self.id:
                        invitation['status'] = "Decline"
                        if invitation['project'] == choose_project:
                            invitation['status'] = "Accept"


                # Add member ID to project
                for project in all_project.table:
                    if project['name'] == choose_project:

                        member = project["member"]
                        member_ls = member.split('/')
                        for mem in range(len(member_ls)):
                            if member_ls[mem] == "none":
                                member_ls[mem] = self.id
                                member = "/".join(member_ls)
                                break
                        project["member"] = member

                        # Change member count
                        member_count = int(project['member_count'])
                        member_count += 1
                        project['member_count'] = str(member_count)

                        break

                # Change role in login table
                for person in login_table.table:
                    if person['ID'] == self.id:
                        person['role'] = "member"
                        break

                print(f"You've join {choose_project}")
                wait_for_enter()
                user = Member(self.username, self.id, self.db)
                user.menu()
                record_change(self.db)
                sys.exit()

            elif ac == 2:

                # Get list of project name
                project_ls = [project['project'] for project in my_invitation.table]

                print("Choose a invitation to decline:")
                choose_project = print_get_choice(project_ls, exit_choice="Cancel")

                if choose_project == 0:
                    return

                choose_project = project_ls[choose_project - 1]

                # Change status in pending member table
                for invitation in pending_member_table.table:
                    if invitation['pending_member'] == self.id and invitation['project'] == choose_project:
                        invitation['status'] = "Decline"
                        break

                return



        else:
            print("There are no pending invitation right at this time.")
            wait_for_enter()

    def menu(self):
        while True:

            choice = print_get_choice(['Start a project', 'Respond invitation'])

            if choice == 1:
                self.__start_project()
                break
            elif choice == 2:
                self.__accept_invite()
            elif choice == 0:
                break


class Lead:
    def __init__(self, username, id, db):
        # Construct attribute for lead student
        self.__username = username
        self.__id = id
        self.__db = db

        # Get user project from table and set as an attribute
        user_pro = db.search("project.csv").filter(lambda project: project["lead"] == self.id).table[0]
        self.__project = user_pro

    def __print_project(self):

        print_project(self.project)

    def __view_project(self):

        self.__print_project()
        wait_for_enter()

        while True:

            choice = print_get_choice(['Edit'])
            if choice == 1:
                edit_choice = print_get_choice(['Project name', 'Detail', 'Proposal', 'Report'])
                if edit_choice != 0:
                    self.__edit_project(edit_choice)
            if choice == 0:
                break

    def __edit_project(self, choice):
        new = get_str("New information: ")

        if choice == 1:
            self.project['name'] = new
        elif choice == 2:
            self.project['detail'] = new
        elif choice == 3:
            self.project['proposal'] = new
        elif choice == 4:
            self.project['report'] = new

        self.__print_project()
        wait_for_enter()

    def __invite_member(self):

        if int(self.project["member_count"]) == 3:
            print("You've already reach maximum number of member")
            wait_for_enter()
            return

        # Prepare table from database for further action
        pending_member_table = self.db.search('pending_member.csv')
        login_table = self.db.search('login.csv')

        if len(pending_member_table.filter(lambda invitation: invitation['lead'] == self.id and invitation['status'] == 'pending').table) != 0:

            # Show invitation if there are pending invitation
            pending_member_table.filter(lambda invitation: invitation['lead'] == self.id and invitation['status'] == 'pending', new_name="Pending member").print_table()

        else:

            # Show table of student who isn't a member in any project if there are no pending invitation
            login_table.filter(lambda person: person["role"] == "student").print_table(exclude_key=['password'])

            # Let user input id of student that they want to invite
            invite_done = False
            while True:

                if invite_done:
                    break

                # Prompt user for ID
                id = get_str("Enter student ID or type 0 to abort: ")

                if id == '0':
                    break

                # Check is ID available
                for person in login_table.table:
                    if person['ID'] == id:

                        if person['role'] != 'student':
                            print("Invalid ID")

                        print(f"Invite {person['username']} ID: {person['ID']}.")
                        ans = print_get_choice(["Confirm"], 'Cancel')
                        if ans == 0:
                            break
                        if ans == 1:

                            print("Sending invite")

                            # Record new invitation to table
                            pending_member_table.insert(
                                {
                                    'lead': self.id,
                                    'project': self.project['name'],
                                    'pending_member': id,
                                    'status': "Pending"
                                }
                            )

                            invite_done = True
                            break
                if not invite_done:
                    print("Invalid ID")
                    wait_for_enter()

    def __view_invitation_status(self):

        pending_member_table = self.db.search('pending_member.csv')
        if len(pending_member_table.filter(lambda invitation: invitation['lead'] == self.id).table) != 0:

            # Show invitation if there are pending invitation
            pending_member_table.filter(lambda invitation: invitation['lead'] == self.id, new_name="Pending member").print_table()
            wait_for_enter()

        else:
            print("There are no pending member right at this time.")
            wait_for_enter()

    def __invite_advisor(self):

        if self.project["advisor"] != "none":
            print("You already have advisor")
            wait_for_enter()
            return

        # Prepare table from database for further action
        pending_advisor_table = self.db.search('pending_advisor.csv')
        login_table = self.db.search('login.csv')

        if len(pending_advisor_table.filter(lambda invitation: invitation['lead'] == self.id and invitation['status'] == 'pending').table) != 0:

            # Show invitation if there are pending invitation
            pending_advisor_table.filter(lambda invitation: invitation['lead'] == self.id and invitation['status'] == 'pending', new_name="Pending member").print_table()
            wait_for_enter()

        else:

            # Show table of student who isn't a member in any project if there are no pending invitation
            login_table.filter(lambda person: person["role"] == "faculty" or person["role"] == "advisor", new_name="Faculty member list" ).print_table(exclude_key=['password'])

            # Let user input id of student that they want to invite
            invite_done = False
            while True:

                if invite_done:
                    break

                # Prompt user for ID
                id = get_str("Enter faculty member ID or type 0 to abort: ")

                if id == '0':
                    break

                # Check is ID available
                for person in login_table.table:
                    if person['ID'] == id:

                        if person['role'] != 'faculty' and person['role'] != 'advisor':
                            print("Invalid ID")
                            wait_for_enter()
                            break

                        print(f"Invite {person['username']} ID: {person['ID']}.")
                        ans = print_get_choice(["Confirm"], 'Cancel')
                        if ans == 0:
                            break
                        if ans == 1:
                            print("Sending invite")

                            # Record new invitation to table
                            pending_advisor_table.insert(
                                {
                                    'lead': self.id,
                                    'project': self.project['name'],
                                    'pending_advisor': id,
                                    'status': "Pending"
                                }
                            )
                            invite_done = True
                            break

                if not invite_done:
                    print("Invalid ID")
                    wait_for_enter()

    def __view_request_history(self):

        # Prepare necessary table for further action
        pending_approve_table = self.db.search("pending_approve.csv")

        # Get pending request to check are their any ongoing request
        my_request = pending_approve_table.filter(lambda request: request['lead'] == self.id, new_name="Your request history")

        if len(my_request.table) == 0:
            print("You haven't sent any request")
            wait_for_enter()
        else:
            my_request.print_table(new_line_key=["feedback"])
            wait_for_enter()

    def __ap_request(self, re_type):

        # Prepare necessary table for further action
        pending_approve_table = self.db.search("pending_approve.csv")

        # Get pending request to check are their any ongoing request
        if re_type == "proposal":

            if self.project['status'] != 'Writing proposal':
                print("You can't send proposal approve request at this time")
                wait_for_enter()
                return

            my_request = pending_approve_table.filter(lambda request : request['lead'] == self.id and
                                                                       request['status'] == 'Proposal approve pending',
                                                      new_name="Your Ongoing request")
        else:

            if self.project['status'] != 'Evaluated':
                print("You can't send report approve request at this time")
                wait_for_enter()
                return

            my_request = pending_approve_table.filter(lambda request : request['lead'] == self.id and
                                                                       request['status'] == 'Report approve pending',
                                                      new_name="Your Ongoing request")

        if len(my_request.table) == 0:

            # If there are no ongoing request
            # Print project detail to let user check before sending request
            self.__print_project()
            wait_for_enter()

            if re_type == "proposal":
                choice = print_get_choice(['Confirm'], exit_choice="Cancel",
                                          prompt="Confirm sending proposal approve request: ")
            else:
                choice = print_get_choice(['Confirm'], exit_choice="Cancel",
                                          prompt="Confirm sending report approve request: ")

            # If user tp cancel request go back to main menu
            if choice == 0:
                return
            # If user confirm record log to table
            elif choice == 1:
                pending_approve_table.insert(
                    {
                        'lead': self.id,
                        'project': self.project['name'],
                        'advisor': self.project['advisor'],
                        'feedback': 'None',
                        'status': 'Report approve pending'
                    }
                )
        else:
            my_request.print_table(new_line_key=["feedback"])
            wait_for_enter()

    def __eval_request(self):

        pending_eval = self.db.search('pending_eval.csv')

        # If project not in writing report state user can't request a evaluate.
        if self.project["status"] == "Writing Report" or self.project['status'] == "Evaluated":
            pass
        else:
            ongoing = pending_eval.filter(lambda request: request['lead'] == self.id and request['status'] == "Evaluate request pending")
            ongoing.print_table(new_line_key=['feedback'])
            wait_for_enter()
            return

        # Print project out to let user recheck before send a request
        self.__print_project()
        wait_for_enter()

        # Prepare table for further action
        login_table = self.db.search('login.csv')
        person_table = self.db.search('persons.csv')

        # New joined table to show both username and real name
        join_table = login_table.join(person_table, "ID").filter(lambda person: (person['role'] == 'faculty' or person['role'] == 'advisor') and person['ID'] != self.project['advisor'])

        # Print List of faculty member that able to evaluate project
        join_table.print_table(exclude_key=['password', 'type'])
        wait_for_enter()

        invite_done = False

        while True:

            if invite_done:
                break

            # Prompt user for ID
            selected_id = get_str("Enter faculty member ID or type 0 to abort: ")

            if selected_id == '0':
                break

            # Check is ID available
            for person in login_table.table:
                if person['ID'] == selected_id:

                    # Check that selected faculty member already evaluated this project or not.
                    if person['ID'] in self.project['approval']:
                        # If so prompt user for ID again
                        print(f"{person['username']} already evaluate your project")
                        break

                    # Check is selected person have a valid role or not
                    if (person['role'] != 'advisor' and person['role'] != 'faculty') or person["ID"] == self.project['advisor']:
                        print(f"{person['username']} can't evaluated project")
                        break

                    print(f"Invite {person['username']} ID: {person['ID']}.")
                    ans = print_get_choice(["Confirm"], 'Cancel')
                    if ans == 0:
                        break
                    if ans == 1:
                        print("Sending request")

                        # Record new invitation to table
                        pending_eval.insert(
                            {
                                'lead': self.id,
                                'project': self.project['name'],
                                'pending_committee': selected_id,
                                'feedback': 'none',
                                'status': "Evaluate request pending"
                            }
                        )
                        wait_for_enter()

                        invite_done = True
                        break

            if not invite_done:
                print("Invalid ID")
                wait_for_enter()

    def __eval_history(self):

        pending_eval = self.db.search('pending_eval.csv')

        eval = pending_eval.filter(lambda request: request['lead'] == self.id)

        if len(eval.table) != 0:
            eval.print_table(new_line_key=['feedback'])
            wait_for_enter()
        else:
            print("No request history available")
            wait_for_enter()
        return

    def menu(self):

        while True:

            choice = print_get_choice(['View project', 'Invite member', 'Invite Advisor', 'Member invitation status', 'Proposal Approve request','Report approve request', 'View request history', 'Evaluate request', 'Evaluated history'])

            if choice == 1:
                self.__view_project()
            elif choice == 2:
                self.__invite_member()
            elif choice == 3:
                self.__invite_advisor()
            elif choice == 4:
                self.__view_invitation_status()
            elif choice == 5:
                self.__ap_request('proposal')
            elif choice == 6:
                self.__ap_request('report')
            elif choice == 7:
                self.__view_request_history()
            elif choice == 8:
                self.__eval_request()
            elif choice == 9:
                self.__eval_history()
            elif choice == 0:
                break

    @property
    def id(self):
        return self.__id

    @property
    def username(self):
        return self.__username

    @property
    def db(self):
        return self.__db

    @property
    def project(self):
        return self.__project


class Member:
    def __init__(self, username, id, db):
        # Construct attribute for lead student
        self.__username = username
        self.__id = id
        self.__db = db

        user_pro = db.search("project.csv").filter(lambda project: self.id in project["advisor"]).table[0]
        print(user_pro)
        self.__project = user_pro

    def __print_project(self):

        print_project(self.project)

    def __edit_project(self, choice):

        new = get_str("New information: ")

        if choice == 1:
            self.project['detail'] = new
        elif choice == 2:
            self.project['proposal'] = new
        elif choice == 3:
            self.project['report'] = new

        self.__print_project()
        wait_for_enter()

    def __view_project(self):

        self.__print_project()
        wait_for_enter()

        while True:

            choice = print_get_choice(['Edit'])
            if choice == 1:
                edit_choice = print_get_choice(['Detail', 'Proposal', 'Report'])
                if edit_choice != 0:
                    self.__edit_project(edit_choice)
            if choice == 0:
                break

    def menu(self):
        while True:

            choice = print_get_choice(['View and edit project'])

            if choice == 0:
                break
            elif choice == 1:
                self.__view_project()

    @property
    def id(self):
        return self.__id

    @property
    def username(self):
        return self.__username

    @property
    def db(self):
        return self.__db

    @property
    def project(self):
        return self.__project


class Faculty:
    def __init__(self, username, id, db):
        # Construct attribute for faculty member
        self.__username = username
        self.__id = id
        self.__db = db

    def __view_advisor_request(self):

        # Get necessary table for further action
        pending_advisor_table = self.db.search('pending_advisor.csv')
        all_project = self.db.search('project.csv')
        login_table = self.db.search('login.csv')

        if len(pending_advisor_table.filter(lambda invitation: invitation['pending_advisor'] == self.id and invitation['status'] == "Pending").table) != 0:

            # Show invitation if there are pending invitation
            my_invitation = pending_advisor_table.filter(lambda invitation: invitation['pending_advisor'] == self.id and invitation['status'] == "Pending", new_name="Pending invitation")
            my_invitation.print_table()

            # Ask what user want to do.
            print("Accept or Decline.:")
            ac = print_get_choice(['Accept', 'Decline'], exit_choice="Cancel")

            # If user choose cancel return back to menu
            if ac == 0:
                return

            # If user choose accept let user choose which group to join.
            elif ac == 1:
                # Get list of project name
                project_ls = [project['project'] for project in my_invitation.table]

                print("Choose a project to join:")
                choose_project = print_get_choice(project_ls, exit_choice="Cancel")

                if choose_project == 0:
                    return

                choose_project = project_ls[choose_project - 1]

                # Change status in pending member table
                for invitation in pending_advisor_table.table:
                    if invitation['pending_advisor'] == self.id and invitation['project'] == choose_project:
                        invitation['status'] = "Accept"


                # Add member ID to project
                for project in all_project.table:
                    if project['name'] == choose_project:
                        project['advisor'] = self.id
                        break

                # Change role in login table
                for person in login_table.table:
                    if person['ID'] == self.id:
                        person['role'] = "advisor"
                        break

                print(f"You've join {choose_project}")
                wait_for_enter()
                user = Advisor(self.username, self.id, self.db)
                user.menu()
                record_change(self.db)
                sys.exit()

            elif ac == 2:

                # Get list of project name
                project_ls = [project['project'] for project in my_invitation.table]

                print("Choose a invitation to decline:")
                choose_project = print_get_choice(project_ls, exit_choice="Cancel")

                if choose_project == 0:
                    return

                choose_project = project_ls[choose_project - 1]

                # Change status in pending advisor table
                for invitation in pending_advisor_table.table:
                    if invitation['pending_advisor'] == self.id and invitation['project'] == choose_project:
                        invitation['status'] = "Decline"
                        break

                return



        else:
            print("There are no pending invitation right at this time.")
            wait_for_enter()

    def __eval(self):
        # Prepare necessary table for further action
        pending_eval_table = self.db.search("pending_eval.csv")
        all_project = self.db.search("project.csv")

        my_request = pending_eval_table.filter(lambda request: request['pending_committee'] == self.id and
                                                                  request['status'] == 'Evaluate request pending',
                                                  new_name="Your Ongoing request")

        if len(my_request.table) == 0:
            print("There are no request right at this time")
            wait_for_enter()
            return

        my_request.print_table()
        wait_for_enter()

        # Get list of project name
        project_ls = [project['project'] for project in my_request.table]

        while True:
            # Prompt user which project to respond
            choose_project = print_get_choice(project_ls, exit_choice="Cancel", prompt="Choose a project to evaluate: ")

            # If user choose to cancel return back to menu
            if choose_project == 0:
                return

            # Set choose project to a name of project instead of index
            choose_project = project_ls[choose_project - 1]

            for project in all_project.table:
                if project['name'] == choose_project:
                    choose_project = project

            # Let user select to approve or not
            print_project(choose_project)
            action = print_get_choice(["Approve", "Unapprove"],
                                      exit_choice="Cancel",
                                      prompt=f"Approve this project?: ")

            if action == 0:
                continue

            feedback = get_str("Feedback: ")

            right_request = {}

            for request in pending_eval_table.table:
                if choose_project['lead'] == request['lead'] and request['status'] == "Evaluate request pending":
                    right_request = request
                    break

            if action == 1:

                choose_project["status"] = 'Evaluated'
                right_request["status"] = 'Evaluated'
                right_request["feedback"] = feedback

                if choose_project['approval'] == 'none':
                    choose_project['approval'] = self.id
                else:
                    approval = choose_project['approval']
                    approval += f"/{self.id}"
                    choose_project['approval'] = approval

                return

            elif action == 2:
                right_request["status"] = 'Unapprove'
                right_request["feedback"] = feedback
                return

    def menu(self):
        while True:

            choice = print_get_choice(['Respond advisor request', 'Evaluate Project'])

            if choice == 0:
                break
            elif choice == 1:
                self.__view_advisor_request()
            elif choice == 2:
                self.__eval()
                pass


    @property
    def id(self):
        return self.__id

    @property
    def username(self):
        return self.__username

    @property
    def db(self):
        return self.__db


class Advisor:
    def __init__(self, username, id, db):
        # Construct attribute for faculty member
        self.__username = username
        self.__id = id
        self.__db = db

        all_project = db.search('project.csv')
        self.__advising = [project for project in all_project.table if project['advisor'] == self.id]

    def __view_advisor_request(self):

        # Get necessary table for further action
        pending_advisor_table = self.db.search('pending_advisor.csv')
        all_project = self.db.search('project.csv')
        login_table = self.db.search('login.csv')

        if len(pending_advisor_table.filter(lambda invitation: invitation['pending_advisor'] == self.id and invitation['status'] == "Pending").table) != 0:

            # Show invitation if there are pending invitation
            my_invitation = pending_advisor_table.filter(
                lambda invitation: invitation['pending_advisor'] == self.id and invitation['status'] == "Pending",
                new_name="Pending invitation"
            )
            my_invitation.print_table()

            # Ask what user want to do.
            print("Accept or Decline.:")
            ac = print_get_choice(['Accept', 'Decline'], exit_choice="Cancel")

            # If user choose cancel return back to menu
            if ac == 0:
                return

            # If user choose accept let user choose which group to join.
            elif ac == 1:
                # Get list of project name
                project_ls = [project['project'] for project in my_invitation.table]

                choose_project = print_get_choice(project_ls, exit_choice="Cancel", prompt="Choose a project to join:")

                if choose_project == 0:
                    return

                choose_project = project_ls[choose_project - 1]

                # Change status in pending member table
                for invitation in pending_advisor_table.table:
                    if invitation['pending_advisor'] == self.id and invitation['project'] == choose_project:
                        invitation['status'] = "Accept"

                # Add member ID to project
                for project in all_project.table:
                    if project['name'] == choose_project:
                        project['advisor'] = self.id
                        break

                # Change role in login table
                for person in login_table.table:
                    if person['ID'] == self.id:
                        person['role'] = "advisor"
                        break

                print(f"You've join {choose_project}")
                wait_for_enter()
                return

            elif ac == 2:

                # Get list of project name
                project_ls = [project['project'] for project in my_invitation.table]

                print("Choose a invitation to decline:")
                choose_project = print_get_choice(project_ls, exit_choice="Cancel")

                if choose_project == 0:
                    return

                choose_project = project_ls[choose_project - 1]

                # Change status in pending member table
                for invitation in pending_advisor_table.table:
                    if invitation['pending_member'] == self.id and invitation['project'] == choose_project:
                        invitation['status'] = "Decline"
                        break

                return



        else:
            print("There are no pending invitation right at this time.")
            wait_for_enter()

    def __edit_project(self, choice, project):

        new = get_str("New information: ")

        if choice == 1:
            project['detail'] = new
        elif choice == 2:
            project['proposal'] = new
        elif choice == 3:
            project['report'] = new

        print_project(project)
        wait_for_enter()

    def __view_advising_project(self):

        # Get list of project from attribute
        project_ls = [project['name'] for project in self.advising]

        while True:
            choose_project = print_get_choice(project_ls, exit_choice="Cancel", prompt="Choose a project to advise:")

            if choose_project == 0:
                return

            choose_project = self.advising[choose_project - 1]

            print_project(choose_project)
            wait_for_enter()

            while True:

                choice = print_get_choice(['Edit'])
                if choice == 1:
                    edit_choice = print_get_choice(['Detail', 'Proposal', 'Report'])
                    if edit_choice != 0:
                        self.__edit_project(edit_choice, choose_project)
                if choice == 0:
                    break

    def __approve_project(self, re_type):

        # Prepare necessary table for further action
        pending_approve_table = self.db.search("pending_approve.csv")

        # Get pending request to check are their any ongoing request
        if re_type == "proposal":
            my_request = pending_approve_table.filter(lambda request : request['advisor'] == self.id and
                                                                       request['status'] == 'Proposal approve pending',
                                                      new_name="Your Ongoing request")
        else:
            my_request = pending_approve_table.filter(lambda request : request['advisor'] == self.id and
                                                                       request['status'] == 'Report approve pending',
                                                      new_name="Your Ongoing request")

        # If don't have any ongoing request return to main menu.
        if len(my_request.table) == 0:
            print("There are no request right at this time")
            wait_for_enter()
            return

        my_request.print_table(exclude_key="feedback")

        # Get list of project name
        project_ls = [project['project'] for project in my_request.table]

        while True:
            # Prompt user which project to respond
            choose_project = print_get_choice(project_ls, exit_choice="Cancel", prompt=f"Choose a {re_type} to approve:")

            # If user choose to cancel return back to menu
            if choose_project == 0:
                return

            # Set choose project to a name of project instead of index
            choose_project = project_ls[choose_project - 1]

            # Find matching project name inside advisee attribute than set choose project to dict of project info instead.
            for advising in self.advising:
                if advising['name'] == choose_project:
                    choose_project = advising
                    break

            # Let user select to approve or not
            print_project(choose_project)
            action = print_get_choice(["Approve", "Unapprove"],
                                      exit_choice="Cancel",
                                      prompt=f"Approve this project's {re_type}?: ")

            if action == 0:
                continue

            feedback = get_str("Feedback: ")

            right_request = {}

            for request in pending_approve_table.table:
                if choose_project['lead'] == request['lead'] and request['status'] == f"{re_type.title()} approve pending":
                    right_request = request
                    break

            # Approve proposal
            if action == 1 and re_type == "proposal":
                choose_project["status"] = 'Writing Report'
                right_request["status"] = 'Approve'
                right_request["feedback"] = feedback
                return

            # Unapprove proposal
            elif action == 2 and re_type == "proposal":
                right_request["status"] = 'Unapprove'
                right_request["feedback"] = feedback
                return

            # Approve report
            elif action == 1 and re_type == "report":
                choose_project["status"] = 'Completed'
                right_request["status"] = 'Approve'
                right_request["feedback"] = feedback
                return

            # Unapprove report
            elif action == 2 and re_type == "report":
                right_request["status"] = 'Unapprove'
                right_request["feedback"] = feedback
                return



    def __eval(self):
        # Prepare necessary table for further action
        pending_eval_table = self.db.search("pending_eval.csv")
        all_project = self.db.search("project.csv")

        my_request = pending_eval_table.filter(lambda request: request['pending_committee'] == self.id and
                                                               request['status'] == 'Evaluate request pending',
                                               new_name="Your Ongoing request")

        if len(my_request.table) == 0:
            print("There are no request right at this time")
            wait_for_enter()
            return

        my_request.print_table()
        wait_for_enter()

        # Get list of project name
        project_ls = [project['project'] for project in my_request.table]

        while True:
            # Prompt user which project to respond
            choose_project = print_get_choice(project_ls, exit_choice="Cancel", prompt="Choose a project to evaluate: ")

            # If user choose to cancel return back to menu
            if choose_project == 0:
                return

            # Set choose project to a name of project instead of index
            choose_project = project_ls[choose_project - 1]

            for project in all_project.table:
                if project['name'] == choose_project:
                    choose_project = project

            # Let user select to approve or not
            print_project(choose_project)
            action = print_get_choice(["Approve", "Unapprove"],
                                      exit_choice="Cancel",
                                      prompt=f"Approve this project?: ")

            if action == 0:
                continue

            feedback = get_str("Feedback: ")

            right_request = {}

            for request in pending_eval_table.table:
                if choose_project['lead'] == request['lead'] and request['status'] == "Evaluate request pending":
                    right_request = request
                    break

            if action == 1:

                choose_project["status"] = 'Evaluated'
                right_request["status"] = 'Evaluated'
                right_request["feedback"] = feedback

                if choose_project['approval'] == 'none':
                    choose_project['approval'] = self.id
                else:
                    approval = choose_project['approval']
                    approval += f"/{self.id}"
                    choose_project['approval'] = approval

                return

            elif action == 2:
                right_request["status"] = 'Unapprove'
                right_request["feedback"] = feedback
                return

    def menu(self):
        while True:

            choice = print_get_choice(['View advisor request', 'View advising project', 'Approve proposal', 'Approve Report','Evaluate Project'])

            if choice == 0:
                break
            elif choice == 1:
                self.__view_advisor_request()
            elif choice == 2:
                self.__view_advising_project()
            elif choice == 3:
                self.__approve_project('proposal')
            elif choice == 4:
                self.__approve_project('report')
            elif choice == 5:
                self.__eval()


    @property
    def id(self):
        return self.__id

    @property
    def username(self):
        return self.__username

    @property
    def db(self):
        return self.__db

    @property
    def advising(self):
        return self.__advising
