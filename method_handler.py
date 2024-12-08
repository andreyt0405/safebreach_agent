import tornado


class DNSQueryHandler(tornado.web.RequestHandler):
    def initialize(self, agent):
        self.agent = agent

    def get(self):
        # Extract the domain query parameter
        domain = self.get_argument("domain", None)
        if not domain:
            self.set_status(400)
            self.write({"error": "Missing 'domain' parameter"})
            return
        result = self.agent.get_dns_by_query(domain)
        self.write({"domain": domain, "ip": result})


class HTTPGetHandler(tornado.web.RequestHandler):
    def initialize(self, agent):
        self.agent = agent

    def get(self):
        # Extract query parameters
        ip = self.get_argument("ip", None)
        port = self.get_argument("port", None)
        uri = self.get_argument("uri", "/")
        if not ip or not port:
            self.set_status(400)
            self.write({"error": "Missing 'ip' or 'port' parameter"})
            return
        try:
            port = int(port)
        except ValueError:
            self.set_status(400)
            self.write({"error": "Invalid 'port' value, must be an integer"})
            return
        result = self.agent.perform_http_get_request(ip, port, uri)
        self.write({"url": f"http://{ip}:{port}{uri}", "response": result})


class ServerStatusHandler(tornado.web.RequestHandler):
    def initialize(self, agent):
        self.agent = agent

    def get(self):
        port = self.get_argument("port", None)
        self.write({"status": self.agent.get_server_status(port)})


class StartHttpServer(tornado.web.RequestHandler):
    def initialize(self, agent):
        self.agent = agent

    def get(self):
        port = self.get_argument("port", None)
        self.write({"unique_id": self.agent.start_http_server(port)})


class KillAgent(tornado.web.RequestHandler):
    def initialize(self, agent):
        self.agent = agent

    def get(self):
        self.write({"status_kill": self.agent.kill_agent()})
