from flask_mysqldb import MySQL
from MySQLdb import cursors

def registrarUsuario(datos, mysql):
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO usuario (usuario, nombre, apellido, mail, contra, sexo, fecha_nacimiento, altura, peso, cintura, cuello, caderas) VALUES ("{0}", "{1}", "{2}", "{3}", "{4}", "{5}", "{6}", {7}, {8}, {9}, {10}, {11})'.format
    (datos[0], datos[1], datos[2], datos[3], datos[4], datos[5], datos[6], datos[7], datos[8], datos[9], datos[10], datos[11]))
    mysql.connection.commit()

def coincidenciasMail(datos, mysql):
    cur = mysql.connection.cursor()
    cur.execute('SELECT usuario,mail FROM usuario WHERE mail="{0}"'.format(datos[3]))
    coincidenciasMail= cur.fetchall()
    return coincidenciasMail

def coincidenciasUsuario(datos, mysql):
    cur = mysql.connection.cursor()
    cur.execute('SELECT usuario,mail FROM usuario WHERE usuario="{0}"'.format(datos[0]))
    coincidenciasUsuario= cur.fetchall()
    return coincidenciasUsuario
    