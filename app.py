from MySQLdb import cursors
from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session
import flask
from flask.globals import request
from flask.wrappers import Request
from flask_mysqldb import MySQL
import forms, functions

app = Flask(__name__)

#Mysql connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_PORT'] = 3300
app.config['MYSQL_DB'] = 'aplicaciongym'
mysql=MySQL(app)

# settings session

app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    if 'username' in session:
        return redirect(url_for('home'))
    else:
        return render_template('Index.html')

@app.route('/prueba')
def prueba():
    return render_template('prueba.html')

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('Index'))

@app.route('/register', methods = ['GET', 'POST'])
def Register():
    registerForm= forms.RegisterForm(request.form)
    datos=[];
    if request.method == 'POST' and registerForm.validate():
        datos.append(request.form['usuario'])
        datos.append(request.form['nombre'])
        datos.append(request.form['apellido'])
        datos.append(request.form['mail'])
        datos.append(request.form['contrasenia'])
        datos.append(request.form['sexo'])
        datos.append(request.form['fechaNacimiento'])
        datos.append(request.form['altura'])
        datos.append(request.form['peso'])
        datos.append(request.form['cintura'])
        datos.append(request.form['cuello'])
        datos.append(request.form['caderas'])
        x= (i for i in datos if i.strip()=="")
        lista = list(x) 
        if (len(lista)!=0):
            flash('Complete todos los datos')
        else:
            
            cur = mysql.connection.cursor()
            cur.execute('SELECT usuario,mail FROM usuario WHERE usuario="{0}"'.format(datos[0]))
            coincidenciasUsuario= cur.fetchall()
            cur.execute('SELECT usuario,mail FROM usuario WHERE mail="{0}"'.format(datos[3]))
            coincidenciasMail= cur.fetchall()
            print(datos)
            if (len(coincidenciasMail)==0 and len(coincidenciasUsuario)==0):
                cur.execute('INSERT INTO usuario (usuario, nombre, apellido, mail, contra, sexo, fecha_nacimiento, altura, peso, cintura, cuello, caderas) VALUES ("{0}", "{1}", "{2}", "{3}", "{4}", "{5}", "{6}", {7}, {8}, {9}, {10}, {11})'.format
                (datos[0], datos[1], datos[2], datos[3], datos[4], datos[5], datos[6], datos[7], datos[8], datos[9], datos[10], datos[11]))
                mysql.connection.commit()
                flash('Registrado correctamente')
                return redirect(url_for('Index', success=True))
            else:
                if (len(coincidenciasUsuario)!=0):
                    flash('El usuario ya esta registrado')
                if (len(coincidenciasMail)!=0):
                    flash('El mail ya esta registrado')
                return redirect(url_for('Register'))

    return render_template('register.html', form=registerForm)

@app.route('/register_add', methods = ['POST'])
def register_add():

    return redirect(url_for('Index'))

@app.route('/home', methods=['POST', 'GET'])
def home():
    if request.method== 'POST':
        usuario= request.form['usuario']
        contrasenia= request.form['contrasenia']
        cur= mysql.connection.cursor()
        cur.execute('SELECT u.id_usuario FROM usuario u WHERE (u.usuario= %s or u.mail=%s) AND u.contra=%s', (usuario, usuario, contrasenia))
        datosUsuario= cur.fetchall()
        if (len(datosUsuario)!=0):
            session['username']= datosUsuario[0][0]
        else:    
            flash("Alguno de los datos es incorrecto")
            return redirect(url_for('Index', success=False))

    if 'username' in session and request.method== 'GET':
        id=session['username']
        cur= mysql.connection.cursor()
        cur.execute('SELECT r.id_rutina, e.id_ejercicio, e.nombre, re.peso, re.repeticiones, re.series, re.descanso FROM usuario_rutina ur JOIN rutina r ON r.id_rutina=ur.id_rutina JOIN rutina_ejercicio re ON r.id_rutina=re.id_rutina JOIN ejercicio e ON e.id_ejercicio=re.id_ejercicio WHERE ur.id_usuario={0}'.format(id))
        datosEjercicio= cur.fetchall()
        cur.execute('SELECT distinct(r.id_rutina), r.nombre FROM usuario_rutina ur JOIN rutina r ON r.id_rutina=ur.id_rutina JOIN rutina_ejercicio re ON r.id_rutina=re.id_rutina WHERE ur.id_usuario={0}'.format(id))
        rutinas= cur.fetchall()
        datosRutinas= list()
        for rut in rutinas:
            ejercicioRut=list()
            ejercicioRut.append(rut[0])
            ejercicioRut.append(rut[1])
            for datosRut in datosEjercicio:
                aux= list()
                if rut[0] == datosRut[0]:
                    aux= list([datosRut[1], datosRut[2], datosRut[3], datosRut[4], datosRut[5], datosRut[6]])
                    ejercicioRut.append(aux)
            datosRutinas.append(ejercicioRut)
        rutina= request.args.get('rutina')
        if rutina!=None:
            cur= mysql.connection.cursor()
            cur.execute('SELECT e.id_ejercicio, e.nombre, re.peso, re.repeticiones, re.series, re.descanso FROM usuario_rutina ur JOIN rutina r ON r.id_rutina=ur.id_rutina JOIN rutina_ejercicio re ON r.id_rutina=re.id_rutina JOIN ejercicio e ON e.id_ejercicio=re.id_ejercicio WHERE ur.id_usuario={0} AND r.id_rutina={1}'.format(id, rutina))
            ejercicios= cur.fetchall()
            cur.execute('SELECT r.nombre FROM rutina r WHERE r.id_rutina={0}'.format(rutina))
            rutina= cur.fetchall()
            rutina=rutina[0][0]
            return render_template('home.html', datosRutinas=datosRutinas, rutina=rutina, ejercicios=ejercicios)
        return render_template('home.html', datosRutinas=datosRutinas, rutina=rutina)
    else:
        return redirect(url_for('Index'))

