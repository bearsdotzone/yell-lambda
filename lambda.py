from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
import random

members = requests.get(
    'https://raw.githubusercontent.com/bearsdotzone/blasebears/main/data/members.json').json()
m_nextmap = dict()
m_prevmap = dict()
howmany = len(members)
for x in range(howmany):
    y = (x + 1) % howmany
    z = (x - 1) % howmany
    m_nextmap[members[x]['url']] = members[y]['url']
    m_prevmap[members[x]['url']] = members[z]['url']

class WebServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(303)
        self.send_header('cache-control', 'no-cache')
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        referer = self.headers['Referer']
        if self.path.endswith('next'):
            self.send_header(
                'Location', m_nextmap[referer] if referer in m_nextmap else random.choice(members)['url'])
        if self.path.endswith('prev'):
            self.send_header(
                'Location', m_prevmap[referer] if referer in m_nextmap else random.choice(members)['url'])
        if self.path.endswith('random'):
            self.send_header('Location', random.choice(members)['url'])
        self.end_headers()

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print("Web server is running on port {}".format(port))
        server.serve_forever()

    except KeyboardInterrupt:
        print("^C entered, stopping web server...")
        server.socket.close()


if __name__ == '__main__':
    main()
