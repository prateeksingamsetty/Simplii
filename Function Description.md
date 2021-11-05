refresh_data()
- This function loads all the data required to display the home page from file system

getnewTaskID()
- This function is used to generate a new unique TaskID. All our TaskIDs are alphanumeric strings of length 5. Eg. “AAAA2”, “2342V”. No special characters are used for obtaining TaskIDs
- This function randomly produces a possible TaskID and checks if it is already in use. If the generated TaskID is in use, then we keep on generating random TaskIDs until we find one that is not in use

homePage()
- This function renders the home page

login()
- This function is used for login by the user
- Using userID, passoword is validated and the user is directed to index

send_email()
- This function is used to send an email to user's email ID containing all tasks
- The email is sent from simplii.reminder@gmail.com

logout()
- This function is used for login by the user
- Using userID, passoword is validated and the user is directed to index

signUp()
- This function is used for registering new users
- Details of new users are stored in the database and the user is automatically logged in

delete_task_byID()
- Deletes a task from the to-do list given its ID. This API moves a task from the TODO list to the COMPLETED list

add_new_task()
- User fills details of tasks on a form which gets added to the database
- User can also see their tasks and their details on index page

delete_task_byID()
- This function deletes the tasks that are already stored by the user
