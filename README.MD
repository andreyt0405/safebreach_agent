# **Agent Management System**

## **Overview**

This program implements an **Agent Management System**, designed to handle various tasks, including:

- Managing HTTP servers.
- Performing DNS queries.
- Executing HTTP GET requests.
- Providing an interface to start or stop services via HTTP endpoints using the **Tornado** web framework.

### **Main Components**

1. **Agent**
    - Manages HTTP servers.
    - Interacts with a database to store server statuses.
    - Provides utility functions for DNS resolution and HTTP requests.

2. **TornadoHandler**
    - Manages HTTP APIs for interacting with the Agent via endpoints.
    - Handles requests for DNS queries, HTTP GET requests, server management, and killing the agent.

---

## **Features**

- **Database Integration**: Maintains a record of server states using the `AgentDatabase`.
- **HTTP API Endpoints**: Provides RESTful endpoints via the Tornado web server.
- **DNS Query**: Resolves domain names to IP addresses.
- **HTTP GET Requests**: Performs HTTP GET requests to specified URLs.
- **Server Management**: Allows starting and stopping Tornado servers on specific ports.
- **Graceful Cleanup**: Ensures all resources (servers, database connections) are cleaned up during termination.

---

## **How It Works**

### **1. Main Components**

#### **Agent**

- Initializes and manages HTTP servers.
- Performs database operations.
- Provides utility functions for DNS resolution and HTTP requests.
- Supports starting, stopping, and querying server status.

#### **TornadoHandler**

- Acts as the REST API layer to interact with the **Agent**.
- Exposes endpoints for DNS queries, HTTP GET requests, server management, and killing the agent.

---

## **Running the Program**

### **Prerequisites**

- **Python 3.8+** installed.
- Install required libraries:
  ```bash
  pip install -r requirements.txt
- Run the program using pycharm or command line
- The program is running and waiting for GET requests
- Use postman or using CURL tool

## **API usage examples**

### **Requests**

- **Request Example Start new server**:
  ```bash
  curl "http://localhost:8080/get-http-server?port=9090"
- **Response Example Start new server**:
  ```bash
  {"unique_id": "f81d4fae-7dec-11d0-a765-00a0c91e6bf6"}
