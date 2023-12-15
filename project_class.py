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
                        print(f"Invite {person['username']} ID: {person['ID']}.")
                        ans = print_get_choice(["Confirm"], 'Cancel')
                        if ans == 0:
                            break
                        if ans == 1:
                            print("Sending invite")

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
            # Record new invitation to table

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
                        print(f"Invite {person['username']} ID: {person['ID']}.")
                        ans = print_get_choice(["Confirm"], 'Cancel')
                        if ans == 0:
                            break
                        if ans == 1:
                            print("Sending invite")

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
            # Record new invitation to table

    def menu(self):

        while True:

            choice = print_get_choice(['View project', 'Invite member', 'Invite Advisor', 'Member invitation status'])

            if choice == 1:
                self.__view_project()
            elif choice == 2:
                self.__invite_member()
            elif choice == 3:
                self.__invite_advisor()
            elif choice == 4:
                self.__view_invitation_status()
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
        pending_adivisor_table = self.db.search('pending_advisor.csv')
        all_project = self.db.search('project.csv')
        login_table = self.db.search('login.csv')

        if len(pending_adivisor_table.filter(lambda invitation: invitation['pending_advisor'] == self.id and invitation['status'] == "Pending").table) != 0:

            # Show invitation if there are pending invitation
            my_invitation = pending_adivisor_table.filter(lambda invitation: invitation['pending_advisor'] == self.id and invitation['status'] == "Pending", new_name="Pending invitation")
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
                for invitation in pending_adivisor_table.table:
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
                for invitation in pending_adivisor_table.table:
                    if invitation['pending_advisor'] == self.id and invitation['project'] == choose_project:
                        invitation['status'] = "Decline"
                        break

                return



        else:
            print("There are no pending invitation right at this time.")
            wait_for_enter()

    def menu(self):
        while True:

            choice = print_get_choice(['Respond advisor request', 'Evaluate Project'])

            if choice == 0:
                break
            elif choice == 1:
                self.__view_advisor_request()
            elif choice == 2:
                #TODO
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
    # TODO add advisee attribute as a list of project.
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

    def menu(self):
        while True:

            choice = print_get_choice(['View advisor request', 'View advising project', 'Evaluate Project'])

            if choice == 0:
                break
            elif choice == 1:
                self.__view_advisor_request()
            elif choice == 2:
                self.__view_advising_project()

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






