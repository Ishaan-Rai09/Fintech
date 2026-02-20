from flask import Flask, render_template, request, redirect, url_for, flash, session, g
import mysql.connector
from db import get_db, init_app
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')

# Mail Configuration
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

mail = Mail(app)
init_app(app)

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('landing.html')

@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        cursor = db.cursor()
        error = None

        if not username:
            error = 'Username is required.'
        elif not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                cursor.execute(
                    "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                    (username, email, generate_password_hash(password)),
                )
                db.commit()
            except mysql.connector.Error as e:
                error = f"User {username} is already registered."
            else:
                flash("Registration successful. Please login.")
                return redirect(url_for('login'))

        flash(error, 'danger')

    return render_template('register.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        cursor = db.cursor(dictionary=True)
        error = None
        
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user is None:
            error = 'Incorrect email.'
        elif not check_password_hash(user['password_hash'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('dashboard'))

        flash(error, 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard', methods=('GET', 'POST'))
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    # Get Balance
    cursor.execute("SELECT balance FROM users WHERE id = %s", (session['user_id'],))
    user = cursor.fetchone()
    balance = user['balance']
    
    if request.method == 'POST':
        receiver_username = request.form['receiver']
        amount = float(request.form['amount'])
        
        error = None
        if amount <= 0:
            error = "Amount must be positive."
        elif amount > balance:
            error = "Insufficient balance."
        
        if error is None:
            try:
                # Start Transaction
                # Check receiver
                cursor.execute("SELECT id, email FROM users WHERE username = %s", (receiver_username,))
                receiver = cursor.fetchone()
                
                if receiver is None:
                    error = "Receiver not found."
                elif receiver['id'] == session['user_id']:
                    error = "Cannot send money to yourself."
                else:
                    # Deduct from sender
                    cursor.execute("UPDATE users SET balance = balance - %s WHERE id = %s", (amount, session['user_id']))
                    # Add to receiver
                    cursor.execute("UPDATE users SET balance = balance + %s WHERE id = %s", (amount, receiver['id']))
                    # Record transaction
                    cursor.execute(
                        "INSERT INTO transactions (sender_id, receiver_id, amount) VALUES (%s, %s, %s)",
                        (session['user_id'], receiver['id'], amount)
                    )
                    
                    db.commit()
                    
                    # Send Email
                    try:
                        send_email(receiver['email'], "Money Received", f"You received ${amount} from {session['username']}")
                        
                        # Get sender email
                        cursor.execute("SELECT email FROM users WHERE id = %s", (session['user_id'],))
                        sender = cursor.fetchone()
                        send_email(sender['email'], "Money Sent", f"You sent ${amount} to {receiver_username}")
                    except Exception as e:
                        flash(f"Transaction successful but email failed: {e}", 'warning')
                    else:
                        flash(f"Successfully sent ${amount} to {receiver_username}", 'success')
                        
                    return redirect(url_for('dashboard'))
            except mysql.connector.Error as e:
                db.rollback()
                error = f"Transaction failed: {e}"
        
        if error:
            flash(error, 'danger')

    return render_template('dashboard.html', balance=balance)

@app.route('/transactions')
def transactions_list():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT t.id, t.amount, t.timestamp, u_sender.username as sender, u_receiver.username as receiver
        FROM transactions t
        JOIN users u_sender ON t.sender_id = u_sender.id
        JOIN users u_receiver ON t.receiver_id = u_receiver.id
        WHERE t.sender_id = %s OR t.receiver_id = %s
        ORDER BY t.timestamp DESC
    """, (session['user_id'], session['user_id']))
    
    transactions = cursor.fetchall()
    return render_template('transactions.html', transactions=transactions)

def send_email(to, subject, body):
    msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[to])
    msg.body = body
    mail.send(msg)

if __name__ == '__main__':
    app.run(debug=True)
