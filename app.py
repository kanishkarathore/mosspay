from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

# --- App Configuration ---
app = Flask(__name__)
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'your-super-secret-key-for-sessions' # Make sure this is strong in production
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# --- Database Helper Function ---
def get_db_connection():
    """Establishes a connection to the database."""
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row # Allows accessing columns by name
    return conn


# --- General Routes ---

@app.route('/')
def index():
    """Renders the main landing page."""
    return render_template('index.html')

@app.route('/logout')
def logout():
    """Logs the user or vendor out by clearing the session."""
    user_type = session.get('user_type')
    session.clear()
    flash('You have been successfully logged out.', 'success')
    # Redirect to the correct login page based on who logged out
    if user_type == 'vendor':
        return redirect(url_for('login_vendor'))
    return redirect(url_for('login_user'))


# --- User/Consumer Routes ---

@app.route('/login/user', methods=['GET', 'POST'])
def login_user():
    """Handles user login, verification, and session creation."""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            # Store user's info in the session
            session['user_id'] = user['id']
            session['user_name'] = user['full_name']
            session['user_type'] = 'consumer'
            return redirect(url_for('consumer_dashboard'))
        else:
            flash('Login failed. Please check your email and password.', 'danger')
            return redirect(url_for('login_user'))
            
    return render_template('login_user.html')

@app.route('/register/user', methods=['GET', 'POST'])
def register_user():
    """Handles new user registration."""
    if request.method == 'POST':
        name = request.form.get('fullName')
        email = request.form.get('email')
        password = request.form.get('password')
        if not all([name, email, password]):
            flash('All fields are required!', 'danger')
            return redirect(url_for('register_user'))
        hashed_password = generate_password_hash(password)
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (full_name, email, password) VALUES (?, ?, ?)', (name, email, hashed_password))
            conn.commit()
            flash('Registration successful! Please log in.', 'success')
        except sqlite3.IntegrityError:
            flash('Email address already registered.', 'danger')
        finally:
            conn.close()
        return redirect(url_for('login_user'))
    return render_template('register_user.html')

@app.route('/dashboard/consumer')
def consumer_dashboard():
    """Displays the personalized dashboard for the logged-in user."""
    if 'user_id' not in session or session.get('user_type') != 'consumer':
        flash('You need to be logged in to view this page.', 'danger')
        return redirect(url_for('login_user'))

    user_id = session['user_id']
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()

    return render_template('consumer_dashboard.html', user=user)

@app.route('/scan_pay')
def scan_pay():
    """Renders the Scan & Pay page for consumers."""
    return render_template('scan_pay.html')

@app.route('/log_purchase')
def log_purchase():
    """Renders the Log Purchase page for consumers."""
    return render_template('log_purchase.html')

@app.route('/discover_vendors')
def discover_vendors():
    """Renders the Discover Vendors page for consumers."""
    return render_template('discover_vendors.html')

@app.route('/redeem')
def redeem():
    """Renders the Redeem Coins page for consumers."""
    return render_template('redeem.html')

@app.route('/ecotips')
def ecotips():
    """Renders the Eco-Tips page for consumers."""
    return render_template('ecotips.html')

@app.route('/refer_earn')
def refer_earn():
    """Renders the Refer & Earn page for consumers."""
    return render_template('refer_earn.html')

@app.route('/eco_advisor')
def eco_advisor():
    """Renders the Eco-Advisor chatbot page for consumers."""
    return render_template('eco_advisor.html')

@app.route('/settings')
def settings():
    """Renders the Settings page for consumers."""
    return render_template('settings.html')

@app.route('/help')
def help():
    """Renders the Help page for consumers."""
    return render_template('help.html')


# --- Vendor/Business Routes ---

@app.route('/login/vendor', methods=['GET', 'POST'])
def login_vendor():
    """Handles vendor login, verification, and session creation."""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        conn = get_db_connection()
        vendor = conn.execute('SELECT * FROM vendors WHERE email = ?', (email,)).fetchone()
        conn.close()

        if vendor and check_password_hash(vendor['password'], password):
            # Store vendor info in the session
            session['user_id'] = vendor['id']
            session['user_name'] = vendor['business_name']
            session['user_type'] = 'vendor'
            return redirect(url_for('vendor_dashboard'))
        else:
            flash('Login failed. Please check your email and password.', 'danger')
            return redirect(url_for('login_vendor'))
            
    return render_template('login_vendor.html')

