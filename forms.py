from flask_wtf import Form
from flask import flash
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, \
                    RadioField, SelectField, validators, ValidationError, BooleanField \
                    
from models import Moduly
import sqlite3
from wtforms_alchemy import ModelForm







class ContactForm(Form):
   name = TextField("Name Of Student",[validators.Required("Please enter your name.")])
   Gender = RadioField('Gender', choices = [('M','Male'),('F','Female')])
   Address = TextAreaField("Address")
   
   email = TextField("Email",[validators.Required("Please enter your email address."),
      validators.Email("Please enter your email address.")])
   
   Age = IntegerField("age")
   language = SelectField('Languages', choices = [('cpp', 'C++'), 
      ('py', 'Python')])
   submit = SubmitField("Send")
   
class LoginForm(Form):
    openid = TextField('openid', validators=[validators.DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
   
   
class UrzadzeniaForm(Form):
   name = TextField('nazwa', validators=[validators.DataRequired()])
   rejestr = IntegerField('rejestr')
   sterowanie = SelectField('sterowanie', choices = ['on/off','0-100%','RGB','Tylko do odczytu'])
   wartosc = IntegerField('wartosc')
   wartosc2 =IntegerField('wartosc2')
   wartosc3 =IntegerField('wartosc3')

class NewModuleForm(Form):
   name = TextField('name', validators=[validators.DataRequired()])
   id = IntegerField('id')
   
class KameraForm(Form):
   name = TextField('name', validators=[validators.DataRequired()])

   
