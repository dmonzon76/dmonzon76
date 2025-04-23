from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import os
import logging
logging.basicConfig(level=logging.DEBUG)


app = Flask(__name__, static_folder='static' )

# MYSQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'biblos12'
mysql = MySQL(app)

# Settings
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret_key')
 

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/Books/books', methods=['GET', 'POST'])
def Books():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM titles')
        data = cur.fetchall()
        print(data)  # For debugging purposes
        return render_template('Books/books.html', titles=data)
    except Exception as e:
        return f"Error: {str(e)}"


@app.route('/Books/addbooks', methods=['GET','POST'])
def addBooks():
    if request.method == 'POST':
        title = request.form['title']
        location = request.form['location']
        isbn = request.form['isbn']
        cur = mysql.connection.cursor()
        cur.execute(
            'INSERT INTO titles (title, location, isbn) VALUES (%s, %s, %s)', (title, location, isbn))
        mysql.connection.commit()
        cur.close()
        return redirect (url_for('Books'))
    else:
        return render_template('Books/addbooks.html')


@app.route('/Books/edit_book/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            'SELECT * FROM titles title, location, isbn WHERE id=%s', (id,))
        data = cur.fetchone()
        mysql.connection.commit()
        return render_template('Books/edit_book.html', title=data)
    except Exception as e:
        cur.close()
        return f"Error: {str(e)}"

def get_title(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM titles WHERE id=%s', (id, ))
    data = cur.fetchone()
    return data






@app.route('/delete_book/<id>', methods=['GET', 'POST'])
def delete_book(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM titles WHERE id=%s', (id,))
        mysql.connection.commit()

        cur.execute('SELECT * FROM titles')
        data = cur.fetchall()
        print(data)  # For debugging purposes

        return render_template('Books/books.html', titles=data)
    except Exception as e:
        cur.close()
        return f"Error: {str(e)}"


# Authors

@app.route('/Authors/authors', methods=['GET', 'POST'])
def authors():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM authors')
        data = cur.fetchall()
        print(data)  # For debugging purposes
        return render_template('Authors/authors.html', authors=data)
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/Authors/edit_author/<int:id>', methods=['GET', 'POST'])
def edit_author(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            'SELECT last_name, names, nationality FROM authors WHERE id=%s', (id,))
        data = cur.fetchone()
        mysql.connection.commit()
        return render_template('Authors/edit_author.html', author=data)
    except Exception as e:
        cur.close()
        return f"Error: {str(e)}"  

@app.route('/update<int:id>', methods=['GET','POST'])
def update_author(id):
    if request.method == 'POST':      
        last_name = request.form['last_name']
        names = request.form['names']
        nationality = request.form['nationality']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE authors
        SET last_name = %s,
            names = %s,
            nationality = %s
        WHERE id = %s    
        """, (last_name, names, nationality, id))
        mysql.connection.commit()
        cur.execute('SELECT last_name, names, nationality FROM authors WHERE id=%s', (id,)) 
        print("Updated Data: {updated_data}")
        cur.close()
    return redirect(url_for("Authors/authors"))    

@app.route('/delete_author/<id>', methods=['GET', 'POST'])
def delete_author(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM authors WHERE id=%s', (id,))
        mysql.connection.commit()

        cur.execute('SELECT * FROM authors')
        data = cur.fetchall()
        print(data)  # For debugging purposes

        return render_template('Authors/authors.html', authors=data)
    except Exception as e:
        cur.close()

        
        
        return f"Error: {str(e)}"
    

    
@app.route('/Authors/addauthor', methods=['GET','POST'])
def addauthor():
    if request.method == 'POST':
        last_name = request.form['last_name']
        names = request.form['names']
        nationality = request.form['nationality']
        cur = mysql.connection.cursor()
        cur.execute(
            'INSERT INTO authors (last_name, names, nationality) VALUES (%s, %s, %s)', (last_name, names, nationality))
        mysql.connection.commit()
        return redirect (url_for('authors'))
    else:
        return render_template('Authors/addauthor.html')
    
#@app.route('/update<int:id>', methods=['GET','POST'])
def update_author(id):
    if request.method == 'POST':      
        last_name = request.form['last_name']
        names = request.form['names']
        nationality = request.form['nationality']
        cur = mysql.connection.cursor()
        
        # Actualización de datos en la tabla "authors"
        cur.execute("""
        UPDATE authors
        SET last_name = %s,
            names = %s,
            nationality = %s
        WHERE id = %s    
        """, (last_name, names, nationality, id))
        mysql.connection.commit()
        
        # Puedes agregar aquí un SELECT si deseas obtener los datos actualizados
        cur.execute('SELECT * FROM authors last_name, names, nationality  WHERE id=%s', (id,))
        updated_data = cur.fetchone()  # Recupera los datos actualizados
        print("Updated Data: {updated_data}")
        
        cur.close()
    return redirect(url_for("Authors/authors"))


if __name__ == '__main__':
    app.run(port=5000, debug=True)






























