@app.route('/register/business', methods=['GET', 'POST'])
def register_business():
    """Handles new business registration."""
    if request.method == 'POST':
        business_name = request.form.get('businessName')
        contact_name = request.form.get('contactName')
        mobile = request.form.get('mobileNumber')
        udyam_id = request.form.get('udyamId')
        address = request.form.get('businessAddress')
        email = request.form.get('email')
        password = request.form.get('password')
        cert_file = request.files.get('greenCert')
        
        if not all([business_name, contact_name, mobile, udyam_id, address, email, password]):
            flash('All fields are required!', 'danger')
            return redirect(url_for('register_business'))

        hashed_password = generate_password_hash(password)
        cert_filename = "N/A"
        if cert_file and cert_file.filename != '':
            filename = secure_filename(f"{udyam_id}_{cert_file.filename}")
            cert_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            cert_filename = filename

        conn = get_db_connection()
        try:
            conn.execute(
                'INSERT INTO vendors (business_name, contact_name, mobile_number, udyam_id, business_address, email, password, cert_filename) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (business_name, contact_name, mobile, udyam_id, address, email, hashed_password, cert_filename)
            )
            conn.commit()
            flash('Business registration successful! Please log in.', 'success')
        except sqlite3.IntegrityError:
            flash('Email or Udyam ID already registered.', 'danger')
        finally:
            conn.close()
        return redirect(url_for('login_vendor'))
        
    return render_template('register_business.html')
    
# --- 
# --- vvv THIS IS THE MODIFIED FUNCTION vvv ---
# --- 
@app.route('/vendor/dashboard')
def vendor_dashboard():
    """Displays the personalized dashboard for the logged-in vendor."""
    if 'user_id' not in session or session.get('user_type') != 'vendor':
        flash('You need to be logged in as a vendor to view this page.', 'danger')
        return redirect(url_for('login_vendor'))
        
    vendor_id = session['user_id']
    conn = get_db_connection()
    vendor = conn.execute('SELECT * FROM vendors WHERE id = ?', (vendor_id,)).fetchone()
    
    # --- THIS IS THE FIX for TypeError: Object of type Row is not JSON serializable ---
    # Fetch items from the database
    items_rows = conn.execute('SELECT * FROM items WHERE vendor_id = ? ORDER BY item_name', (vendor_id,)).fetchall()
    
    # --- THIS IS THE FIX: Convert Row objects to plain dictionaries ---
    items = [dict(row) for row in items_rows]
    
    conn.close()

    # --- UPDATED THIS LINE: Pass 'items' (as a list of dicts) to the template ---
    return render_template('vendor_dashboard.html', vendor=vendor, items=items)

@app.route('/vendor/manage_items')
def vendor_manage_items():
    """Fetches and displays items for the logged-in vendor."""
    if 'user_id' not in session or session.get('user_type') != 'vendor':
        flash('Please log in to manage items.', 'danger')
        return redirect(url_for('login_vendor'))

    vendor_id = session['user_id']
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM items WHERE vendor_id = ? ORDER BY created_at DESC', (vendor_id,)).fetchall()
    conn.close()

    return render_template('vendor_manage_items.html', items=items)

@app.route('/vendor/manage_items/add', methods=['GET', 'POST'])
def vendor_add_item():
    """Handles adding a new item for the logged-in vendor."""
    if 'user_id' not in session or session.get('user_type') != 'vendor':
        flash('Please log in as a vendor to add items.', 'danger')
        return redirect(url_for('login_vendor'))
    if request.method == 'POST':
        vendor_id = session['user_id']
        item_name = request.form.get('itemName')
        category = request.form.get('itemCategory')
        price = request.form.get('itemPrice')
        unit = request.form.get('itemUnit')
        stock_status = request.form.get('stockStatus')
        item_image = request.files.get('itemImage')

        if not all([item_name, price, unit]):
            flash('Item Name, Price, and Unit are required fields.', 'danger')
            return redirect(url_for('vendor_add_item'))

        image_filename = "default_item.png" # You should have a placeholder image with this name
        if item_image and item_image.filename != '':
            filename = secure_filename(f"{vendor_id}_{item_name.replace(' ', '_')}_{item_image.filename}")
            item_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_filename = filename
        
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO items (vendor_id, item_name, category, price, unit, stock_status, image_filename) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (vendor_id, item_name, category, price, unit, stock_status, image_filename)
        )
        conn.commit()
        conn.close()

        flash(f"Item '{item_name}' has been added successfully!", 'success')
        return redirect(url_for('vendor_manage_items'))

    return render_template('vendor_add_item.html')

