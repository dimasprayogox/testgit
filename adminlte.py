from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.secret_key = 'wow'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pos'
app.config['MYSQL_HOST'] = 'localhost'

mysql = MySQL(app) 

@app.route("/")
def index():
    if 'loggedin' in session and session['level'] == 'admin':
        return render_template('index.html')
    flash('Harap Login dulu','danger')
    return redirect(url_for('login'))

#registrasi
@app.route('/registrasi', methods=('GET', 'POST'))
def registrasi():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        level = request.form['level']

        # cek username atau email
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username=%s OR email=%s', (username, email))
        existing_user = cursor.fetchone()

        if existing_user is None:
            cursor.execute('INSERT INTO users (username, email, password, level) VALUES (%s, %s, %s, %s)', 
                           (username, email, generate_password_hash(password), level))
            mysql.connection.commit()
            flash('Registrasi Berhasil', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username atau email sudah ada', 'danger')

    return render_template('registrasi.html')

#login
@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Cek data username
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE email=%s', (email,))
        akun = cursor.fetchone()
        
        if akun is None:
            flash('Login Gagal, Cek Username Anda', 'danger')
        elif not check_password_hash(akun[3], password):  # Asumsi kolom password berada di indeks ke-3
            flash('Login gagal, Cek Password Anda', 'danger')
        else:
            session['loggedin'] = True
            session['username'] = akun[1]
            session['level'] = akun[4]  # Asumsi kolom level berada di indeks ke-4
            
            if akun[4] == 'admin':
                return redirect(url_for('index'))
            elif akun[4] == 'pembeli':
                return redirect(url_for('pembeli_index'))
    return render_template('login.html')


@app.route('/pembeli_index')
def pembeli_index():
    if 'loggedin' in session and session['level'] == 'pembeli':
        return render_template('uhuy.html')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    session.pop('level', None)
    return redirect(url_for('login'))



@app.route("/masterbarang")
def masterbarang():
    cursor = mysql.connection.cursor()
    sql = ('select * from masterbarang')
    cursor.execute(sql)
    barang = cursor.fetchall()
    cursor.close()
    
    return render_template("masterbarang.html", menu = 'master', submenu = 'barang', data = barang)

@app.route("/formmasterbarang")
def formmasterbarang():
    return render_template("formmasterbarang.html", menu = 'master', submenu = 'barang')

@app.route("/simpanformmasterbarang", methods = ["GET", "POST"])
def simpanformmasterbarang():
    if request.method == "POST":
        nama = request.form['nama']
        harga = request.form['harga']
        satuan = request.form['satuan']
        
        sql = 'insert into masterbarang (nama,harga,satuan) values (%s, %s, %s)'
        data = (nama,harga,satuan)
        
        cursor = mysql.connection.cursor()
        cursor.execute(sql, data)
        mysql.connection.commit()
        cursor.close()
        
        return redirect(url_for('masterbarang'))
    else :
        return render_template("formmasterbarang")
    

@app.route("/mastersupplier")
def mastersupplier():
    cursor = mysql.connection.cursor()
    sql = ('select * from mastersupplier')
    cursor.execute(sql)
    supplier = cursor.fetchall()
    cursor.close()
    return render_template("mastersupplier.html", menu = 'master', submenu = 'supplier', data = supplier)

@app.route("/formmastersupplier")
def formmastersupplier():
    return render_template("formmastersupplier.html", menu = 'master', submenu = 'barang')

@app.route("/simpanformmastersupplier", methods = ["GET", "POST"])
def simpanformmastersupplier():
    if request.method == "POST":
        nama = request.form['nama']
        alamat = request.form['alamat']
        kota = request.form['kota']
        
        sql = 'insert into mastersupplier (nama,alamat,kota) values (%s, %s, %s)'
        data = (nama,alamat,kota)
        
        cursor = mysql.connection.cursor()
        cursor.execute(sql, data)
        mysql.connection.commit()
        cursor.close()
        
        return redirect(url_for('mastersupplier'))
    else :
        return render_template("formmastersupplier")
    
    

@app.route("/masterpelanggan")
def masterpelanggan():
    cursor = mysql.connection.cursor()
    sql = ('select * from masterpelanggan')
    cursor.execute(sql)
    pelanggan = cursor.fetchall()
    cursor.close()
    return render_template("masterpelanggan.html", menu = 'master', submenu = 'pelanggan', data = pelanggan)

@app.route("/formmasterpelanggan")
def formmasterpelanggan():
    return render_template("formmasterpelanggan.html", menu = 'master', submenu = 'barang')

@app.route("/simpanformmasterpelanggan", methods = ["GET", "POST"])
def simpanformmasterpelanggan():
    if request.method == "POST":
        nama = request.form['nama']
        alamat = request.form['alamat']
        kota = request.form['kota']
        
        sql = 'insert into masterpelanggan (nama,alamat,kota) values (%s, %s, %s)'
        data = (nama,alamat,kota)
        
        cursor = mysql.connection.cursor()
        cursor.execute(sql, data)
        mysql.connection.commit()
        cursor.close()
        
        return redirect(url_for('masterpelanggan'))
    else :
        return render_template("formmasterpelanggan")
    
    
@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route("/formpembelian")
def formpembelian():
    return render_template("formpembelian.html", menu = 'pembelian', submenu = 'formpembelian')

@app.route("/datapembelian")
def datapembelian():
    return render_template("datapembelian.html", menu = 'pembelian', submenu = 'datapembelian')

@app.route("/formpenjualan")
def formpenjualan():
    return render_template("formpenjualan.html", menu = 'penjualan', submenu = 'formpenjualan')

@app.route("/datapenjualan")
def datapenjualan():
    return render_template("datapenjualan.html", menu = 'penjualan', submenu = 'datapenjualan')



if __name__=='__main__':
    app.run(debug=True)