@app.route('/home/user', methods=['POST', 'GET']) 
def perfil():
    if request.method =='POST':
        return render_template('perfil.html')
    if 'username' in session and request.method=='GET':
        cur= mysql.connection.cursor()
        cur.execute('SELECT usuario, nombre, apellido, mail, contra, sexo, fecha_nacimiento, altura, peso, cintura, cuello, caderas FROM usuario WHERE id_usuario={0}'.format(session['username']))
        usuario= cur.fetchall()
        usuario=usuario[0]
        print(usuario)
        imc=functions.IMC(usuario[8], usuario[7])
        return render_template('perfil.html', usuario=usuario, imc=imc, evaluacion=functions.evaluarIMC(imc), pg=functions.porcentajeGrasa(usuario[5], usuario[9], usuario[10], usuario[7], usuario[11]) )
    else:
        return redirect(url_for('Index'))

@app.route('/home/administracion_rutinas')
def adm_rutinas():
    if 'username' in session:
        cur= mysql.connection.cursor()
        cur.execute('SELECT r.nombre FROM rutina r JOIN usuario_rutina ur ON r.id_rutina=ur.id_rutina JOIN usuario u ON u.id_usuario=ur.id_usuario WHERE u.usuario = "{0}"'.format(session['username']))
        rutinas= cur.fetchall()
        #print(rutinas)
        cur= mysql.connection.cursor()
        return render_template('administracion_rutinas.html')
    else:
        return redirect(url_for('Index'))

@app.route('/home/administracion_rutinas/add_rutina', methods= ['POST'])
def add_rutina():
    if request.method =='POST' and 'username' in session:
        
        rutina=request.form['nombre-rutina']
        cur= mysql.connection.cursor()
        cur.execute('SELECT r.nombre FROM rutina r JOIN usuario_rutina ur ON r.id_rutina=ur.id_rutina JOIN usuario u ON u.id_usuario=ur.id_usuario WHERE r.nombre="{0}" and u.usuario = "{1}"'.format(rutina, session['username']))
        rutinaRepetida = cur.fetchall()
        cur= mysql.connection.cursor()
        print(session['username'])
        cur.execute('SELECT id_usuario FROM usuario u WHERE id_usuario= "{0}"'.format(session['username']))
        idUsuario= cur.fetchall()
        print(idUsuario)
        if (len(rutinaRepetida)==0):
            cur= mysql.connection.cursor()
            cur.execute('INSERT into rutina(fecha, nombre, estado) VALUES (CURDATE(), %s , "Creada")', [rutina])
            mysql.connection.commit()
            cur= mysql.connection.cursor()
            cur.execute('SELECT max(id_rutina) FROM rutina')
            idrutina=cur.fetchall()
            idrutina= idrutina[0]
            idrutina= idrutina[0]
            session['idrutina']= idrutina
            cur.execute('INSERT into usuario_rutina(id_usuario, id_rutina, fecha_rutina) VALUES (%s, %s , CURDATE())', [idUsuario[0][0], idrutina])
            mysql.connection.commit()
            cur= mysql.connection.cursor()
            cur.execute('SELECT * FROM ejercicio')
            datosEjer=cur.fetchall()
            return render_template('add_rutina.html', rutina=rutina , ejercicios=datosEjer)
        else:
            flash("Ya tiene una rutina llamada "+ rutina)
            return redirect(url_for('adm_rutinas'))
    else:
        if 'idrutina' in session and 'username' in session:
            cur= mysql.connection.cursor()
            cur.execute('SELECT nombre FROM rutina WHERE id_rutina= {0}'.format(session['idrutina'])) 
            nombrerutina= cur.fetchall()
            nombrerutina=nombrerutina[0]
            nombrerutina=nombrerutina[0]
            cur= mysql.connection.cursor()
            cur.execute('SELECT max(id_rutina) FROM rutina')
            idrutina=cur.fetchall()
            idrutina= idrutina[0]
            idrutina= idrutina[0]
            session['idrutina']= idrutina
            cur= mysql.connection.cursor()
            cur.execute('SELECT * FROM ejercicio')
            datosEjer=cur.fetchall()
            return render_template('add_rutina.html', rutina=nombrerutina , ejercicios=datosEjer)
        if 'username' in session:
            return redirect(url_for('adm_rutinas'))
        else:
            return redirect(url_for('Index'))


