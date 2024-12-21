from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuración de la aplicación y la base de datos
app.secret_key = 'supersecretkey'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'movie_library'
app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)

# Ruta principal
@app.route('/')
def home():
    return render_template('home.html')

# Gestión de películas
@app.route('/movies')
def list_movies():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM movies")
    movies = cur.fetchall()
    cur.close()
    return render_template('movies/list.html', movies=movies)

@app.route('/movies/add', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        title = request.form.get('title')
        director = request.form.get('director')
        genre = request.form.get('genre')
        year = request.form.get('year')

        if not all([title, director, genre, year]):
            flash('Todos los campos son obligatorios.', 'error')
            return redirect(url_for('add_movie'))

        try:
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO movies (title, director, genre, year) VALUES (%s, %s, %s, %s)",
                (title, director, genre, year),
            )
            mysql.connection.commit()
            flash('Película agregada exitosamente.', 'success')
        except Exception as e:
            flash(f'Ocurrió un error: {e}', 'error')
        finally:
            cur.close()

        return redirect(url_for('list_movies'))

    return render_template('movies/add.html')

@app.route('/movies/edit/<int:id>', methods=['GET', 'POST'])
def edit_movie(id):
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        title = request.form.get('title')
        director = request.form.get('director')
        genre = request.form.get('genre')
        year = request.form.get('year')

        if not all([title, director, genre, year]):
            flash('Todos los campos son obligatorios.', 'error')
            return redirect(url_for('edit_movie', id=id))

        try:
            cur.execute(
                """
                UPDATE movies
                SET title = %s, director = %s, genre = %s, year = %s
                WHERE id = %s
                """,
                (title, director, genre, year, id),
            )
            mysql.connection.commit()
            flash('Película actualizada exitosamente.', 'success')
        except Exception as e:
            flash(f'Ocurrió un error: {e}', 'error')
        finally:
            cur.close()

        return redirect(url_for('list_movies'))

    cur.execute("SELECT * FROM movies WHERE id = %s", (id,))
    movie = cur.fetchone()
    cur.close()
    return render_template('movies/edit.html', movie=movie)

@app.route('/movies/delete/<int:id>', methods=['POST'])
def delete_movie(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM movies WHERE id = %s", (id,))
        mysql.connection.commit()
        flash('Película eliminada exitosamente.', 'success')
    except Exception as e:
        flash(f'Ocurrió un error: {e}', 'error')
    finally:
        cur.close()

    return redirect(url_for('list_movies'))

# Gestión de miembros
@app.route('/members')
def list_members():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM members")
    members = cur.fetchall()
    cur.close()
    return render_template('members/list.html', members=members)

@app.route('/members/add', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')

        if not all([name, email, phone]):
            flash('Todos los campos son obligatorios.', 'error')
            return redirect(url_for('add_member'))

        try:
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO members (name, email, phone) VALUES (%s, %s, %s)",
                (name, email, phone),
            )
            mysql.connection.commit()
            flash('Miembro agregado exitosamente.', 'success')
        except Exception as e:
            flash(f'Ocurrió un error: {e}', 'error')
        finally:
            cur.close()

        return redirect(url_for('list_members'))

    return render_template('members/add.html')

@app.route('/members/edit/<int:id>', methods=['GET', 'POST'])
def edit_member(id):
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')

        if not all([name, email, phone]):
            flash('Todos los campos son obligatorios.', 'error')
            return redirect(url_for('edit_member', id=id))

        try:
            cur.execute(
                """
                UPDATE members
                SET name = %s, email = %s, phone = %s
                WHERE id = %s
                """,
                (name, email, phone, id),
            )
            mysql.connection.commit()
            flash('Miembro actualizado exitosamente.', 'success')
        except Exception as e:
            flash(f'Ocurrió un error: {e}', 'error')
        finally:
            cur.close()

        return redirect(url_for('list_members'))

    cur.execute("SELECT * FROM members WHERE id = %s", (id,))
    member = cur.fetchone()
    cur.close()
    return render_template('members/edit.html', member=member)

@app.route('/members/delete/<int:id>', methods=['POST'])
def delete_member(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM members WHERE id = %s", (id,))
        mysql.connection.commit()
        flash('Miembro eliminado exitosamente.', 'success')
    except Exception as e:
        flash(f'Ocurrió un error: {e}', 'error')
    finally:
        cur.close()

    return redirect(url_for('list_members'))

@app.route('/borrowings')
def list_borrowings():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM borrowing")
    borrowings = cur.fetchall()
    cur.close()
    return render_template('borrowings/list.html', borrowings=borrowings)

@app.route('/borrowings/add', methods=['GET', 'POST'])
def add_borrowing():
    if request.method == 'POST':
        movie_id = request.form.get('movie_id')
        member_id = request.form.get('member_id')
        borrow_date = request.form.get('borrow_date')
        return_date = request.form.get('return_date')

        if not all([movie_id, member_id, borrow_date]):
            flash('Todos los campos son obligatorios.', 'error')
            return redirect(url_for('add_borrowing'))

        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO borrowing (movie_id, member_id, borrow_date, return_date)
                VALUES (%s, %s, %s, %s)
            """, (movie_id, member_id, borrow_date, return_date))
            mysql.connection.commit()
            flash('Préstamo registrado exitosamente.', 'success')
        except Exception as e:
            flash(f'Ocurrió un error: {e}', 'error')
        finally:
            cur.close()

        return redirect(url_for('list_borrowings'))

    # Obtener todas las películas y miembros para los formularios
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM movies")
    movies = cur.fetchall()
    cur.execute("SELECT * FROM members")
    members = cur.fetchall()
    cur.close()

    return render_template('borrowings/add.html', movies=movies, members=members)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        if not all([name, email, message]):
            flash('Todos los campos son obligatorios.', 'error')
            return redirect(url_for('contact'))

        # Aquí podrías agregar la lógica para enviar el mensaje (por ejemplo, a un correo electrónico o base de datos).
        flash('¡Gracias por contactarnos! Nos comunicaremos contigo pronto.', 'success')
        return redirect(url_for('home'))

    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
