# **Todo list of final project**

## **General** 
  - Implement project table class to store information for each project.
  - Implement member request pending table. To keep track of each invitation and make other student able to view their own invitation to project.
  - Implement advisor request pending table. work same as member request pending table but for faculty member.
  - Implement login table to collect information of each user information that require for login.
  - Implement Approve request table to keep track approve status for each project
  - Implement Approve request table to keep track evaluate status for each project


## **Each role todo list**

  - In every class will have common method which is menu method to let user choose which action they will perform
  
  - ### ***student***
    - Implement student class to store action that student can perform. In student class will contain the following
      * *Attribute*
        - Username
        - User's ID
      * *Method*
        - View invitation for lead student and able to accept or deny invitation.
        - Start a project and turn into Lead student.

  - ### ***Lead student***
    - Implement lead student class to store action that lead student can perform. In student lead class will contain the following
      * *Attribute*
        - Username
        - User's ID
        - Project name
      * *Method*
        - Sent invitation to other student to join their group which. They can have only one pending invitation at the same time. Student who got invited must responded before lead student invite another student. In their group they're allowed to have at most 3 member which is 1 lead and 2 member.
        - Sent invitation to faculty member to be their advisor.
        - See and modified their own project.
        - Submit project proposal to let their advisor approve.
        - Submit their project report to let faculty member evaluate.
        - Approve member leave request.

  - ### ***Member***
    - Implement member class to store action that member can perform. In member class will contain the following
      * *Attribute*
        - Username
        - User's ID
        - Project name
      * *Method*
        - View and modified their project.
        - Leave group

  - ### ***Faculty member***
    - Implement member class to store action that faculty member can perform. In faculty member class will contain the following
      * *Attribute*
        - Username
        - User's ID
      * *Method*
        - View and respond advisor request. One faculty member may have multiple advisee
        - See detail of all project
        - Evaluate project report and choose to approve or feedback project.
        
  - ### ***Advisor***
    - Implement Advisor class to store action that Advisor can perform. In Advisor class will contain the following
        * *Attribute*
          - Username
          - User's ID
          - Advisee project
        * *Method*
          - View their advisee project.
          - View a proposal approve request from their advisee and choose to approve or feedback
          - Evaluate project report and choose to approve or feedback project.
