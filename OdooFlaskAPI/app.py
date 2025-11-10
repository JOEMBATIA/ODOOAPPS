from flask import Flask, jsonify, request
import xmlrpc.client
import base64
import re

app = Flask(__name__)

# Connect to Odoo
def get_odoo_connection(odoo_url, db_name, email, password):
    common = xmlrpc.client.ServerProxy(f'{odoo_url}/xmlrpc/2/common')
    uid = common.authenticate(db_name, email, password, {})
    return uid

def strip_html(html):
    # Convert HTML to plain text while keeping paragraphs
    clean = re.sub('<h1>(.*?)</h1>', r'\n\1\n', html)  # Keep <h1> text
    clean = re.sub('<p>(.*?)</p>', r'\1\n', clean)    # Keep <p> text
    return clean.strip()

@app.route('/api/get_projects', methods=['POST'])
def fetch_projects():
    # Get credentials from the request payload
    data = request.get_json()
    odoo_url = data.get('odoo_url')
    db_name = data.get('db_name')
    email = data.get('email')
    password = data.get('password')

    if not all([odoo_url, db_name, email, password]):
        return jsonify({'error': 'Missing credentials'}), 400

    uid = get_odoo_connection(odoo_url, db_name, email, password)

    if not uid:
        return jsonify({'error': 'Invalid credentials'}), 401

    models = xmlrpc.client.ServerProxy(f'{odoo_url}/xmlrpc/2/object')

    # Fetch projects from the Odoo project module
    project_ids = models.execute_kw(
        db_name, uid, password,
        'project.project', 'search',
        [[]]
    )
    projects = models.execute_kw(
        db_name, uid, password,
        'project.project', 'read',
        [project_ids], {'fields': ['name', 'user_id', 'description','date_start', 'country_id', 'state_id', 'image', 'active']}
    )

    # Process and format output
    formatted_projects = []

    for project in projects:
        # Extract the name attributes from user_id, country_id, and state_id
        coordinator = project.get('user_id')[1] if project.get('user_id') else None
        country_name = project.get('country_id')[1] if project.get('country_id') else None
        state_name = project.get('state_id')[1] if project.get('state_id') else None

        # Fetch the email of the coordinator using the user_id
        coordinator_email = None
        if project.get('user_id'):
            user_id = project['user_id'][0]  # Fetch the user_id (ID)
            # Fetch the email from the res.users model
            user_data = models.execute_kw(
                db_name, uid, password,
                'res.users', 'read',
                [[user_id]], {'fields': ['email']}
            )
            coordinator_email = user_data[0]['email'] if user_data and 'email' in user_data[0] else None

        # Ensure the correct order and structure of the output
        formatted_project = {
            'active': project.get('active'),
            'name': project.get('name'),
            'coordinator': coordinator,  # Fetch user name
            'coordinator_email': coordinator_email,  # Fetch user email
            'description': strip_html(project.get('description', '')),
            'date_start': project.get('date_start'),
            'country': country_name,  # Fetch country name
            'county': state_name,  # Fetch state name
            # 'image': base64.b64encode(project['image'].encode('utf-8')).decode('utf-8') if isinstance(
            #     project.get('image'), str) else None
        }

        formatted_projects.append(formatted_project)

    # Return the JSON response with the desired structure
    return jsonify(formatted_projects)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
