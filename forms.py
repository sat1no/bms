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
   
class NewModuleForm(Form):
   name = TextField('name', validators=[validators.DataRequired()])
   value1 = IntegerField('value1', validators=[validators.DataRequired()])
   value2 = IntegerField('value2', validators=[validators.Optional()])
   value3 = IntegerField('value3', validators=[validators.Optional()])
   
   def validate_name(form, field):
      if len(field.data) < 4:
         raise ValidationError(flash("za krotko"))