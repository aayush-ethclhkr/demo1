import socket
import nmap
import requests

def scan_ports(target):
    print(f"\n[+] Scanning ports on {target} ...")
    scanner = nmap.PortScanner()
    scanner.scan(hosts=target, arguments='-p 1-1024 --open')

    for host in scanner.all_hosts():
        print(f"\n[+] Host: {host} ({scanner[host].hostname()})")
        print(f"    State: {scanner[host].state()}")
        for proto in scanner[host].all_protocols():
            ports = scanner[host][proto].keys()
            for port in sorted(ports):
                print(f"    Port: {port} ({proto}) - State: {scanner[host][proto][port]['state']}")




import requests

def get_cve_info_nvd(service, api_key):
    print(f"\n[+] Searching CVEs for service: {service}")
    try:
        headers = {
            'apiKey': api_key
        }
        params = {
            'keywordSearch': service,
            'resultsPerPage': 5
        }
        url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        response = requests.get(url, headers=headers, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            cves = data.get('vulnerabilities', [])

            if not cves:
                print("    [!] No CVEs found for this service.")
                return

            for cve in cves:
                cve_id = cve['cve']['id']
                description = cve['cve']['descriptions'][0]['value']
                print(f"    - {cve_id}: {description}")

        else:
            print(f"    [!] API error: {response.status_code}")

    except Exception as e:
        print(f"    [!] Could not fetch CVE data: {e}")


if __name__ == "__main__":
    target = input("[?] Enter target IP address: ")
    scan_ports(target)
    
    
   

    service = input("\n[?] Enter service name (e.g., apache, openssh, nginx): ")
    api_key = "339f6977-9631-41e5-b50d-cc03f26f59de"
    get_cve_info_nvd(service, api_key)

