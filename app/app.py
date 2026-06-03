from datetime import datetime
from flask import Flask, render_template, session, redirect, url_for, request, flash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature

app = Flask(__name__)
app.secret_key = 'your_super_secret_session_key'

# Serializer for generating secure, time-sensitive tokens
def get_serializer():
    return URLSafeTimedSerializer(app.secret_key)

@app.context_processor
def inject_global_variables():
    return {'current_year': datetime.now().year}

@app.route('/')
def home():
    return render_template('index.html', active_page='home')

@app.route('/features')
def features():
    return render_template('features.html', active_page='features')

@app.route('/about')
def about():
    return render_template('about.html', active_page='about')

@app.route('/contact')
def contact():
    return render_template('contact.html', active_page='contact')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html', active_page='privacy')

@app.route('/terms')
def terms():
    return render_template('terms.html', active_page='terms')

# New Login Route Handler
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Simulate successful validation logic
        session['user_id'] = 123
        session['username'] = request.form.get('email').split('@')[0].capitalize()
        return redirect(url_for('dashboard'))
    return render_template('login.html', active_page='login')
    

# New Registration Route Handler
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_email = request.form.get('email')
        user_name = request.form.get('name')
        
        # 1. Generate secure token (expires in 3600 seconds / 1 hour)
        serializer = get_serializer()
        token = serializer.dumps(user_email, salt='email-activation-salt')
        
        # 2. Build the structural activation link
        activation_url = url_for('activate_account', token=token, _external=True)
        
        # 3. Simulate email dispatch safely to terminal logs
        print("\n" + "="*60)
        print(f"MOCK EMAIL SENT TO: {user_email}")
        print(f"Hello {user_name},\nClick the link below to activate your account:")
        print(activation_url)
        print("="*60 + "\n")
        
        # Cache email in session strictly to render the confirmation screen details
        session['pending_email'] = user_email
        return redirect(url_for('verify_email_notice'))
        
    return render_template('register.html', active_page='register')


# Notice screen telling users to check inbox
@app.route('/verify-email-notice')
def verify_email_notice():
    email = session.get('pending_email', 'your email address')
    return render_template('verify_notice.html', email=email)

# The endpoint the user clicks inside their email body
@app.route('/activate/<token>')
def activate_account(token):
    serializer = get_serializer()
    try:
        # Check token validity against a maximum age of 1 hour (3600 seconds)
        email = serializer.loads(token, salt='email-activation-salt', max_age=3600)
        
        # Success: Clear pending flags and log user session into workspace
        session.pop('pending_email', None)
        session['user_id'] = 999  
        session['username'] = email.split('@')[0].capitalize()
        
        return render_template('welcome.html', success=True)
        
    except SignatureExpired:
        return render_template('welcome.html', success=False, error="The activation link has expired. Please register again.")
    except (BadTimeSignature, Exception):
        return render_template('welcome.html', success=False, error="Invalid token authentication signature.")


# New Post-Registration Success Route
@app.route('/welcome')
def welcome():
    # Security check: Ensure only newly registered/logged-in users can see this
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('welcome.html', active_page='welcome', success=True)

# New Secure Dashboard View Router
@app.route('/dashboard')
def dashboard():
    # Security Guard: Block unauthorized requests
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', active_page='dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
