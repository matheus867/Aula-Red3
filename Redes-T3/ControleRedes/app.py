from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Configuração do MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    port=7306,  # Ajuste a porta conforme necessário
    database="rack_management"
)

@app.route('/')
def index():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM devices")
    devices = cursor.fetchall()
    return render_template('index.html', devices=devices)

@app.route('/add', methods=['GET', 'POST'])
def add_device():
    if request.method == 'POST':
        device = {
            'device_name': request.form['device_name'],
            'device_type': request.form['device_type'],
            'ip_address': request.form['ip_address'],
            'vlan': request.form['vlan'],
            'configuration': request.form['configuration'],
            'notes': request.form['notes']
        }
        cursor = db.cursor()
        cursor.execute("INSERT INTO devices (device_name, device_type, ip_address, vlan, configuration, notes) VALUES (%s, %s, %s, %s, %s, %s)", 
                        (device['device_name'], device['device_type'], device['ip_address'], device['vlan'], device['configuration'], device['notes']))
        db.commit()
        return redirect(url_for('index'))
    return render_template('add_device.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_device(id):
    cursor = db.cursor(dictionary=True)
    if request.method == 'POST':
        device = {
            'device_name': request.form['device_name'],
            'device_type': request.form['device_type'],
            'ip_address': request.form['ip_address'],
            'vlan': request.form['vlan'],
            'configuration': request.form['configuration'],
            'notes': request.form['notes']
        }
        cursor.execute("UPDATE devices SET device_name = %s, device_type = %s, ip_address = %s, vlan = %s, configuration = %s, notes = %s WHERE id = %s",
                        (device['device_name'], device['device_type'], device['ip_address'], device['vlan'], device['configuration'], device['notes'], id))
        db.commit()
        return redirect(url_for('index'))
    cursor.execute("SELECT * FROM devices WHERE id = %s", (id,))
    device = cursor.fetchone()
    return render_template('edit_device.html', device=device)

@app.route('/delete/<int:id>')
def delete_device(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM devices WHERE id = %s", (id,))
    db.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=5000, debug=True)
