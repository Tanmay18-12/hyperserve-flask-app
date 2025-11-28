from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        'service': 'HyperServe',
        'status': 'online',
        'cie_set': '207',
        'version': '3.0',
        'message': 'HyperServe service online for CIE set 207'
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'service': 'hyperserve-svc:3'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 12208))
    app.run(host='0.0.0.0', port=port, debug=False)