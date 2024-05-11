from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import sqlite3
import os
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__)

# Function to establish connection to SQLite database
def get_db_connection():
    conn = sqlite3.connect('keyinfo.db')
    conn.row_factory = sqlite3.Row #allows selecting a row of tuples with column name
    return conn

# Function to initialize database schema
def init_db():
    with app.app_context():
        db = get_db_connection()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

"""Route to store username, keys and imagepath"""
@app.route('/store', methods=['POST'])
def store_data():
    if 'image_path' not in request.files:
        return jsonify({'error': 'No file part'})

    username = request.form['username']
    public_key = request.form['public_key']
    facebook_URL = request.form['facebook_URL']

    db = get_db_connection()
    try:
        db.execute('INSERT INTO keys (username, public_key, facebook_URL) VALUES (?, ?, ?)',
                   (username, public_key, facebook_URL))
        db.commit()
    except Exception as e:
        db.rollback()  # Rollback changes if an error occurs
        db.close()
        return jsonify({'error': 'Database operation failed: {}'.format(str(e))}), 500

    db.close()
    return jsonify({'message': 'Data uploaded successfully'}), 201



"""route to search database with username-substring"""
@app.route('/fetch_data', methods=['GET'])
def fetch_data():
  substring = request.args.get('substring')  # Get substring from query string
  if not substring:
    return jsonify({'error': 'Missing required parameter: substring'}), 400

  limit = 10  # Limit results to 10 tuples

  db = get_db_connection()
  try:
    # Escape the substring to prevent SQL injection
    cursor = db.cursor()
    cursor.execute("""
      SELECT *
      FROM keys
      WHERE username LIKE %s
      LIMIT ?
    """, ('%' + substring + '%', limit))
    data = cursor.fetchall()  # Fetch all matching rows
  except Exception as e:
    db.rollback()  # Rollback if error
    db.close()
    return jsonify({'error': 'Database error: {}'.format(str(e))}), 500
  finally:
    db.close()  # Always close connection

  # Convert data to array of tuples
  data_array = [item for item in data]

  return jsonify({'data': data_array})

"route to search facebook_url"
@app.route('/fetch_single', methods=['GET'])
def fetch_single():
  value = request.args.get('value')  # Get value from query string
  attribute = request.args.get('attribute')  # Get attribute name

  if not value or not attribute:
    return jsonify({'error': 'Missing required parameters: value or attribute'}), 400

  db = get_db_connection()
  try:
    cursor = db.cursor()
    cursor.execute("""
      SELECT *
      FROM keys
      WHERE facebook_URL = ?
      LIMIT 1
    """, (value,))  # Single value as tuple
    data = cursor.fetchone()  # Fetch single matching row (or None)
  except Exception as e:
    db.rollback()  # Rollback if error
    db.close()
    return jsonify({'error': 'Database error: {}'.format(str(e))}), 500
  finally:
    db.close()  # Always close connection

  return jsonify({'data': data}) if data else jsonify({'message': 'No matching record found'})


""" route to search for facebook_URL"""
@app.route('/append_facebook_url', methods=['POST'])
def append_facebook_url():
  username = request.form.get('username')
  facebook_url = request.form.get('facebook_URL')

  if not username or not facebook_url:
    return jsonify({'error': 'Missing required parameters: username or facebook_URL'}), 400

  db = get_db_connection()
  try:
    cursor = db.cursor()
    # Escape the URL to prevent SQL injection
    cursor.execute("""
      UPDATE your_table
      SET facebook_URL = CONCAT(COALESCE(facebook_URL, ''), ?)
      WHERE username = ?
    """, (facebook_url, username))
    db.commit()
  except Exception as e:
    db.rollback()  # Rollback if error
    db.close()
    return jsonify({'error': 'Database error: {}'.format(str(e))}), 500
  finally:
    db.close()  # Always close connection

  return jsonify({'message': 'Facebook URL appended successfully'})

"""route to append facebook url for appending existing username"""
@app.route('/append_facebook_url', methods=['POST'])
def append_facebook_url_attribute():
  username = request.form.get('username')
  facebook_url = request.form.get('facebook_URL')

  if not username or not facebook_url:
    return jsonify({'error': 'Missing required parameters: username or facebook_URL'}), 400

  db = get_db_connection()
  try:
    cursor = db.cursor()
    # Escape the URL to prevent SQL injection
    cursor.execute("""
      UPDATE keys
      SET facebook_URL = CONCAT(COALESCE(facebook_URL, ''), ?)
      WHERE username = ?
    """, (facebook_url, username))
    db.commit()
  except Exception as e:
    db.rollback()  # Rollback if error
    db.close()
    return jsonify({'error': 'Database error: {}'.format(str(e))}), 500
  finally:
    db.close()  # Always close connection

  return jsonify({'message': 'Facebook URL appended successfully'})


if __name__ == '__main__':
    init_db()