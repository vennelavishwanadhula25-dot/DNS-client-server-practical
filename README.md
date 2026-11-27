# DNS-Based Client-Server Application

## Aim
Develop a DNS-based client-server application that accepts domain-name
queries, resolves them to IP addresses, and returns the results using
socket communication.

## Technologies
- Python 3
- socket module
- UDP (User Datagram Protocol)

## How to run
1. Open a terminal in this folder.
2. Start the server: `python dns_server.py`
3. Open a second terminal.
4. Start the client: `python dns_client.py`
5. Enter a domain name when prompted.

## Note
This is an educational hostname-resolution application. The server uses
Python's system resolver function; it is not a full implementation of
the DNS wire protocol.

## Files
- `dns_server.py` — server program
- `dns_client.py` — client program
- `DNS_Practical_2_Notes.docx` — practical notes and explanation
