import argparse
import socket

DEFAULT_PORT = 5053
MAX_RESPONSE_BYTES = 4096


def main() -> None:
    parser = argparse.ArgumentParser(description="Ask a DNS lookup server for a domain")
    parser.add_argument("domain", help="domain name to resolve, such as example.com")
    parser.add_argument("--server", default="127.0.0.1", help="server IP address")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--timeout", type=float, default=5.0, help="wait time in seconds")
    args = parser.parse_args()

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
            client.settimeout(args.timeout)
            client.sendto(args.domain.encode("utf-8"), (args.server, args.port))
            response, _ = client.recvfrom(MAX_RESPONSE_BYTES)
        print(response.decode("utf-8"))
    except socket.timeout:
        print("ERROR: No reply received. Is server.py running on the selected address and port?")
    except (UnicodeEncodeError, OSError) as error:
        print(f"ERROR: Could not communicate with the server: {error}")


if __name__ == "__main__":
    main()

     