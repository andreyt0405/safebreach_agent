import threading
import uuid
import logging

from agent_database import AgentDatabase
from tornado_handler import TornadoHandler

# Global variable to control agent running state
agent_running = threading.Event()
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Agent:
    def __init__(self):
        """Initialize the Agent instance."""
        self.server_threads = {}
        self.database = AgentDatabase(database="agent_db")
        self.lock = threading.Lock()

    def initialize_database(self):
        """Initialize and connect the database, creating necessary tables."""
        try:
            logging.info("Initializing database connection...")
            self.database.connect()
            self.database.create_new_table("servers", "(id TEXT PRIMARY KEY, port INTEGER, status TEXT)")
        except Exception as e:
            logging.error(f"Failed to initialize database: {e}")
            self.cleanup()
            raise

    def get_dns_by_query(self, domain):
        """Resolve a domain to its IP address."""
        import socket
        try:
            logging.info(f"Resolving DNS for domain: {domain}")
            return socket.gethostbyname(domain)
        except socket.gaierror as e:
            logging.warning(f"DNS resolution failed for domain {domain}: {e}")
            return f"Error resolving domain: {e}"

    def perform_http_get_request(self, ip, port, uri):
        """Perform an HTTP GET request."""
        import requests
        url = f"http://{ip}:{port}{uri}"
        try:
            logging.info(f"Performing HTTP GET request to {url}")
            response = requests.get(url)
            return response.text
        except requests.exceptions.RequestException as e:
            logging.error(f"HTTP GET request failed for {url}: {e}")
            return f"Error performing HTTP GET request: {e}"

    def start_http_server(self, port):
        """Start a Tornado HTTP server on a separate thread."""
        if port in self.server_threads:
            logging.warning(f"Server already running on port {port}")
            return

        def run_server():
            TornadoHandler.start_server(port, self)

        try:
            logging.info(f"Starting HTTP server on port {port}")
            thread = threading.Thread(target=run_server, daemon=True)
            thread.start()
            with self.lock:
                self.server_threads[port] = thread
            unique_id = str(uuid.uuid1())
            self.database.insert("servers", ["id", "port", "status"], (unique_id, port, "running"))
            return unique_id
        except Exception as e:
            logging.error(f"Failed to start server on port {port}: {e}")

    def stop_http_server(self, port):
        """Stop the Tornado HTTP server running on the specified port."""
        try:
            logging.info(f"Stopping HTTP server on port {port}")
            TornadoHandler.stop_server(port)
            with self.lock:
                if port in self.server_threads:
                    del self.server_threads[port]
            self.database.update("servers", {"status": "stopped"}, {"port": port})
        except Exception as e:
            logging.error(f"Failed to stop server on port {port}: {e}")

    def get_server_status(self, port):
        """Get the status of the server running on the specified port."""
        try:
            logging.info(f"Fetching server status for port {port}")
            condition = f"port = {port}"
            return self.database.select("servers", "status", condition)
        except Exception as e:
            logging.error(f"Failed to get server status for port {port}: {e}")
            return None

    def cleanup(self):
        """Clean up resources such as database connections and threads."""
        logging.info("Cleaning up resources...")
        if self.database:
            self.database.close_connection()
        with self.lock:
            for port in list(self.server_threads.keys()):
                self.stop_http_server(port)

    def terminate_agent(self):
        """Kill running agent."""
        logging.info("Received kill agent command, stopping the agent...")
        agent_running.clear()
        return 0


if __name__ == '__main__':
    agent = Agent()
    try:
        agent.initialize_database()
        agent.start_http_server(8080)
        agent_running.set()
        while agent_running.is_set():
            pass
        else:
            agent.cleanup()

    except Exception as e:
        logging.critical(f"Agent encountered a critical error: {e}")
    finally:
        agent.cleanup()
