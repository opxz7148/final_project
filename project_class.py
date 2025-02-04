import sys
from helper import get_str, print_get_choice, wait_for_enter, record_change, print_project


class Student:
    def __init__(self, username, user_id, db):
        self.__username = username
        self.__id = user_id
        self.__db = db

    def __start_project(self):
        """
        Let student able to start a new project and change role to lead student.
        """
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
            "proposal": "TODO",
            "report": "TODO",
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
        """
        Show a pending project group invitation to user and let user decide to accept invitation or not.
        """

        # Get necessary table for further action
        pending_member_table = self.db.search('pending_member.csv')
        all_project = self.db.search('project.csv')
        login_table = self.db.search('login.csv')

        if len(
                pending_member_table.filter(
                    lambda pending:
                        pending['pending_member'] == self.id and
                        pending['status'] == "Pending"
                ).table
               ) != 0:

            # Show invitation if there are pending invitation

            my_invitation = pending_member_table.filter(
                lambda pending:
                    pending['pending_member'] == self.id and
                    pending['status'] == "Pending",
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

                choose_project = print_get_choice(project_ls, exit_choice="Cancel", prompt="Which project to join: ")

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
                choose_project = print_get_choice(project_ls, exit_choice="Cancel", prompt="Which project to decline: ")

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
        """
        Menu that will show an action that student able to do and let them to decide what to do.
        :return:
        """
        while True:

            choice = print_get_choice(['Start a project', 'Respond invitation'])

            if choice == 1:
                self.__start_project()
                break
            elif choice == 2:
                self.__accept_invite()
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


class Lead:
    def __init__(self, username, user_id, db):
        # Construct attribute for lead student
        self.__username = username
        self.__id = user_id
        self.__db = db

        # Get user project from table and set as an attribute
        user_pro = db.search("project.csv").filter(lambda project: project["lead"] == self.id).table[0]
        self.__project = user_pro

    def __print_project(self):

        """
        Simply print project in a easy to read format
        """

        print_project(self.project, self.db)

    def __view_project(self):

        """
        Show project detail to user and let them decide to edit or do nothing.
        :return:
        """

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
        """
        Edit project depend on user choice
        :param choice: Key of dict that user want ot edit
        """
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

        """
        Show a list of student that able to send an invitation and let user sent an invitation to that student.
        """

        if int(self.project["member_count"]) == 3:
            print("You've already reach maximum number of member")
            wait_for_enter()
            return

        # Prepare table from database for further action
        pending_member_table = self.db.search('pending_member.csv')
        login_table = self.db.search('login.csv')

        if len(
                pending_member_table.filter(
                    lambda invitation:
                        invitation['lead'] == self.id and
                        invitation['status'] == 'pending'
                ).table
        ) != 0:

            # Show invitation if there are pending invitation
            pending_member_table.filter(
                lambda invitation:
                    invitation['lead'] == self.id and
                    invitation['status'] == 'pending',
                new_name="Pending member").print_table()

        else:

            # Show table of student who isn't a member in any project if there are no pending invitation
            login_table.filter(
                lambda able_person:
                    able_person["role"] == "student"
            ).print_table(exclude_key=['password'])
            wait_for_enter()

            # Let user input id of student that they want to invite
            invite_done = False
            while True:

                if invite_done:
                    break

                # Prompt user for ID
                user_id = get_str("Enter student ID or type 0 to abort: ")

                if user_id == '0':
                    break

                # Check is ID available
                for person in login_table.table:
                    if person['ID'] == user_id:

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
                                    'pending_member': user_id,
                                    'status': "Pending"
                                }
                            )

                            invite_done = True
                            break
                if not invite_done:
                    print("Invalid ID")
                    wait_for_enter()

    def __view_invitation_status(self):
        """
        Show pending member table that correspond to this lead student.
        :return:
        """

        pending_member_table = self.db.search('pending_member.csv')
        my_invitation = pending_member_table.filter(lambda invitation: invitation['lead'] == self.project['lead'])
        if len(my_invitation.table) != 0:

            # Show invitation if there are pending invitation
            my_invitation.filter(
                lambda invitation:
                    invitation['lead'] == self.project['lead'],
                new_name="Pending member"
            ).print_table()

            wait_for_enter()

        else:
            print("There are no pending member right at this time.")
            wait_for_enter()

    def __invite_advisor(self):
        """
        Show list of faculty and advisor that able to advise a group and sent invitation to them.
        """

        if self.project["advisor"] != "none":
            print("You already have advisor")
            wait_for_enter()
            return

        # Prepare table from database for further action
        pending_advisor_table = self.db.search('pending_advisor.csv')
        login_table = self.db.search('login.csv')

        if len(
                pending_advisor_table.filter(
                    lambda invitation:
                        invitation['lead'] == self.id and
                        invitation['status'] == 'pending'
                ).table
        ) != 0:

            # Show invitation if there are pending invitation
            pending_advisor_table.filter(
                lambda invitation:
                    invitation['lead'] == self.id and
                    invitation['status'] == 'pending',
                new_name="Pending member").print_table()
            wait_for_enter()

        else:

            # Show table of student who isn't a member in any project if there are no pending invitation
            login_table.filter(
                lambda able_person:
                    able_person["role"] == "faculty" or
                    able_person["role"] == "advisor",
                new_name="Faculty member list").print_table(exclude_key=['password'])

            # Let user input id of student that they want to invite
            invite_done = False
            while True:

                if invite_done:
                    break

                # Prompt user for ID
                user_id = get_str("Enter faculty member ID or type 0 to abort: ")

                if user_id == '0':
                    break

                # Check is ID available
                for person in login_table.table:
                    if person['ID'] == user_id:

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
                                    'pending_advisor': user_id,
                                    'status': "Pending"
                                }
                            )
                            invite_done = True
                            break

                if not invite_done:
                    print("Invalid ID")
                    wait_for_enter()

    def __ap_request(self, re_type):
        """
        Sent a proposal or report approve request to advisor depend on re_type param.
        :param re_type: proposal or report
        """

        # Prepare necessary table for further action
        pending_approve_table = self.db.search("pending_approve.csv")

        # Get pending request to check are their any ongoing request
        if re_type == "proposal":

            if self.project['status'] != 'Writing proposal':
                print("You can't send proposal approve request at this time")
                wait_for_enter()
                return

            if self.project['advisor'] == "none":
                print("You must invite advisor before request an approval")
                wait_for_enter()
                return

            my_request = pending_approve_table.filter(
                lambda request:
                    request['lead'] == self.id and
                    request['status'] == 'Proposal approve pending',
                new_name="Your Ongoing request")

        else:

            if self.project['status'] != 'Evaluated':
                print("You can't send report approve request at this time")
                wait_for_enter()
                return

            my_request = pending_approve_table.filter(
                lambda request:
                    request['lead'] == self.id and
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
                        'status': f'{re_type.title()} approve pending',
                        'type': re_type
                    }
                )
        else:
            my_request.print_table(new_line_key=["feedback"])
            wait_for_enter()

    def __eval_request(self):
        """
        Sent evaluate request to choose faculty member.
        """

        pending_eval = self.db.search('pending_eval.csv')

        # If project not in writing report state, user can't request an evaluate.
        if self.project["status"] == "Writing Report" or self.project['status'] == "Evaluated":
            pass
        else:
            print("You can't send evaluate request at this time")
            wait_for_enter()
            return

        ongoing = pending_eval.filter(
            lambda request:
            request['lead'] == self.id and
            request['status'] == "Evaluate request pending"
        )

        if len(ongoing.table) != 0:
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
        join_table = (login_table.join(person_table, "ID").filter(

            lambda able_person:
                (
                    able_person['role'] == 'faculty' or
                    able_person['role'] == 'advisor'
                )
                and able_person['ID'] != self.project['advisor'])

        )

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
                    if (
                            (person['role'] != 'advisor' and person['role'] != 'faculty') or
                            person["ID"] == self.project['advisor']
                    ):

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
        """
        Show past and pending evaluation.
        """

        pending_eval = self.db.search('pending_eval.csv')

        eval_his = pending_eval.filter(lambda request: request['lead'] == self.id)

        if len(eval_his.table) != 0:
            eval_his.print_table(new_line_key=['feedback'])
            wait_for_enter()
        else:
            print("No request history available")
            wait_for_enter()
        return

    def __view_proposal_approve_or_report_request(self, ap_type):
        """
        Show past report or proposal approve request depend of ap_type param.
        :param ap_type: report of proposal
        """

        my_request = self.db.search('pending_approve.csv').filter(
            lambda request:
                request['lead'] == self.project['lead'] and
                request['type'] == ap_type
        )

        if len(my_request.table) != 0:
            my_request.print_table(exclude_key=['type'], new_line_key=["feedback"])
            wait_for_enter()
            return
        else:
            print(f"You haven't sent {ap_type} approve yet")

    def __show_history(self):

        while True:

            choice = print_get_choice([
                'Member invite history',
                'Proposal approval request history',
                'Evaluate History',
                'Report approval request history'
            ], prompt="Which history and status you want to view: ")

            if choice == 0:
                return
            if choice == 1:
                self.__view_invitation_status()
            if choice == 2:
                self.__view_proposal_approve_or_report_request('proposal')
            if choice == 3:
                self.__eval_history()
            if choice == 4:
                self.__view_proposal_approve_or_report_request('report')

    def menu(self):
        """
        Show a list of action that lead student can perform.
        :return:
        """

        while True:

            choice = print_get_choice([
                'View project',
                'Invite member',
                'Invite Advisor',
                'Proposal approval request',
                'Report approval request',
                'Evaluate request',
                'View history'
            ])

            # 'Member invitation status', View request history' 'Evaluated history'
            if choice == 1:
                self.__view_project()
            elif choice == 2:
                self.__invite_member()
            elif choice == 3:
                self.__invite_advisor()
            elif choice == 4:
                self.__ap_request('proposal')
            elif choice == 5:
                self.__ap_request('report')
            elif choice == 6:
                self.__eval_request()
            elif choice == 7:
                self.__show_history()
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
    def __init__(self, username, user_id, db):
        # Construct attribute for lead student
        self.__username = username
        self.__id = user_id
        self.__db = db

        user_pro = db.search("project.csv").filter(lambda project: self.id in project["member"]).table[0]
        self.__project = user_pro

    def __print_project(self):

        print_project(self.project, self.db)

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

    def __view_proposal_approve_or_report_request(self, ap_type):

        my_request = self.db.search('pending_approve.csv').filter(
            lambda request:
                request['lead'] == self.project['lead'] and
                request['type'] == ap_type
        )

        if len(my_request.table) != 0:
            my_request.print_table(exclude_key=['type'], new_line_key=["feedback"])
            wait_for_enter()
            return
        else:
            print(f"You haven't sent {ap_type} approve yet")

    def __view_invitation_status(self):

        pending_member_table = self.db.search('pending_member.csv')
        my_invitation = pending_member_table.filter(lambda invitation: invitation['lead'] == self.project['lead'])
        if len(my_invitation.table) != 0:

            # Show invitation if there are pending invitation
            my_invitation.filter(
                lambda invitation:
                    invitation['lead'] == self.project['lead'],
                new_name="Pending member"
            ).print_table()

            wait_for_enter()

        else:
            print("There are no pending member right at this time.")
            wait_for_enter()

    def __eval_history(self):

        pending_eval = self.db.search('pending_eval.csv')

        eval_his = pending_eval.filter(lambda request: request['lead'] == self.project['lead'])

        if len(eval_his.table) != 0:
            eval_his.print_table(new_line_key=['feedback'])
            wait_for_enter()
        else:
            print("No request history available")
            wait_for_enter()
        return

    def __show_history(self):

        while True:

            choice = print_get_choice([
                'Member invite history',
                'Proposal approval request history',
                'Evaluate History',
                'Report approval request history'
            ], prompt="Which history and status you want to view")

            if choice == 0:
                return
            if choice == 1:
                self.__view_invitation_status()
            if choice == 2:
                self.__view_proposal_approve_or_report_request("proposal")
            if choice == 3:
                self.__eval_history()
            if choice == 4:
                self.__view_proposal_approve_or_report_request("report")

    def menu(self):
        while True:

            choice = print_get_choice(['View and edit project', 'View history and status'])

            if choice == 0:
                break
            elif choice == 1:
                self.__view_project()
            elif choice == 2:
                self.__show_history()

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
    def __init__(self, username, user_id, db):
        # Construct attribute for faculty member
        self.__username = username
        self.__id = user_id
        self.__db = db

    def __view_advisor_request(self):

        # Get necessary table for further action
        pending_advisor_table = self.db.search('pending_advisor.csv')
        all_project = self.db.search('project.csv')
        login_table = self.db.search('login.csv')

        if len(
                pending_advisor_table.filter(
                    lambda pending:
                        pending['pending_advisor'] == self.id and
                        pending['status'] == "Pending"
                ).table
        ) != 0:

            # Show invitation if there are pending invitation
            my_invitation = pending_advisor_table.filter(
                lambda pending:
                    pending['pending_advisor'] == self.id and
                    pending['status'] == "Pending", new_name="Pending invitation"
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
                    if invitation['pending_advisor'] == self.id and invitation['status'] == "Pending":
                        invitation['status'] = "Decline"
                        if invitation['project'] == choose_project:
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

        my_request = pending_eval_table.filter(
            lambda request_log:
                request_log['pending_committee'] == self.id and
                request_log['status'] == 'Evaluate request pending',
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
            print_project(choose_project, self.db)
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

            choice = print_get_choice(['Response advisor request', 'Evaluate Project'])

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
    def __init__(self, username, user_id, db):
        # Construct attribute for faculty member
        self.__username = username
        self.__id = user_id
        self.__db = db

        all_project = db.search('project.csv')
        self.__advising = [project for project in all_project.table if project['advisor'] == self.id]

    def __view_advisor_request(self):

        # Get necessary table for further action
        pending_advisor_table = self.db.search('pending_advisor.csv')
        all_project = self.db.search('project.csv')
        login_table = self.db.search('login.csv')

        if len(
                pending_advisor_table.filter(
                    lambda pending:
                        pending['pending_advisor'] == self.id and
                        pending['status'] == "Pending"
                ).table
        ) != 0:

            # Show invitation if there are pending invitation
            my_invitation = pending_advisor_table.filter(
                lambda pending:
                    pending['pending_advisor'] == self.id and
                    pending['status'] == "Pending",
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
                    if invitation['pending_advisor'] == self.id and invitation['status'] == "Pending":
                        invitation['status'] = "Decline"
                        if invitation['project'] == choose_project:
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

        print_project(project, self.db)
        wait_for_enter()

    def __view_advising_project(self):

        # Get list of project from attribute
        project_ls = [project['name'] for project in self.advising]

        while True:
            choose_project = print_get_choice(project_ls, exit_choice="Cancel", prompt="Choose a project to advise:")

            if choose_project == 0:
                return

            choose_project = self.advising[choose_project - 1]

            print_project(choose_project, self.db)
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

            my_request = pending_approve_table.filter(
                lambda request_log:
                    request_log['advisor'] == self.id and
                    request_log['status'] == 'Proposal approve pending',
                new_name="Your Ongoing request")

        else:

            my_request = pending_approve_table.filter(
                lambda request_log:
                    request_log['advisor'] == self.id and
                    request_log['status'] == 'Report approve pending',
                new_name="Your Ongoing request"
            )

        # If advisor don't have any ongoing request return to main menu.
        if len(my_request.table) == 0:
            print("There are no request right at this time")
            wait_for_enter()
            return

        my_request.print_table(exclude_key="feedback")
        wait_for_enter()

        # Get list of project name
        project_ls = [project['project'] for project in my_request.table]

        while True:
            # Prompt user which project to respond
            choose_project = print_get_choice(
                project_ls,
                exit_choice="Cancel",
                prompt=f"Choose a {re_type} to approve: "
            )

            # If user choose to cancel return back to menu
            if choose_project == 0:
                return

            # Set choose project to a name of project instead of index
            choose_project = project_ls[choose_project - 1]

            # Find matching project name inside advisee attribute than set choose project to dict of project instead.
            for advising in self.advising:
                if advising['name'] == choose_project:
                    choose_project = advising
                    break

            # Let user select to approve or not
            print_project(choose_project, self.db)
            action = print_get_choice(["Approve", "Unapprove"],
                                      exit_choice="Cancel",
                                      prompt=f"Approve this project's {re_type}?: ")

            if action == 0:
                continue

            feedback = get_str("Feedback: ")

            right_request = {}

            for request in pending_approve_table.table:

                if (
                        choose_project['lead'] == request['lead'] and
                        request['status'] == f"{re_type.title()} approve pending"
                ):

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

        my_request = pending_eval_table.filter(
            lambda request_log:
                request_log['pending_committee'] == self.id and
                request_log['status'] == 'Evaluate request pending',
            new_name="Your Ongoing request"
        )

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
            print_project(choose_project, self.db)
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

            choice = print_get_choice([
                'View advisor request',
                'View advising project',
                'Approve proposal',
                'Approve Report',
                'Evaluate Project'
            ])

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


class Admin:
    def __init__(self, username, user_id, db):
        # Construct attribute for lead student
        self.__username = username
        self.__id = user_id
        self.__db = db

    def __insert_table(self, table):

        print("Input data for each column")
        keys = list(table.table[0].keys())
        temp = {}
        for key in keys:
            temp[key] = get_str(key + ": ")
        table.insert(temp)

    def __view_and_insert_table(self, filename):

        choose_table = self.db.search(filename)

        if len(choose_table.table) == 0:
            print("No data available")
            wait_for_enter()
            return

        if filename == 'project.csv':
            self.__print_all_project()
        else:
            choose_table.print_table()

        wait_for_enter()

        while True:

            choice = print_get_choice(['Edit'])
            if choice == 1:
                self.__insert_table(choose_table)
            if choice == 0:
                break

    def __print_all_project(self):
        all_project = self.db.search('project.csv')

        if len(all_project.table) == 0:
            print("No data available")
            wait_for_enter()
            return

        for project in all_project.table:
            print_project(project, self.db)

    def menu(self):
        while True:
            choice = print_get_choice(
                [
                    'Login table',
                    'Pending member invitation table',
                    'Pending advisor invitation table',
                    'Pending approval table',
                    'Pending evaluate table',
                    'All project'
                ],
                prompt="Which table you want to view and insert: "
            )

            if choice == 1:
                self.__view_and_insert_table("login.csv")
            elif choice == 2:
                self.__view_and_insert_table('pending_member.csv')
            elif choice == 3:
                self.__view_and_insert_table('pending_advisor.csv')
            elif choice == 4:
                self.__view_and_insert_table('pending_approve.csv')
            elif choice == 5:
                self.__view_and_insert_table('pending_eval.csv')
            elif choice == 6:
                self.__view_and_insert_table('project.csv')
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
