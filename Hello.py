from flask import   Flask, redirect, g, url_for, flash, \
                    request, render_template, make_response, session, abort, jsonify, Response
import random, string, sqlite3, os, wtforms
from werkzeug import secure_filename
from forms import ContactForm, LoginForm, NewModuleForm, UrzadzeniaForm
from models import Moduly, Urzadzenia
from __init__ import app, db
from modbusmaster import writeRegister, readRegisters, writeMultipleRegisters
from datetime import datetime
from config import WARSAW




##########################################################################################
########################################FUNKCJE###########################################
##########################################################################################


def zapisPoOdczycie(address, rejestrPoczatkowy, liczbaRejestrow):
    
    dane = readRegisters(address,rejestrPoczatkowy,liczbaRejestrow)
    
    if 'Problem' in dane:
        return dane
    
    if dane != -1:
        urzadzenie = Urzadzenia.query.filter_by(modul_id = address, rejestr = rejestrPoczatkowy).first()
        if len(dane) == 1 and urzadzenie.sterowanie == "on/off":
            
            urzadzenie.stan = dane[0]
            db.session.commit()

        elif len(dane) == 1 and (urzadzenie.sterowanie == "odczyt temperatura" or "odczyt prad" or "odczyt wilgotnosc" or "odczyt cisnienie" or "tylko do odczytu" or "odczyt PIR"):
            
            urzadzenie.wartosc = dane[0]
            db.session.commit()

        # elif len(dane) == 2:
        #     
        #     urzadzenie.stan = dane[0]
        #     urzadzenie.wartosc = dane[1]
        #     db.session.commit()
            
        elif len(dane) == 4:
            
            urzadzenie.stan = dane[0]
            urzadzenie.r = dane[1]
            urzadzenie.g = dane[2]
            urzadzenie.b = dane[3]
            db.session.commit()
            
        else:
            
            return -1
        
        
def prepare_for_json3(_modul, status):
    modul = dict()
    _urzadzenia = dict()
    for i in range(len(_modul.urzadzenia.all())):
        _urzadzenia['%s' %i] = {
            'id': _modul.urzadzenia.all()[i].id,
            'name': _modul.urzadzenia.all()[i].name,
            'rejestr': _modul.urzadzenia.all()[i].rejestr,
            'sterowanie': _modul.urzadzenia.all()[i].sterowanie,
            'wartosc': _modul.urzadzenia.all()[i].wartosc,
            'r': _modul.urzadzenia.all()[i].r,
            'g': _modul.urzadzenia.all()[i].g,
            'b': _modul.urzadzenia.all()[i].b,
            'stan': _modul.urzadzenia.all()[i].stan,
            'status': status[i]
                
        }
        
    modul['name']= _modul.name
    modul['urzadzenia'] = _urzadzenia
    modul['id'] = _modul.id
    
    return modul

#########################################################################################
        ###########################INDEX#####################################
#########################################################################################
        

@app.route('/', methods=['GET','POST'])
def index():
    if 'username' in session:
        username = session['username']
        password = session['password']
        if username == 'bms' and password == 'bms':
            liczba_modulow = len(Moduly.query.all())
            return render_template('main.html', Moduly = Moduly.query.all(), Urzadzenia = Urzadzenia.query.all(),liczba_modulow = liczba_modulow)
    return redirect(url_for('login'))



#########################################################################################
        ###########################LOGIN#####################################
#########################################################################################
        