@app.route('/vendor/item/edit/<int:item_id>', methods=['GET', 'POST'])
def vendor_edit_item(item_id):
    """Handles editing an existing item for the logged-in vendor."""
    if 'user_id' not in session or session.get('user_type') != 'vendor':
        flash('Authentication required to perform this action.', 'danger')
        return redirect(url_for('login_vendor'))

    vendor_id = session['user_id']
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM items WHERE id = ? AND vendor_id = ?', (item_id, vendor_id)).fetchone()

    if item is None:
        flash('Item not found or you do not have permission to edit it.', 'danger')
        conn.close()
        return redirect(url_for('vendor_manage_items'))

    if request.method == 'POST':
        item_name = request.form.get('itemName')
        category = request.form.get('itemCategory')
        price = request.form.get('itemPrice')
        unit = request.form.get('itemUnit')
        stock_status = request.form.get('stockStatus')
        new_item_image = request.files.get('newItemImage')

        if not all([item_name, price, unit]):
            flash('Item Name, Price, and Unit are required fields.', 'danger')
            conn.close() # Close connection before returning
            return render_template('vendor_edit_item.html', item=item)

        image_filename = item['image_filename']
        if new_item_image and new_item_image.filename != '':
            # Optional: Delete old image file
            
            filename = secure_filename(f"{vendor_id}_{item_name.replace(' ', '_')}_{new_item_image.filename}")
            new_item_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_filename = filename

        conn.execute(
            'UPDATE items SET item_name = ?, category = ?, price = ?, unit = ?, stock_status = ?, image_filename = ? WHERE id = ? AND vendor_id = ?',
            (item_name, category, price, unit, stock_status, image_filename, item_id, vendor_id)
        )
        conn.commit()
        conn.close()

        flash(f"Item '{item_name}' has been updated successfully!", 'success')
        return redirect(url_for('vendor_manage_items'))

    # For GET request, show the form pre-filled
    conn.close() # Close connection after fetching item
    return render_template('vendor_edit_item.html', item=item)


@app.route('/vendor/item/delete/<int:item_id>', methods=['POST'])
def vendor_delete_item(item_id):
    """Handles deleting an item for the logged-in vendor."""
    if 'user_id' not in session or session.get('user_type') != 'vendor':
        flash('Authentication required to perform this action.', 'danger')
        return redirect(url_for('login_vendor'))

    vendor_id = session['user_id']
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM items WHERE id = ? AND vendor_id = ?', (item_id, vendor_id)).fetchone()

    if item is None:
        flash('Item not found or you do not have permission to delete it.', 'danger')
    else:
        conn.execute('DELETE FROM items WHERE id = ?', (item_id,))
        conn.commit()
        flash(f"Item '{item['item_name']}' has been deleted successfully.", 'success')
    
    conn.close()
    return redirect(url_for('vendor_manage_items'))

# --- 
# --- vvv THIS ROUTE HAS BEEN REMOVED vvv ---
# --- 
# @app.route('/vendor/generate_bill')
# def vendor_generate_bill():
#     return render_template('vendor_generate_bill.html')

@app.route('/vendor/scan_pay')
def vendor_scan_pay():
    return render_template('scan_pay.html')

@app.route('/vendor/manage_profile')
def vendor_manage_profile():
    return render_template('vendor_manage_profile.html')

@app.route('/vendor/manage_offers')
def vendor_manage_offers():
    return render_template('vendor_manage_offers.html')

@app.route('/vendor/customer_insights')
def vendor_customer_insights():
    return render_template('vendor_customer_insights.html')

@app.route('/vendor/transaction_history')
def vendor_transaction_history():
    return render_template('vendor_transaction_history.html')

@app.route('/vendor/subscription')
def vendor_subscription():
    return render_template('vendor_subscription.html')

@app.route('/vendor/help_support')
def vendor_help_support():
    return render_template('vendor_help_support.html')


# --- Main execution ---
if __name__ == '__main__':
    app.run(debug=True)