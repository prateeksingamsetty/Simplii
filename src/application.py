from datetime import datetime, timedelta
from bson.objectid import ObjectId

from flask_wtf import form
from flask import app, render_template, session, url_for, flash, redirect, request, Response, Flask
from flask_pymongo import PyMongo
from flask import json
from flask.helpers import make_response
from flask.json import jsonify
from flask_mail import Mail, Message
from pymongo import ASCENDING
from forms import ForgotPasswordForm, RegistrationForm, LoginForm, ResetPasswordForm, PostingForm, ApplyForm, TaskForm, UpdateForm
import bcrypt
import os
import csv
import sys

from flask_login import LoginManager, login_required

app = Flask(__name__)
app.secret_key = 'secret'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/simplii'
mongo = PyMongo(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "dummysinghhh@gmail.com"
app.config['MAIL_PASSWORD'] = "wbjf dsfu mper nqfv"
mail = Mail(app)

@app.route("/")
@app.route("/home")
def home():
    ############################
    # home() function displays the homepage of our website.
    # route "/home" will redirect to home() function.
    # input: The function takes session as the input
    # Output: Out function will redirect to the login page
    # ##########################
    if session.get('email'):
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))


@app.route("/forgotPassword")
def forgotPassword():
    ############################
    # forgotPassword() redirects the user to dummy template.
    # route "/forgotPassword" will redirect to forgotPassword() function.
    # input: The function takes session as the input
    # Output: Out function will redirect to the dummy page
    # ##########################
    return redirect(url_for('dummy'))


@app.route("/recommend")
def recommend():
    ############################
    # recommend() function opens the task_recommendation.csv file and displays the data of the file
    # route "/recommend" will redirect to recommend() function.
    # input: The function opens the task_recommendation.csv
    # Output: Our function will redirect to the recommend page for showing the data
    # ##########################
    '''data = []
    with open(os.path.join(sys.path[0], "../models/task_recommendation.csv")) as f:
        reader = csv.DictReader(f)

        for row in reader:
            data.append(dict(row))

    return render_template('recommend.html', data=data, list=list)'''


    if session.get('user_id'):
        user_str_id = session.get('user_id')
        user_id = ObjectId(user_str_id)

        # Fetch all tasks for the user and sort by 'duedate' in ascending order
        tasks = list(mongo.db.tasks.find({'user_id': user_id}).sort('duedate', ASCENDING))

        # Convert 'duedate' strings to datetime objects for sorting
        for task in tasks:
            task['duedate'] = datetime.strptime(task['duedate'], '%Y-%m-%d')

        return render_template('recommend.html', title='Recommend', tasks=tasks)
    else:
        return redirect(url_for('home'))
    



@app.route("/send_email_reminders", methods=['GET', 'POST'])
def send_email_reminders():
    if session.get('user_id'):
        if request.method == 'POST':
            due_date = request.form.get('duedate')  # Get the due date input from the form
            user_str_id = session.get('user_id')
            user_id = ObjectId(user_str_id)

            
            # Convert the due date to a datetime object
            #due_date = datetime.strptime(due_date, '%Y-%m-%d')

            due_date=datetime.strptime(due_date, '%Y-%m-%d').date()
            
            

            # Calculate the current date
            current_date = datetime.now().date()

            print("Due Date",type(due_date))
            print("current_date",type(current_date))
        

            # Fetch tasks whose due date falls within the specified range
            relevant_tasks = mongo.db.tasks.find({
                'user_id': user_id,
                'duedate': {'$gte': current_date, '$lte': due_date}
            })

            for task in relevant_tasks:
            # Compose and send email reminders
                subject = "Task Reminder"
                recipients = [task['user_email']]  # Assuming you have a field for user email in tasks
                message_body = render_template('reminder_email_template.html', task=task)

                msg = Message(subject=subject, recipients=recipients, body=message_body)
                mail.send(msg)

            flash("Email reminders sent for tasks with due dates in the specified range.", 'success')

        # Continue with the rest of the code to display tasks and the input field
        # ...

    else:
        return redirect(url_for('home'))
    return render_template('mailsent.html', title='Recommend')




@app.route("/dashboard")
def dashboard():
    ############################
    # dashboard() function displays the tasks of the user
    # route "/dashboard" will redirect to dashboard() function.
    # input: The function takes session as the input and fetches user tasks from Database
    # Output: Our function will redirect to the dashboard page with user tasks being displayed
    # ##########################
    tasks = ''
    print('session in dashboard ',session)
    if session.get('user_id'):
        tasks = mongo.db.tasks.find({'user_id': ObjectId(session.get('user_id'))})
    return render_template('dashboard.html', tasks=tasks)


