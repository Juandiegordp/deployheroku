from MySQLdb import cursors
from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session
import flask
from flask.globals import request
from flask.wrappers import Request
from flask_mysqldb import MySQL

app = Flask(__name__)

#Mysql connection
app.config['MYSQL_HOST'] = 'ec2-3-221-100-217.compute-1.amazonaws.com'
app.config['MYSQL_USER'] = 'zrsirfmyuqtoov'
app.config['MYSQL_PASSWORD'] = '93fb8780150b7132c4d8ca2bd2be418e40d126941b3e91f1750de2445e02a754'
app.config['MYSQL_PORT'] = 5432
app.config['MYSQL_DB'] = 'da7t12d2030eu3'
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

@app.route('/register')
def Register():
    return render_template('register.html')

@app.route('/register_add', methods = ['POST'])
def register_add():
    datos=[];
    if request.method == 'POST':
        datos.append(request.form['usuario'])
        datos.append(request.form['nombre'])
        datos.append(request.form['apellido'])
        datos.append(request.form['mail'])
        datos.append(request.form['password'])
        x= (i for i in datos if i.strip()=="")
        lista = list(x)       
        if (len(lista)!=0):
            flash('Complete todos los datos')
        else:
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO usuario (usuario, nombre, apellido, mail, contra) VALUES (%s, %s, %s, %s, %s)',
            (datos[0], datos[1], datos[2], datos[3], datos[4]))
            mysql.connection.commit()
            flash('Registrado correctamente')
    return redirect(url_for('Register'))

@app.route('/home', methods=['POST', 'GET'])
def home():
    if request.method== 'POST':
        usuario= request.form['usuario']
        contrasenia= request.form['contrasenia']
        cur= mysql.connection.cursor()
        cur.execute('SELECT u.usuario FROM usuario u WHERE (u.usuario= %s or u.mail=%s) AND u.contra=%s', (usuario, usuario, contrasenia))
        datosUsuario= cur.fetchall()
        if (len(datosUsuario)!=0):

            session['username']= datosUsuario[0]
            return render_template('home.html')
        return redirect(url_for('Index'))
    else:
        if 'username' in session:
            return render_template('home.html')
        else:
            return redirect(url_for('Index'))

@app.route('/home/user')
def perfil():
    if 'username' in session:
        return render_template('perfil.html')
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
        cur.execute('SELECT u.id_usuario FROM usuario u WHERE u.usuario= "{0}"'.format(session['username']))
        idUsuario= cur.fetchall()
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
            cur.execute('INSERT into usuario_rutina(id_usuario, id_rutina, fecha_rutina) VALUES (%s, %s , CURDATE())', [idUsuario[0], idrutina])
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
            cur.execute('SELECT u.id_usuario FROM usuario u WHERE u.usuario= "{0}"'.format(session['username']))
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
        cur.execute('SELECT r.id_rutina, r.nombre FROM rutina r JOIN usuario_rutina ur ON r.id_rutina=ur.id_rutina JOIN usuario u ON u.id_usuario=ur.id_usuario WHERE u.usuario= %s ', 
        [session['username']])
        rutinas=cur.fetchall()
        cur= mysql.connection.cursor()
        cur.execute('SELECT r.id_rutina, e.id_ejercicio, e.nombre, re.series, re.repeticiones, re.peso, re.descanso FROM rutina r JOIN usuario_rutina ur ON r.id_rutina=ur.id_rutina JOIN usuario u ON u.id_usuario=ur.id_usuario JOIN rutina_ejercicio re ON r.id_rutina=re.id_rutina JOIN ejercicio e ON re.id_ejercicio=e.id_ejercicio WHERE u.usuario= %s ', 
        [session['username']])
        rutinaEjercicios=cur.fetchall()
        cur= mysql.connection.cursor()
        cur.execute('SELECT max(id_rutina) FROM rutina')
        idrutina=cur.fetchall()
        idrutina= idrutina[0]
        idrutina= idrutina[0]
        session['idrutina']= idrutina
        cur= mysql.connection.cursor()
        cur.execute('SELECT * FROM ejercicio')
        datosEjer=cur.fetchall()
        print(rutinaEjercicios)
        #print(rutinas)
        print("ingreso al template")
        return render_template('modify_rutina.html', rutinas=rutinas , ejercicios=datosEjer, rutinaEjer=rutinaEjercicios)
    else:
        return redirect(url_for('Index'))
        
@app.route('/home/administracion_rutinas/modify_rutina/add_modification', methods= ['POST'])
def add_modification():
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
            cur.execute('SELECT u.id_usuario FROM usuario u WHERE u.usuario= "{0}"'.format(session['username']))
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