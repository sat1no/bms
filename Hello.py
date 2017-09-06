from flask import   Flask, redirect, g, url_for, flash, \
                    request, render_template, make_response, session, abort, jsonify, Response
import random, string, sqlite3, os, wtforms
from werkzeug import secure_filename
from forms import ContactForm, LoginForm, NewModuleForm, UrzadzeniaForm
import flask_sijax
from models import Moduly, Urzadzenia
from __init__ import app, db




flask_sijax.Sijax(app)

# class Moduly(db.Model):
#     id = db.Column('modul_id',db.Integer, primary_key = True)
#     name = db.Column(db.String(100))
#     value1 = db.Column(db.Integer)  
#     value2 = db.Column(db.Integer)
#     value3 = db.Column(db.Integer)
#     # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     
#     def __init__(self, name, value1, value2, value3):
#         self.name = name
#         self.value1 = value1
#         self.value2 = value2
#         self.value3 = value3   
#    


def prepare_for_json(modul):
    nowy = dict()
    nowy['name']=modul.name
    nowy['value1']=modul.value1
    nowy['urzadzenia']=[]
    for i in range(len(modul.urzadzenia.all())):
        nowy['urzadzenia'].append(modul.urzadzenia.all()[i].id)
        nowy['urzadzenia'].append(modul.urzadzenia.all()[i].name)
        nowy['urzadzenia'].append(modul.urzadzenia.all()[i].rejestr)
        nowy['urzadzenia'].append(modul.urzadzenia.all()[i].sterowanie)
        nowy['urzadzenia'].append(modul.urzadzenia.all()[i].wartosc)
        nowy['urzadzenia'].append(modul.urzadzenia.all()[i].r)
        nowy['urzadzenia'].append(modul.urzadzenia.all()[i].g)
        nowy['urzadzenia'].append(modul.urzadzenia.all()[i].b)    
    return nowy

def prepare_for_json3(_modul):
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
            'stan': _modul.urzadzenia.all()[i].stan
            
            
        }
            

            
        
    modul['name']= _modul.name
    modul['urzadzenia'] = _urzadzenia
    modul['id'] = _modul.id
    
    return modul

def prepare_for_json2(urzadzenia):
    nowy = dict()
    nowy['name']=urzadzenia.name
    nowy['rejestr']=urzadzenia.rejestr
    return nowy
#########################################################################################
        ###########################INDEX#####################################
#########################################################################################
        

@app.route('/', methods=['GET','POST'])
def index():
    # if 'username' in session:
    #     username = session['username']
    liczba_modulow = len(Moduly.query.all())
    return render_template('main.html', Moduly = Moduly.query.all(), Urzadzenia = Urzadzenia.query.all(),liczba_modulow = liczba_modulow)
    # return redirect(url_for('login'))


@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)


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


@app.route('/login2', methods=['GET', 'POST'])
def login2():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
        return redirect('/list')
    return render_template('login2.html', 
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])
#########################################################################################
        ###########################DODAJMODUL#####################################
#########################################################################################
        

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
    form = NewModuleForm()
    if request.method == 'POST':    ## Po kliknieciu submit w newmodule.html
        if form.validate_on_submit(): ## warunki w forms.py

            modul = Moduly(name=request.form['name']) ## Nowa instancja klasy Moduly
                                                                          ## zainicjowana przy uzyciu danych z
                                                                          ## formularza newmodule.html
            
            db.session.add(modul)                                           ## dodanie instancji Moduly do sesji
            db.session.commit()                                             ## dodanie instacji Moduly do bazy
            
            flash('record successfully added')
            return redirect(url_for('list'))
        else:
            return redirect(url_for('addrec'))
    elif request.method == 'GET': ## Po wejsciu przyciskiem z list.html
        return render_template('newmodule.html', form = form) ## Przeslanie formy do newmodule.html
    
 #########################################################################################
        ###########################EDIT#####################################
#########################################################################################

@app.route('/editrec', methods = ['POST', 'GET'])
def editrec():
    
    if request.method == "POST":        ## po wcisnieciu edit przy dowolnym module
    
        modulDoEdycji = request.form['id']      ## pobranie id wybranego modulu, id - nazwa pola hidden input
                                                ## w list.html, ktory przechowuje id wybranego do edycji modulu
        flash("%s" %modulDoEdycji)
        edit = Moduly.query.filter_by(id = modulDoEdycji).first()  # pobranie instancji Moduly o podanym id
        form = NewModuleForm()                                     # wybranie formy
        # form['name'] = edit.name
        flash(edit.name)
        form.name.data = edit.name                              ## nadanie formie wartosci poczatkowych,
        form.value1.data = edit.value1                          ## czyli tych ktore byly wczesniej w bazie
        form.value2.data = edit.value2                          ## pod danym id
        form.value3.data = edit.value3                          ##
        

        
        return render_template('editmodule.html', edit = edit, form = form) ## edit- do przechowania id modulu
                                                                            ## form- forma do edycji danych

            
            
    return "jakis string"  ## jezeli request method = get