@app.route('/login',methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        if session['username'] == 'bms' and session['password'] == 'bms':
            flash("Zalogowano pomyslnie","success")
            
            return redirect(url_for('index'))
        else:
            flash("Zly login lub haslo", "warning")
            return render_template('login.html')
        
    return render_template('login.html')


#########################################################################################
        ###########################DODAJMODUL#####################################
#########################################################################################
        

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
    form = NewModuleForm()
    if request.method == 'POST':    ## Po kliknieciu submit w newmodule.html
        if form.validate_on_submit(): ## warunki w forms.py

            modul = Moduly(name=request.form['name'], id = request.form['id'])
            ## Nowa instancja klasy Moduly
                                                                          ## zainicjowana przy uzyciu danych z
                                                                          ## formularza newmodule.html
            
            db.session.add(modul)                                           ## dodanie instancji Moduly do sesji
            db.session.commit()                                             ## dodanie instacji Moduly do bazy
            
            flash('record successfully added')
            return redirect(url_for('index'))
        else:
            return redirect(url_for('addrec'))
    elif request.method == 'GET': ## Po wejsciu przyciskiem z list.html
        return render_template('newmodule.html', form = form) ## Przeslanie formy do newmodule.html
    
 #########################################################################################
        ###########################EDIT#####################################
#########################################################################################

# @app.route('/editrec', methods = ['POST', 'GET'])
# def editrec():
#     
#     if request.method == "POST":        ## po wcisnieciu edit przy dowolnym module
#     
#         modulDoEdycji = request.form['id']      ## pobranie id wybranego modulu, id - nazwa pola hidden input
#                                                 ## w list.html, ktory przechowuje id wybranego do edycji modulu
#         flash("%s" %modulDoEdycji)
#         edit = Moduly.query.filter_by(id = modulDoEdycji).first()  # pobranie instancji Moduly o podanym id
#         form = NewModuleForm()                                     # wybranie formy
#         # form['name'] = edit.name
#         flash(edit.name)
#         form.name.data = edit.name                              ## nadanie formie wartosci poczatkowych,
#         form.value1.data = edit.value1                          ## czyli tych ktore byly wczesniej w bazie
#         form.value2.data = edit.value2                          ## pod danym id
#         form.value3.data = edit.value3                          ##
#         
# 
#         
#         return render_template('editmodule.html', edit = edit, form = form) ## edit- do przechowania id modulu
#                                                                             ## form- forma do edycji danych
# 
#             
#             
#     return Response(status = 404)  ## jezeli request method = get

 #########################################################################################
        ###########################ZAPIS#####################################
#########################################################################################

# @app.route('/save', methods = ['POST', 'GET'])
# def zapis():
#     form=NewModuleForm()
#     if request.method == 'POST' and form.validate_on_submit():
# 
#         edit = Moduly.query.filter_by(id = request.form['address']).first() ## pobranie id do edycji
#                                                                             ## z editmodule.html i pobranie
#                                                                             ## modulu o danym id
# 
#         if str(request.form['name']) != edit.name or\
#         int(request.form['value1']) != edit.value1 or\
#         int(request.form['value2']) != edit.value2 or\
#         int(request.form['value3']) != edit.value3:         ## jezeli ktores z pol formularza ulegnie zmianie
# 
#             edit.name = request.form['name']                ## zapisanie nowych wartosci 
#             edit.value1 = request.form['value1']            ## z formularza do obiektu,
#             edit.value2 = request.form['value2']            ## ktory zostal wczesniej
#             edit.value3 = request.form['value3']            ## pobrany
#             db.session.commit()                             ## zapisanie do bazy
#             return redirect(url_for('list'))
#         return redirect(url_for('list'))
#     else:
#         edit = Moduly.query.filter_by(id = request.form['address']).first()
#         return render_template('editmodule.html',form = form, edit = edit)
        
 #########################################################################################
        ###########################LISTY#####################################
#########################################################################################
         
#### URZADZENIA   
@app.route('/list', methods = ['POST','GET'])
def list():

    return render_template("list.html", Moduly = Moduly.query.all())

#### MODULY
@app.route('/list2', methods = ['POST','GET'])
def list2():

    return render_template("list2.html", Moduly = Moduly.query.all())
        

#########################################################################################
        ###########################LOGOUT#####################################
#########################################################################################
        
    
@app.route('/logout')
def logout():

   session.pop('username', None)
   flash("Wylogowano","success")
   return redirect(url_for('index'))


#########################################################################################
#########################################################################################
        ###########################PRAWIE REST#####################################
#########################################################################################
#########################################################################################



#########################################################################################
        ###########################GET#####################################
#########################################################################################

@app.route('/moduly', methods = ['GET'])
def moduly_get():
    
    all_modules = Moduly.query.all()

    status = [[0 for x in range(10)] for y in range(len(all_modules))] 

    for i in range(len(all_modules)):
        
        size = len(all_modules[i].urzadzenia.all())
        
        for j in range(size):
            
            urzadzenie = all_modules[i].urzadzenia.all()[j]
            
            if urzadzenie.sterowanie == 'RGB':
                status[i][j] = zapisPoOdczycie(all_modules[i].id,urzadzenie.rejestr,4)
                print(status)

            else:
                status[i][j] = zapisPoOdczycie(all_modules[i].id,urzadzenie.rejestr,1)
                print(status)

    i = 0
    moduly = []
    date = datetime.now(tz=WARSAW).strftime('%Y-%m-%d %H:%M:%S')
    all_modules = Moduly.query.all()
    for modul in all_modules:
        
        item = prepare_for_json3(modul,status[i])
        moduly.append(item)
        i+=1
        
    i = 0
       
    return jsonify({'moduly': moduly, 'date': date})


#########################################################################################
        ###########################POST#####################################
#########################################################################################

@app.route('/moduly', methods = ['POST'])
def moduly_post():
    
    zadanie = request.json

    
    if ('nazwa' in zadanie): 
        urzadzenie = Urzadzenia()
        urzadzenie.name = request.json['nazwa']
        urzadzenie.rejestr = request.json['rejestr']
        urzadzenie.modul_id = request.json['id_modul']
        urzadzenie.sterowanie = request.json['sterowanie']
        urzadzenie.stan = request.json['zakres']

        
        db.session.add(urzadzenie)
        db.session.commit()
    elif ('r' in zadanie):
        urzadzenie = Urzadzenia.query.filter_by(modul_id = request.json['modul_id'], rejestr = request.json['rejestr']).first()
        urzadzenie.r = request.json['r']
        urzadzenie.g = request.json['g']
        urzadzenie.b = request.json['b']
        
        
        
        # wyslij = writeRegister(request.json['modul_id'],request.json['rejestr']+1,request.json['r'])
        # wyslij2 = writeRegister(request.json['modul_id'],request.json['rejestr']+2,request.json['g'])
        # wyslij3 = writeRegister(request.json['modul_id'],request.json['rejestr']+3,request.json['b'])
        
        wyslij = writeMultipleRegisters(request.json['modul_id'], request.json['rejestr'], [1,request.json['r'],request.json['g'],request.json['b']])
        
        
        if wyslij == 1:
            db.session.commit()
        
        

    elif ('stan' in zadanie):
        urzadzenie = Urzadzenia.query.filter_by(modul_id = request.json['modul_id'], rejestr = request.json['rejestr']).first()
        urzadzenie.stan = request.json['stan']
        
        wyslij = writeRegister(request.json['modul_id'],request.json['rejestr'],request.json['stan'])
        
        if wyslij == 1:
            db.session.commit()
    
    elif ('wartosc' in zadanie):
        urzadzenie = Urzadzenia.query.filter_by(modul_id = request.json['modul_id'], rejestr = request.json['rejestr']).first()
        urzadzenie.wartosc = request.json['wartosc']
        print urzadzenie.wartosc
        
        wyslij = writeRegister(request.json['modul_id'],request.json['rejestr'],request.json['wartosc'])
        
        if wyslij == 1:
            db.session.commit()
    elif ('address' in zadanie):
        
        wyslij = writeRegister(0,0,request.json['address']) 
        
        if wyslij == 1:
            print "dziala"
    
    

        
    return Response(status=200)

#########################################################################################
        ###########################DELETE#####################################
#########################################################################################

@app.route('/moduly', methods = ['DELETE'])
def moduly_delete():
    if (request.json['rejestr'] == 0):
        modul = Moduly.query.filter_by(id = request.json['modul']).first()
        for urzadzenie in modul.urzadzenia.all():
            db.session.delete(urzadzenie)
        db.session.delete(modul)
        db.session.commit()
        return Response(status=200)
        
    else:
        urzadzenie = Urzadzenia.query.filter_by(modul_id = request.json['modul'], rejestr = request.json['rejestr']).first()
        
        db.session.delete(urzadzenie)
        db.session.commit()
        return Response(status=200)

#########################################################################################
        ###########################SCENY#####################################
#########################################################################################
@app.route('/sceny', methods = ['GET'])
def scena():
    return render_template('sceny.html', Moduly = Moduly.query.all())

#########################################################################################
#*************************************RUN**********************************************#
#########################################################################################

if __name__ == '__main__':
    db.create_all()
    app.run(debug = True, host='0.0.0.0')
    #80.238.123.9


