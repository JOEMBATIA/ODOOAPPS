import xmlrpc
from odoo import http
from odoo.http import request, Response
import json
import logging

_logger = logging.getLogger(__name__)


class ProjectApiController(http.Controller):
    @http.route('/api/get_projects', auth='public', methods=['POST'], csrf=False)
    def get_projects(self, **kwargs):
        try:
            data = json.loads(request.httprequest.data)

            # Extract credentials and connection details from the request payload
            url = data.get('url')
            db = data.get('db')
            username = data.get('username')
            password = data.get('password')

            if not all([url, db, username, password]):
                return Response("Missing required fields", status=400, mimetype='application/json')

            # Connect to the Odoo instance
            common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
            uid = common.authenticate(db, username, password, {})
            if uid is None:
                return Response("Authentication failed", status=403, mimetype='application/json')

            models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
            projects = models.execute_kw(db, uid, password, 'project.project', 'search_read', [[]],
                                         {'fields': ['name', 'id']})

            return request.make_response(json.dumps({
                'message': 'Projects fetched successfully',
                'projects': projects
            }), headers={'Content-Type': 'application/json'})

        except json.JSONDecodeError:
            return Response("Invalid JSON payload", status=400, mimetype='application/json')

        except xmlrpc.client.Fault as e:
            return Response(f"XML-RPC Fault: {str(e)}", status=500, mimetype='application/json')

        except Exception as e:
            return Response(f"An error occurred: {str(e)}", status=500, mimetype='application/json')