@app.route('/save', methods = ['POST', 'GET'])
def zapis():
    form=NewModuleForm()
    if request.method == 'POST' and form.validate_on_submit():

        edit = Moduly.query.filter_by(id = request.form['address']).first() ## pobranie id do edycji
                                                                            ## z editmodule.html i pobranie
                                                                            ## modulu o danym id

        if str(request.form['name']) != edit.name or\
        int(request.form['value1']) != edit.value1 or\
        int(request.form['value2']) != edit.value2 or\
        int(request.form['value3']) != edit.value3:         ## jezeli ktores z pol formularza ulegnie zmianie

            edit.name = request.form['name']                ## zapisanie nowych wartosci 
            edit.value1 = request.form['value1']            ## z formularza do obiektu,
            edit.value2 = request.form['value2']            ## ktory zostal wczesniej
            edit.value3 = request.form['value3']            ## pobrany
            db.session.commit()                             ## zapisanie do bazy
            return redirect(url_for('list'))
        return redirect(url_for('list'))
    else:
        edit = Moduly.query.filter_by(id = request.form['address']).first()
        return render_template('editmodule.html',form = form, edit = edit)
        
 #########################################################################################
        ###########################HOME#####################################
#########################################################################################
         
    
@app.route('/list', methods = ['POST','GET'])
def list():

    return render_template("list.html", Moduly = Moduly.query.all())
        

#########################################################################################
        ###########################LOGOUT#####################################
#########################################################################################
        
    
@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   flash("Wylogowano","success")
   return redirect(url_for('index'))

#########################################################################################
        ###########################UPLOAD#####################################
#########################################################################################
        

@app.route('/uploader', methods = ['GET', 'POST'])
def uploader_file():

    if request.method == 'POST':
        f = request.files['file']
        if f.filename == '':
            flash('nie wybrales pliku')
            return render_template('upload.html')
                 
        else:
            f.save(secure_filename(f.filename))
            flash('upload przebiegl pomyslnie')
            return render_template('upload.html')
        
    if request.method == 'GET':
        return render_template('upload.html')

############REST
@app.route('/list/<int:address>', methods = ['GET','POST'])
def details(address):
    modul = Moduly.query.filter_by(id = address).first()
    return render_template('main.html', Moduly = Moduly.query.all())

@app.route('/moduly', methods = ['GET'])
def moduly_get():

    moduly = []

    all_modules = Moduly.query.all()
    for modul in all_modules:
        
        item = prepare_for_json3(modul)
        moduly.append(item)
        
        print(modul)
        
    
       
    return jsonify({'moduly': moduly})




@app.route('/moduly', methods = ['POST'])
def moduly_post():
    
    zadanie = request.json
    print(zadanie)
    
    if ('nazwa' in zadanie): 
        urzadzenie = Urzadzenia()
        urzadzenie.name = request.json['nazwa']
        urzadzenie.rejestr = request.json['rejestr']
        urzadzenie.modul_id = request.json['id_modul']
        urzadzenie.sterowanie = request.json['sterowanie']

        
        db.session.add(urzadzenie)
        db.session.commit()
    elif ('r' in zadanie):
        urzadzenie = Urzadzenia.query.filter_by(modul_id = request.json['modul_id'], rejestr = request.json['rejestr']).first()
        urzadzenie.r = request.json['r']
        urzadzenie.g = request.json['g']
        urzadzenie.b = request.json['b']
        
        db.session.commit()
    elif ('stan' in zadanie):
        urzadzenie = Urzadzenia.query.filter_by(modul_id = request.json['modul_id'], rejestr = request.json['rejestr']).first()
        urzadzenie.stan = request.json['stan']
        
        db.session.commit()
    
    elif ('wartosc' in zadanie):
        urzadzenie = Urzadzenia.query.filter_by(modul_id = request.json['modul_id'], rejestr = request.json['rejestr']).first()
        urzadzenie.wartosc = request.json['wartosc']
        
        db.session.commit()
           
        


        
    return Response(status=200)

        # modul = Moduly()
        # modul.name = request.form['name']
        # print modul.name
        # 
        # modul = prepare_for_json(modul)
        
        # db.session.add(modul)
        # db.session.commit()
        
                
 



    
#########################################################################################
#*************************************RUN**********************************************#
#########################################################################################

if __name__ == '__main__':
    db.create_all()
    app.run(debug = True, host='192.168.0.38')
    


