import subprocess
import sys
import platform

def check_nmap():
    try:
        subprocess.check_output(['nmap', '--version'])
        return True
    except FileNotFoundError:
        return False

def run_nmap_scan(target, scan_type):
    options = {
        '1': ['-sn'],        # Host Discovery
        '2': ['-p', '1-1000'], # Port Scan
        '3': ['-sV'],        # Service Version
        '4': ['-O']          # OS Detection (Requires sudo)
    }
    
    command = ['nmap'] + options.get(scan_type, ['-sn']) + [target]
    
    print(f"[*] Running scan: {' '.join(command)}...")
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=300)
        return result.stdout
    except subprocess.TimeoutExpired:
        return "Error: Scan timed out."
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    if not check_nmap():
        print("Error: Nmap is not installed.") [cite: 40, 62]
        sys.exit(1)
        
    target = input("Enter target IP or range (e.g., 192.168.1.1): ")
    print("\nSelect Scan Type:\n1. Host Discovery (-sn)\n2. Port Scan (1-1000)\n3. Service Version (-sV)\n4. OS Detection (-O)")
    choice = input("Enter choice (1-4): ")
    
    output = run_nmap_scan(target, choice)
    print("\n--- Scan Results ---")
    print(output)