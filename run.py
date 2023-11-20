from dotenv import load_dotenv
import os
from app import create_app

load_dotenv()

if __name__ == '__main__':
    app = create_app(config_name=os.getenv('FLASK_ENV'))
    port = os.getenv("FLASK_PORT", 5000)
    ip = os.getenv("FLASK_IP", '127.0.0.1')
    app.run(host=ip, port=port, debug=True)