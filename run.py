import os
from app import create_app
from dotenv import load_dotenv

load_dotenv()
app = create_app(config_name='development')

if __name__ == '__main__':
    port = os.getenv("FLASK_PORT", 5000)
    ip = os.getenv("FLASK_IP", '127.0.0.1')
    app.run(host=ip, port=port, debug=True)