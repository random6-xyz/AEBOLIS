from modules import app
from setting.setup import setup, ip, ports


if __name__ == "__main__":
    db_setup()
    app.run(ip, port=ports, debug=True)
