from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({
        'status': 'success',
        'message': 'Pakistan Number Info API is running',
        'usage': '/api?num=3359736848',
    })

@app.route('/api', methods=['GET'])
def api():
    try:
        # Get number from query parameter 'num'
        search_query = request.args.get('num', '').strip()
        
        if not search_query:
            return jsonify({
                'success': False,
                'error': 'Please provide a number using ?num= parameter'
            }), 400
        
        # Prepare form data for the source API request
        form_data = {
            'post_id': '413',
            'form_id': '5e17544',
            'referer_title': 'Search SIM and CNIC Details - Instant Ownership Check',
            'queried_id': '413',
            'form_fields[search]': search_query,
            'action': 'elementor_pro_forms_send_form',
            'referrer': 'https://simownership.com/search/'
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Mobile Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://simownership.com',
            'Referer': 'https://simownership.com/search/'
        }
        
        # Make request to the source website
        response = requests.post(
            'https://simownership.com/wp-admin/admin-ajax.php',
            headers=headers,
            data=form_data,
            timeout=30
        )
        
        if response.status_code == 200:
            api_data = response.json()
            
            if api_data.get('success') and api_data.get('data', {}).get('data', {}).get('results'):
                results = api_data['data']['data']['results']
                
                # Sanitize and format results
                formatted_results = []
                for res in results:
                    formatted_results.append({
                        'number': res.get('n', 'N/A'),
                        'name': res.get('name', 'N/A'),
                        'cnic': res.get('cnic', 'N/A'),
                        'address': res.get('address', 'N/A')
                    })

                return jsonify({
                    'success': True,
                    'count': len(formatted_results),
                    'results': formatted_results,
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'No records found'
                }), 404
        else:
            return jsonify({
                'success': False,
                'error': 'Source service connection failed'
            }), 503
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Keep the original /search route for compatibility if needed
@app.route('/search', methods=['POST'])
def search_legacy():
    data = request.json
    num = data.get('query', '')
    # Redirect internally to the api logic
    with app.test_request_context(query_string={'num': num}):
        return api()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
