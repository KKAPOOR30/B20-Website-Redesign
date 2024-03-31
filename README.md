B20 assignment 3

To do:

Database:
- person(username,email,password(i hashed it),type{student or insturctor})
- Students(f_name, l_name, stud_id, email, password(HASHED))
- Professor(f_name, l_name, email, password)
- Courses(Code, prof_email)
- Grades(stud_id, A1, A2, A3, Tutorials, Midterm, Exam, Final)
- Feedbacks(prof_email, Feedback)

Do we need to check if thats an acc student number or prof number?
Do we need the teacher accept the student or can anybody just sign up?


Login page:

- Options for Signup and Login 
- if Signup then show signup form :
    (Prof or student, 
    first name,
    last name,
    student/prof number,
    email,
    passward,
    confirm pasword,
    Submit)
- if log in then show login form :
    (Prof or Student,
    email,
    password,
    submit
    If valid then log in and redirect othrewise message to try again)


Website:

General: 
- Fix some of the pages that are very basic or incomplete
- Add a logout and profile area and 

For Students:
- Add a Grades Page with grades and remark box and button with each grade
- Update the Feedback form with the new questions and let him select the instructor

For Instructors:
- Need an are with all students and their grades
- Need a page to display all the feedback given to the specific instructor
- Should be able to update any marks for any student
- Should be able to Add or Update news, assignments, labs, or tutorials pages (NOT SURE IF WE NEED TO DO THIS)
