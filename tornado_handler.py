import asyncio
import logging

import tornado.ioloop
import tornado.web

from method_handler import DNSQueryHandler, HTTPGetHandler, ServerStatusHandler, StartHttpServer, KillAgent


class TornadoHandler:
    servers = {}

    @staticmethod
    def make_app(agent):
        """Create a Tornado application with additional routes."""
        return tornado.web.Application([
            (r"/dns-query", DNSQueryHandler, dict(agent=agent)),
            (r"/http-get", HTTPGetHandler, dict(agent=agent)),
            (r"/server-status", ServerStatusHandler, dict(agent=agent)),
            (r"/start-http-server", StartHttpServer, dict(agent=agent)),
            (r"/kill-agent", KillAgent, dict(agent=agent)),
        ])

    @staticmethod
    def start_server(port, agent):
        """Start the Tornado server on the specified port."""
        asyncio.set_event_loop(asyncio.new_event_loop())
        app = TornadoHandler.make_app(agent)
        server = app.listen(port)
        TornadoHandler.servers[port] = server
        logging.info(f"Server started on port {port}")
        asyncio.get_event_loop().run_forever()

    @staticmethod
    def stop_server(port):
        """Stop the Tornado server running on the specified port."""
        if port in TornadoHandler.servers:
            server = TornadoHandler.servers[port]
            server.stop()  # Stops listening on the port
            del TornadoHandler.servers[port]
            logging.info(f"Server on port {port} stopped.")
        else:
            logging.warning(f"No server found running on port {port}.")