@app.route("/about")
def about():
    # ############################
    # about() function displays About Us page (about.html) template
    # route "/about" will redirect to about() function.
    # ##########################
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    # ############################
    # register() function displays the Registration portal (register.html) template
    # route "/register" will redirect to register() function.
    # RegistrationForm() called and if the form is submitted then various values are fetched and updated into database
    # Input: Username, Email, Password, Confirm Password
    # Output: Value update in database and redirected to home login page
    # ##########################
    if not session.get('email'):
        form = RegistrationForm()
        if form.validate_on_submit():
            if request.method == 'POST':
                username = request.form.get('username')
                email = request.form.get('email')
                password = request.form.get('password')
                mongo.db.users.insert_one({'name': username, 'email': email, 'pwd': bcrypt.hashpw(
                    password.encode("utf-8"), bcrypt.gensalt()), 'tasksList':[]})
            msg = Message('Welcome to Simplii: Your Task Scheduling Companion', sender='dummysinghhh@gmail.com', recipients=['dummysinghhh@gmail.com'])
            msg.body = f"Hey {username},\n\n" \
           "We're excited to welcome you to Simplii, your new task scheduling companion. Simplii is here to help you stay organized, meet deadlines, and achieve your goals efficiently.\n\n" \
           "With Simplii, you can schedule your tasks, set deadlines, and work on them with ease. Never miss an important deadline again!\n\n" \
           "Thank you for choosing Simplii. We're thrilled to have you on board. If you have any questions or need assistance, feel free to reach out to us.\n\n" \
           "Best regards,\n" \
           "The Simplii Team"
            mail.send(msg)
            print("Message sent!")
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/deleteTask", methods=['GET', 'POST'])
def deleteTask():
    ############################
    # deleteTask() function will delete the particular user task from database.
    # route "/deleteTask" will redirect to deleteTask() function.
    # input: The function takes email, task, status, category as the input and fetches from the database
    # Output: Out function will delete the particular user task from database
    # ##########################
    if request.method == 'POST':
        user_str_id = session.get('user_id')
        user_id = ObjectId(user_str_id)
        task = request.form.get('task')
        status = request.form.get('status')
        category = request.form.get('category')
        print("task, status, category ", task, status, category)
        id = mongo.db.tasks.find_one(
            {'user_id': user_id, 'taskname': task, 'status': status, 'category': category}, {'_id'})
        print("id in delete task ",id)
        mongo.db.tasks.delete_one({'_id': id['_id']})
        return "Success"
    else:
        return "Failed"


@app.route("/task", methods=['GET', 'POST'])
def task():
    # ############################
    # task() function displays the Add Task portal (task.html) template
    # route "/task" will redirect to task() function.
    # TaskForm() called and if the form is submitted then new task values are fetched and updated into database
    # Input: Task, Category, start date, end date, number of hours
    # Output: Value update in database and redirected to home login page
    # ##########################
    if session.get('user_id'): 
        form = TaskForm()
        if form.validate_on_submit():
            print("inside form")
            if request.method == 'POST':
                user_str_id = session.get('user_id')
                user_id = ObjectId(user_str_id)
                taskname = request.form.get('taskname')
                category = request.form.get('category')
                startdate = request.form.get('startdate')
                duedate = request.form.get('duedate')
                hours = request.form.get('hours')
                status = request.form.get('status')
                task_id = mongo.db.tasks.insert({'user_id': user_id,
                                       'taskname': taskname,
                                       'category': category,
                                       'startdate': startdate,
                                       'duedate': duedate,
                                       'status': status,
                                       'hours': hours})
                
                #Now update the user schema's TaskList field with the taskId(Basically append the new task id to that array)
                user_document = mongo.db.users.find_one({'_id': user_id})
                tasks_list = user_document.get('tasksList', [])
                tasks_list.append(task_id)

                # Update the user's tasksList field
                mongo.db.users.update_one(
                    {'_id': user_id},
                    {
                        '$set': {'tasksList': tasks_list}
                    }
                )
            flash(f' {form.taskname.data} Task Added!', 'success')
            return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))
    return render_template('task.html', title='Task', form=form)


@app.route("/editTask", methods=['GET', 'POST'])
def editTask():
    ############################
    # editTask() function helps the user to edit a particular task and update in database.
    # route "/editTask" will redirect to editTask() function.
    # input: The function takes email, task, status, category as the input
    # Output: Out function will update new values in the database
    # ##########################
    if request.method == 'POST':
        user_str_id = session.get('user_id')
        user_id = ObjectId(user_str_id)
        task = request.form.get('task')
        status = request.form.get('status')
        category = request.form.get('category')
        id = mongo.db.tasks.find_one(
            {'user_id': user_id, 'taskname': task, 'status': status, 'category': category})
        print("id in edit task ", id)
        return json.dumps({'taskname': id['taskname'], 'category': id['category'], 'startdate': id['startdate'], 'duedate': id['duedate'], 'status': id['status'], 'hours': id['hours']}), 200, {
            'ContentType': 'application/json'}
    else:
        return "Failed"


