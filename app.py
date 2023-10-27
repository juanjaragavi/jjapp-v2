from flask import Flask
import requests
import os
from supabase import create_client, Client
from decouple import config

key = config('SUPABASE_KEY')
url = config('SUPABASE_URL')
supabase: Client = create_client(url, key)

if os.environ.get('ENV') == 'production':
    from decouple import Csv
    config = Csv('jjapp/.env')

print(f'SUPABASE_KEY: {key}')
print(f'SUPABASE_URL: {url}')

app = Flask(__name__)

@app.route('/api/cats', methods=['GET'])
def get_resource():

    response = supabase.table('cat_breeds').select("breed").execute()

    return str(response)

def check_domain_response(domain):
    try:
        response = requests.get(domain)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.RequestException:
        return False

@app.route('/api/domains', methods=['GET'])    
def api_check_domains():
    domains = ['https://juanjaramillo.tech/', 'https://blog.juanjaramillo.tech/', 'https://shop.juanjaramillo.tech/', 'https://testing.juanjaramillo.tech/']
    results = {}

    for domain in domains:
        results[domain] = check_domain_response(domain)

    return str(results)

if __name__ == '__app__':
    app.run(host='0.0.0.0', port=5000)