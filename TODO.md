Todo list of final project

General 
- Implement project table class to store information for each project.
- Implement member request pending table. To keep track of each invitation and make other student able to view their own invitation to project.
- Implement advisor request pending table. work same as member request pending table but for faculty member.
- Implement login table to collect information of each user information that require for login.

Each role action outline 

A student
    - Able to get an invitation from lead student to join a project then accept and change row to member student or decline invitation.
    - Start their own project to become lead student.

Lead student
    - Able to sent invitation to other student in a database who has a student role, But lead student can have only 1 pending invitation.
    - After sent an invitation lead student are able to view a responded of other student.
    - Sent request to faculty member to be their project advisor.

Member
    - Able to view and modified project status in project table.

faculty
    - Able to view advisee request and choose to accept and change role to advisor or not.

Advisor
    - View and edit project.
    - Approve project proposal.
    - Evaluate and apprrove project report