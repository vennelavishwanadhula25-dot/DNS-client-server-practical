# dns_server.py

import argparse

import socket

 

MAX_MESSAGE_BYTES = 1024

DEFAULT_PORT = 5053

 

 

def resolve_domain(domain: str) -> list[str]:

    """Return unique IPv4 and IPv6 addresses using the system resolver."""

    results = socket.getaddrinfo(

        domain,

        None,

        family=socket.AF_UNSPEC,

        type=socket.SOCK_STREAM,

    )

    addresses = []

    seen = set()

    for result in results:

        ip_address = result[4][0]

        if ip_address not in seen:

            seen.add(ip_address)

            addresses.append(ip_address)

    return addresses

 

 

def main() -> None:

    parser = argparse.ArgumentParser(description="DNS lookup UDP server")

    parser.add_argument("--host", default="127.0.0.1",

                        help="bind address (default: localhost only)")

    parser.add_argument("--port", type=int, default=DEFAULT_PORT)

    args = parser.parse_args()

 

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:

        server.bind((args.host, args.port))

        print(f"DNS lookup server listening on {args.host}:{args.port}")

        print("Press Ctrl+C to stop.")

        try:

            while True:

                data, client_address = server.recvfrom(MAX_MESSAGE_BYTES)

                domain = "<invalid>"

                try:

                    domain = data.decode("utf-8").strip()

                    if not domain or len(domain) > 253:

                        raise ValueError("domain name must contain 1 to 253 characters")

                    if any(ch.isspace() for ch in domain):

                        raise ValueError("domain name must not contain spaces")

 

                    addresses = resolve_domain(domain)

                    if not addresses:

                        response = f"ERROR: No IP addresses found for {domain}"

                    else:

                        response = f"Domain: {domain}\nIP addresses:\n" + "\n".join(addresses)

                except (UnicodeDecodeError, ValueError) as error:

                    response = f"ERROR: Invalid request: {error}"

                except socket.gaierror as error:

                    response = f"ERROR: Could not resolve domain: {error.strerror}"

                except OSError as error:

                    response = f"ERROR: Resolver/network failure: {error}"

 

                server.sendto(response.encode("utf-8"), client_address)

                print(f"Request from {client_address}: {domain}")

        except KeyboardInterrupt:

            print("\nServer stopped.")

 

 

if __name__ == "__main__":

    main()