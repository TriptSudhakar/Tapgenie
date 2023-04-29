
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from flask import Flask,request, session, url_for, flash, redirect
from flask_wtf import FlaskForm
from wtforms.validators import ValidationError
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo

app = Flask(__name__,template_folder='templates',static_folder='static')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'dummypwd'
app.config['MYSQL_DB'] = 'tapgenie'
mysql = MySQL(app)


def email_exist_check(form, field):
    email_ID = form.email.data
    password = form.password.data
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM customer WHERE email_ID = % s', (email_ID, ))
    acc=cursor.fetchone()
    if acc:
        raise ValidationError('Account already exists!')

def email_exist_checkP(form, field):
    email_ID = form.email.data
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM professional WHERE email_ID = % s', (email_ID, ))
    acc=cursor.fetchone()
    if acc:
        raise ValidationError('Account already exists!')


    # else:
    #     cursor.execute('INSERT INTO customer VALUES (% s, % s, % s,%s)', (name,mobile_no,username,password))
    #     mysql.connection.commit()
    #     msg = 'You have successfully registered !'


def check_email_DNE(form, field):
    email_ID = form.email.data
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM customer WHERE email_ID = % s', (email_ID, ))
    acc=cursor.fetchone()
    if not acc and not Email()(form, field):
        raise ValidationError('Account does not exist!')

def check_passwd(form, field):
    email_ID = form.email.data
    password = form.password.data

    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM customer WHERE email_ID = % s AND password = % s', (email_ID, password, ))
    acc=cursor.fetchone()

    cursor.execute('SELECT * FROM customer WHERE email_ID = % s', (email_ID, ))
    bcc=cursor.fetchone()

    if (not acc) and bcc:
        raise ValidationError('Wrong password!')
    elif (acc is not None):
        session['loggedin']= True
        session['id']=acc['Customer_ID']
        session['email']=acc['email_ID']

def check_email_DNEP(form, field):
    email_ID = form.email.data
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM professional WHERE email_ID = % s', (email_ID, ))
    acc=cursor.fetchone()
    if not acc and not Email()(form, field):
        raise ValidationError('Account does not exist!')

def check_passwdP(form, field):
    email_ID = form.email.data
    password = form.password.data

    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM professional WHERE email_ID = % s AND password = % s', (email_ID, password, ))
    acc=cursor.fetchone()

    cursor.execute('SELECT * FROM professional WHERE email_ID = % s', (email_ID, ))
    bcc=cursor.fetchone()

    if (not acc) and bcc:
        raise ValidationError('Wrong password!')
    elif (acc is not None):
        session['loggedin']= True
        session['id']=acc['professional_ID']
        session['email']=acc['email_ID']

    

class RegistrationForm(FlaskForm):
    name = StringField('Name',
                           validators=[DataRequired(), Length(min=1, max=50)])
    
    # username = StringField('Username',
    #                        validators=[DataRequired(), Length(min=2, max=20)])
    
    email = StringField('Email',
                           validators=[DataRequired(), Email(), email_exist_check]) 
    phone_number = StringField('Mobile Number',
                           validators=[DataRequired(), Length(min=10, max=12)])
    
    password = PasswordField('Password', validators=[DataRequired()])
    
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), check_email_DNE])
    password = PasswordField('Password', validators=[DataRequired(), check_passwd])
    # /remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class LoginFormP(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), check_email_DNEP])
    password = PasswordField('Password', validators=[DataRequired(), check_passwdP])
    # /remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RegistrationFormP(FlaskForm):
    name = StringField('Name',
                           validators=[DataRequired(), Length(min=1, max=50)])
    
    # username = StringField('Username',
    #                        validators=[DataRequired(), Length(min=2, max=20)])
    
    email = StringField('Email',
                           validators=[DataRequired(), Email(), email_exist_checkP]) 
    
    phone_number = StringField('Mobile Number',
                           validators=[DataRequired(), Length(min=10, max=12)])
    
    password = PasswordField('Password', validators=[DataRequired()])
    
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    
    # profession = StringField('Profession',
    #                                  validators=[DataRequired(),Length(min=1, max=50)])
    profession = SelectField('Profession',
                             choices=[('Barber','Barber'),
                                      ('Masseuse','Masseuse'),
                                      ('Cleaner','Cleaner'),
                                      ('Plumber','Plumber'),
                                      ('Carpenter','Carpenter'),
                                      ('Beautician','Beautician'),
                                      ('Painter','Painter'),
                                      ('Electrician','Electrician'),
                                      ('Technician','Technician'),
                                      ('Exterminator','Exterminator'),
                                      ],
                             validators=[DataRequired(),Length(min=1, max=50)])
    submit = SubmitField('Sign Up')