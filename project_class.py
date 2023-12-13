from helper import get_int, get_str, print_get_choice


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
            "advisor": "none",
            "status": "Writing proposal",
            "approve_count": 0
        })
        login_table = self.db.search("login.csv").table

        for user in login_table:
            if user["ID"] == self.id:
                user["role"] = "lead"

        user = Lead(self.username, self.id, self.db)
        user.menu()


    def __view_invite(self):
        pass

    def menu(self):
        while True:
            # Print action that user able to perform.
            print("""
        [1] Start a project
        [2] View invitation
        [3] Exit
            """)

            # Call a method depend on user choice
            choice = get_int("Enter your choice: ", 1, 3)
            if choice == 1:
                self.__start_project()
                break
            elif choice == 2:
                self.__view_invite()
            elif choice == 3:
                break


class Lead:
    def __init__(self, username, id, db):
        self.__username = username
        self.__id = id
        self.__db = db

        user_pro = db.search("project.csv").filter(lambda project: project["lead"] == self.id).table[0]
        self.__project = user_pro

    def __print_project(self):

        # Print project detail
        # ==============================================#
        print()
        print(f"Project name: {self.project['name']}")
        member = self.project['member'].split("/")
        print(f"Member 1: {member[0]}")
        print(f"Member 2: {member[1]}")
        print(f"advisor: {self.project['advisor']}")
        print(f"Detail: {self.project['detail']}")
        print(f"Lead: {self.project['lead']}")
        print(f"status: {self.project['status']}")
        print(f"Proposal: {self.project['proposal']}")
        print(f"Report: {self.project['report']}")
        # ==============================================#

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

    def __view_project(self):

        self.__print_project()

        while True:

            choice = print_get_choice(['Edit'])
            if choice == 1:
                edit_choice = print_get_choice(['Project name', 'Detail', 'Proposal', 'Report'])
                if edit_choice != 0:
                    self.__edit_project(edit_choice)
            if choice == 0:
                break

    def menu(self):

        while True:

            choice = print_get_choice(['View project', 'Invite member', 'Invite Advisor'])

            if choice == 1:
                self.__view_project()
            elif choice == 2:
                pass
            elif choice == 3:
                pass
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



