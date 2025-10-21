from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

# --- App Configuration ---
app = Flask(__name__)
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'your-secret-key'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# --- General Routes ---
@app.route('/')
def index():
    """Renders the main landing page."""
    return render_template('index.html')


# --- User/Consumer Routes ---
@app.route('/login/user', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        return redirect(url_for('consumer_dashboard'))
    return render_template('login_user.html')

@app.route('/register/user', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        return redirect(url_for('consumer_dashboard'))
    return render_template('register_user.html')

@app.route('/dashboard/consumer')
def consumer_dashboard():
    return render_template('consumer_dashboard.html')

@app.route('/log_purchase')
def log_purchase():
    return render_template('log_purchase.html')

@app.route('/discover_vendors')
def discover_vendors():
    return render_template('discover_vendors.html')

@app.route('/redeem')
def redeem():
    return render_template('redeem.html')

@app.route('/ecotips')
def ecotips():
    return render_template('ecotips.html')

@app.route('/refer_earn')
def refer_earn():
    return render_template('refer_earn.html')

@app.route('/eco_advisor')
def eco_advisor():
    return render_template('eco_advisor.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/logout')
def logout():
    return redirect(url_for('index'))

@app.route('/scan_pay')
def scan_pay():
    return render_template('scan_pay.html')


# --- Vendor/Business Routes ---
@app.route('/login/vendor', methods=['GET', 'POST'])
def login_vendor():
    if request.method == 'POST':
        return redirect(url_for('vendor_dashboard'))
    return render_template('login_vendor.html')

@app.route('/vendor/dashboard')
def vendor_dashboard():
    return render_template('vendor_dashboard.html')

# THIS IS THE SINGLE, CORRECT FUNCTION FOR BUSINESS REGISTRATION
@app.route('/register/business', methods=['GET', 'POST'])
def register_business():
    if request.method == 'POST':
        business_name = request.form.get('businessName')
        cert_file = request.files.get('greenCert')
        if cert_file and cert_file.filename != '':
            filename = secure_filename(cert_file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            cert_file.save(save_path)
            print(f"Registration for '{business_name}' successful. Certificate saved.")
        return redirect(url_for('login_vendor'))
    return render_template('register_business.html')

# Add these new routes with the other VENDOR routes in app.py

@app.route('/vendor/generate_bill')
def vendor_generate_bill():
    """Renders the page for generating a new bill."""
    return render_template('vendor_generate_bill.html')

@app.route('/vendor/scan_pay')
def vendor_scan_pay():
    """Renders the vendor's scan & pay interface."""
    # We can reuse the user's scanner page as the UI is identical
    return render_template('scan_pay.html')

# Add this new route with the other vendor routes in app.py

@app.route('/vendor/manage_profile')
def vendor_manage_profile():
    """Renders the vendor's profile management page."""
    return render_template('vendor_manage_profile.html')

# Add this new route with the other vendor routes in app.py

@app.route('/vendor/manage_offers')
def vendor_manage_offers():
    """Renders the vendor's offer management page."""
    return render_template('vendor_manage_offers.html')

# Add this new route with the other vendor routes in app.py

@app.route('/vendor/customer_insights')
def vendor_customer_insights():
    """Renders the vendor's customer insights page."""
    return render_template('vendor_customer_insights.html')

# Add this new route with the other vendor routes in app.py

@app.route('/vendor/transaction_history')
def vendor_transaction_history():
    """Renders the vendor's transaction history page."""
    return render_template('vendor_transaction_history.html')

# Add this new route with the other vendor routes in app.py

@app.route('/vendor/subscription')
def vendor_subscription():
    """Renders the vendor's subscription management page."""
    return render_template('vendor_subscription.html')

# Add this new route with the other vendor routes in app.py

@app.route('/vendor/manage_items')
def vendor_manage_items():
    """Renders the vendor's item management page."""
    return render_template('vendor_manage_items.html')

# Add this new route with the other vendor routes in app.py

@app.route('/vendor/help_support')
def vendor_help_support():
    """Renders the vendor's help and support page."""
    return render_template('vendor_help_support.html')


# --- Main entry point to run the app ---
if __name__ == '__main__':
    app.run(debug=True)

