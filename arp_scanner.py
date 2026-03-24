import subprocess
import platform
import re

def get_arp_table():
    current_os = platform.system().lower()
    cmd = ['arp', '-a'] if current_os == 'windows' else ['arp', '-n']
    
    try:
        output = subprocess.check_output(cmd, universal_newlines=True)
        ip_pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        mac_pattern = r'([0-9a-fA-F]{2}[:-][0-9a-fA-F]{2}[:-][0-9a-fA-F]{2}[:-][0-9a-fA-F]{2}[:-][0-9a-fA-F]{2}[:-][0-9a-fA-F]{2})'
        
        
        ips = re.findall(ip_pattern, output)
        macs = re.findall(mac_pattern, output)
        
        return list(zip(ips, macs))
    except Exception as e:
        print(f"Error retrieving ARP table: {e}")
        return []

def display_results(mappings):
    print(f"\n{'IP Address':<20} | {'MAC Address':<20}")
    print("-" * 45)
    for ip, mac in mappings:
        print(f"{ip:<20} | {mac:<20}")
    print("-" * 45)
    print(f"Total entries found: {len(mappings)}") [cite: 34]

if __name__ == "__main__":
    print("=== ARP Scanner ===")
    results = get_arp_table()
    display_results(results)
    
    
    save = input("\nSave results to arp_results.txt? (y/n): ").lower()
    if save == 'y':
        with open("arp_results.txt", "w") as f:
            f.write(f"{'IP Address':<20} | {'MAC Address':<20}\n")
            for ip, mac in results:
                f.write(f"{ip:<20} | {mac:<20}\n")
        print("Results saved successfully.")