@app.route("/updateTask", methods=['GET', 'POST'])
def updateTask():
    ############################
    # updateTask() function displays the updateTask.html page for updations
    # route "/updateTask" will redirect to updateTask() function.
    # input: The function takes variious task values as Input
    # Output: Out function will redirect to the updateTask page
    # ##########################
    if session.get('user_id'):
        print("params in updateTask ", request.url)
        params = request.url.split('?')[1].split('&')
        for i in range(len(params)):
            params[i] = params[i].split('=')
        for i in range(len(params)):
            if "%" in params[i][1]:
                index = params[i][1].index('%')
                params[i][1] = params[i][1][:index] + \
                    " " + params[i][1][index + 3:]
        d = {}
        for i in params:
            d[i[0]] = i[1]

        form = UpdateForm()

        form.taskname.data = d['taskname']
        form.category.data = d['category']
        form.status.data = d['status']
        form.hours.data = d['hours']
        
        # Assuming that 'd['startdate']' and 'd['duedate']' are date strings in a format like 'YYYY-MM-DD'
        # Convert them to datetime objects
        startdate_str = d['startdate']
        duedate_str = d['duedate']
        # Convert to datetime objects
        startdate_datetime = datetime.strptime(startdate_str, '%Y-%m-%d')
        duedate_datetime = datetime.strptime(duedate_str, '%Y-%m-%d')

        # Now, set the datetime objects in the form
        form.startdate.data = startdate_datetime
        form.duedate.data = duedate_datetime
        

        if form.validate_on_submit():
            if request.method == 'POST':
                user_str_id = session.get('user_id')
                user_id = ObjectId(user_str_id)
                taskname = request.form.get('taskname')
                category = request.form.get('category')
                startdate = request.form.get('startdate')
                duedate = request.form.get('duedate')
                hours = request.form.get('hours')
                status = request.form.get('status')
                mongo.db.tasks.update({'user_id': user_id, 'taskname': d['taskname'], 'startdate': d['startdate'], 'duedate': d['duedate']},
                                      {'$set': {'taskname': taskname, 'startdate': startdate, 'duedate': duedate, 'category': category, 'status': status, 'hours': hours}})
            flash(f' {form.taskname.data} Task Updated!', 'success')
            return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('home'))
    return render_template('updateTask.html', title='Task', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    # ############################
    # login() function displays the Login form (login.html) template
    # route "/login" will redirect to login() function.
    # LoginForm() called and if the form is submitted then various values are fetched and verified from the database entries
    # Input: Email, Password, Login Type
    # Output: Account Authentication and redirecting to Dashboard
    # ##########################
    if not session.get('user_id'):
        form = LoginForm()
        if form.validate_on_submit():
            temp = mongo.db.users.find_one({'email': form.email.data}, {
                'email', 'name', 'pwd'})
            print("temp ", temp)
            if temp is not None and temp['email'] == form.email.data and (
                bcrypt.checkpw(
                    form.password.data.encode("utf-8"),
                    temp['pwd']) or temp['temp'] == form.password.data):
                flash('You have been logged in!', 'success')
                session['email'] = temp['email']
                session['name'] = temp['name']
                session['user_id'] = str(temp['_id'])
                return redirect(url_for('dashboard'))
            else:
                flash(
                    'Login Unsuccessful. Please check username and password',
                    'danger')
    else:
        print("session details ", session)
        return redirect(url_for('home'))
    return render_template(
        'login.html',
        title='Login',
        form=form)


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    # ############################
    # logout() function just clears out the session and returns success
    # route "/logout" will redirect to logout() function.
    # Output: session clear
    # ##########################
    session.clear()
    return "success"


@app.route("/dummy", methods=['GET'])
def dummy():
    # ############################
    # dummy() function performs the functionality displaying the message "feature will be added soon"
    # route "/dummy" will redirect to dummy() function.
    # Output: redirects to dummy.html
    # ##########################
    """response = make_response(
                redirect(url_for('home'),200),
            )
    response.headers["Content-Type"] = "application/json",
    response.headers["token"] = "123456"
    return response"""
    return "Page Under Maintenance"


if __name__ == '__main__':
    app.run(debug=True)
