import subprocess
import platform
import re
import sys

def ping_host(host):
    """
    Pings a single host and returns a tuple: (is_reachable, avg_time)
    Works on Windows, Linux, and macOS.
    """
    current_os = platform.system().lower()
    
    # Configure the command based on OS
    if current_os == 'windows':
        # -n 1: one packet, -w 2000: 2 second timeout (ms)
        command = ['ping', '-n', '1', '-w', '2000', host]
    else:
        # -c 1: one packet, -W 2: 2 second timeout (seconds)
        command = ['ping', '-c', '1', '-W', '2', host]

    try:
        # Execute the ping command and capture output
        # universal_newlines=True ensures we get a string back, not bytes
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
        
        # Regex patterns to find the average response time
        # Windows: "Average = 15ms"
        # Linux: "avg/min/max/mdev = 15.123"
        # macOS: "round-trip min/avg/max/stddev = 10.1/15.2/20.3"
        search_patterns = [
            r"Average = (\d+)ms",                        # Windows
            r"avg/min/max/mdev = (\d+\.\d+)",           # Linux
            r"round-trip min/avg/max/stddev = [\d\.]+/(\d+\.\d+)"  # macOS
        ]
        
        avg_time = "N/A"
        for pattern in search_patterns:
            match = re.search(pattern, output, re.IGNORECASE)
            if match:
                avg_time = match.group(1)
                break
        
        return True, avg_time

    except (subprocess.CalledProcessError, FileNotFoundError):
        # CalledProcessError happens if the host is unreachable (ping returns non-zero)
        return False, None

def main():
    print("=" * 60)
    print("                PYTHON PING SCANNER v1.0")
    print("=" * 60)
    
    user_input = input("Enter hostname(s) or IP(s) separated by commas: ")
    
    # Clean up the input into a list of hosts
    hosts = [h.strip() for h in user_input.split(',') if h.strip()]

    if not hosts:
        print("Error: No hosts provided.")
        return

    print(f"\n{'Target Host':<30} | {'Status':<12} | {'Avg Time (ms)':<15}")
    print("-" * 60)

    for host in hosts:
        reachable, avg_time = ping_host(host)
        
        status = "REACHABLE" if reachable else "UNREACHABLE"
        time_display = f"{avg_time} ms" if avg_time else "---"
        
        print(f"{host:<30} | {status:<12} | {time_display:<15}")

    print("-" * 60)
    print("Scan Complete.")

if __name__ == "__main__":
    main()