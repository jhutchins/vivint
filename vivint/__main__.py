from server import Server
from service import Service

# Run the web server
if __name__ == '__main__':
    Server(Service()).run()