@app.route('/home/administracion_rutinas/add_rutina/create_rutina', methods= ['POST'])
def create_rutina():
    if request.method == 'POST':
        cantEjerc= len(request.form.getlist('orden'))
        if cantEjerc>0 and request.form.get('botonSubmit')=="botonSubmit":
            nombreEjer= request.form.getlist('nombre-ejer')
            series= request.form.getlist('series')
            repeticiones= request.form.getlist('repeticiones')
            peso= request.form.getlist('peso')
            descansos= request.form.getlist('descansos')
            idrutina= session['idrutina']
            cur= mysql.connection.cursor()
            cur.execute('SELECT fecha FROM rutina WHERE id_rutina= {0}'.format(idrutina)) 
            fecharutina= cur.fetchall()
            fecharutina=fecharutina[0]
            fecharutina=fecharutina[0]
            for i in range(cantEjerc):
                cur= mysql.connection.cursor()
                cur.execute('SELECT id_ejercicio FROM ejercicio WHERE nombre= %s' , [nombreEjer[i]]) 
                idejercicio= cur.fetchall()
                idejercicio=idejercicio[0]
                idejercicio=idejercicio[0]
                cur= mysql.connection.cursor()
                cur.execute('INSERT into rutina_ejercicio(fecha_rutina, id_rutina, id_ejercicio, descanso, repeticiones, peso, series) VALUES( %s, %s, %s, %s, %s, %s, %s )',
                (fecharutina, idrutina, idejercicio, descansos[i], repeticiones[i], peso[i], series[i]))
                mysql.connection.commit()
            session.pop('idrutina')
            flash('Creada correctamente')
        else:
            idrutina= session['idrutina']
            cur= mysql.connection.cursor()
            cur.execute('SELECT u.id_usuario FROM usuario u WHERE u.id_usuario= "{0}"'.format(session['username']))
            idUsuario= cur.fetchall()
            idUsuario= idUsuario[0]
            idUsuario= idUsuario[0]
            cur.execute('DELETE FROM usuario_rutina WHERE id_rutina = %s and id_usuario= %s' , [idrutina, idUsuario])
            mysql.connection.commit()
            cur.execute('DELETE FROM rutina WHERE id_rutina = %s', [idrutina])
            mysql.connection.commit()
            session.pop('idrutina')
            flash('No se agrego ningun ejercicio')

        return redirect(url_for('adm_rutinas'))
    return redirect(url_for('adm_rutinas'))

@app.route('/home/administracion_rutinas/modify_rutina')
def modify_rutina():
    if 'username' in session:
        cur= mysql.connection.cursor()
        cur.execute('SELECT r.id_rutina, r.nombre FROM rutina r JOIN usuario_rutina ur ON r.id_rutina=ur.id_rutina WHERE ur.id_usuario= %s ', 
        [session['username']])
        rutinas=cur.fetchall()
        cur= mysql.connection.cursor()
        cur.execute('SELECT r.id_rutina, e.id_ejercicio, e.nombre, re.series, re.repeticiones, re.peso, re.descanso FROM rutina r JOIN usuario_rutina ur ON r.id_rutina=ur.id_rutina JOIN rutina_ejercicio re ON r.id_rutina=re.id_rutina JOIN ejercicio e ON re.id_ejercicio=e.id_ejercicio WHERE ur.id_usuario= %s ', 
        [session['username']])
        rutinaEjercicios=cur.fetchall()
        cur= mysql.connection.cursor()
        cur.execute('SELECT * FROM ejercicio')
        datosEjer=cur.fetchall()
        return render_template('modify_rutina.html', rutinas=rutinas , ejercicios=datosEjer, rutinaEjer=rutinaEjercicios)
    else:
        return redirect(url_for('Index'))
        
@app.route('/home/administracion_rutinas/modify_rutina/add_modification', methods= ['POST'])
def add_modification():
    if request.method == 'POST':
        cantEjerc= len(request.form.getlist('orden'))
        if cantEjerc>0 and request.form.get('botonSubmit')=="botonSubmit":
            nombrerutina= request.form['nomb-rut']
            idrutina=request.form['numb-rut']
            nombreEjer= request.form.getlist('nombre-ejer')
            series= request.form.getlist('series')
            repeticiones= request.form.getlist('repeticiones')
            peso= request.form.getlist('peso')
            descansos= request.form.getlist('descansos')
            cur= mysql.connection.cursor()
            cur.execute('UPDATE rutina r SET fecha=CURDATE() WHERE r.id_rutina={0}'.format(idrutina))
            cur.execute('DELETE FROM rutina_ejercicio WHERE id_rutina={0}'.format(idrutina))
            mysql.connection.commit()         
            cur.execute('SELECT r.fecha FROM rutina r WHERE r.id_rutina={0}'.format(idrutina))
            fecharutina= cur.fetchall()
            print(fecharutina)
            fecharutina=fecharutina[0]
            fecharutina=fecharutina[0]
            for i in range(cantEjerc):
                cur.execute('SELECT id_ejercicio FROM ejercicio WHERE nombre= %s' , [nombreEjer[i]]) 
                idejercicio= cur.fetchall()
                idejercicio=idejercicio[0]
                idejercicio=idejercicio[0]
                cur= mysql.connection.cursor()
                cur.execute('INSERT into rutina_ejercicio(fecha_rutina, id_rutina, id_ejercicio, descanso, repeticiones, peso, series) VALUES( %s, %s, %s, %s, %s, %s, %s )',
                (fecharutina, idrutina, idejercicio, descansos[i], repeticiones[i], peso[i], series[i]))
                mysql.connection.commit()
            flash('Modificada correctamente')
        else:
            flash('Tiene que agregar algun ejercicio a la rutina')
        return redirect(url_for('adm_rutinas'))
    return redirect(url_for('adm_rutinas'))

@app.route('/home/administracion_rutinas/delete_rutina')
def delete_rutina():
    if 'username' in session:
        cur= mysql.connection.cursor()
        cur.execute('SELECT r.id_rutina, r.nombre FROM rutina r JOIN usuario_rutina ur ON r.id_rutina=ur.id_rutina WHERE ur.id_usuario= %s ', 
        [session['username']])
        rutinas=cur.fetchall()
        cur= mysql.connection.cursor()
        cur.execute('SELECT r.id_rutina, e.id_ejercicio, e.nombre, re.series, re.repeticiones, re.peso, re.descanso FROM rutina r JOIN usuario_rutina ur ON r.id_rutina=ur.id_rutina JOIN rutina_ejercicio re ON r.id_rutina=re.id_rutina JOIN ejercicio e ON re.id_ejercicio=e.id_ejercicio WHERE ur.id_usuario= %s ', 
        [session['username']])
        rutinaEjercicios=cur.fetchall()
        cur= mysql.connection.cursor()
        print(rutinaEjercicios)
        print(rutinas)
        print("ingreso al template")
        return render_template('delete_rutina.html', rutinas=rutinas , rutinaEjer=rutinaEjercicios)
    else:
        return redirect(url_for('Index'))

@app.route('/home/administracion_rutinas/delete_rutina/confirm_delete', methods= ['POST'])
def confirm_delete():
    if request.method=='POST' and 'username' in session:
        if request.form.get('botonSubmit')=="botonSubmit":
            cantEjerc= len(request.form.getlist('orden'))
            idrutina= request.form['numb-rut']
            usuario= session['username']
            cur= mysql.connection.cursor()
            cur.execute('DELETE FROM rutina_ejercicio WHERE id_rutina = {0}'.format(idrutina))
            cur.execute('DELETE FROM usuario_rutina WHERE id_rutina ={0} and id_usuario={1}'.format(idrutina, usuario))
            cur.execute('DELETE FROM rutina WHERE id_rutina = {0}'.format(idrutina))
            mysql.connection.commit()
            flash('eliminada correctamente')
        else:
            flash('No se hicieron cambios')
        return redirect(url_for('adm_rutinas'))
    else:
        return redirect(url_for('Index'))


@app.route('/ejercicios')
def ejercicios():
    return render_template('CargarEjercicios.html')

@app.route('/ejercicios_add', methods= ['POST'])
def ejercicios_add():
    if request.method == 'POST':
        nombre=request.form['nombre-ejercicio']
        descrip=request.form['descripcion']
        cur= mysql.connection.cursor()
        cur.execute('INSERT INTO ejercicio(nombre, descripcion) VALUES (%s, %s)',
        (nombre, descrip))
        mysql.connection.commit()
        flash('Se registro el ejercicio')
    return redirect(url_for('ejercicios'))

if __name__== '__main__':
    app.run(port = 3000, debug=True)