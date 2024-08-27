import pyfiglet
import colorama
from colorama import Fore, Style
import argparse
import requests

colorama.init(autoreset=True)

ascii_banner = pyfiglet.figlet_format("DARK 0")
print(Fore.RED + ascii_banner)

parser = argparse.ArgumentParser(description='DARK 0 Vulnerability Scanner')
parser.add_argument('-u', '--url', help='URL of the target website', required=True)
parser.add_argument('-t', '--type', help='Type of scan', required=True)
parser.add_argument('-p', '--payloads', help='Number of payloads to test', type=int, default=10)
args = parser.parse_args()

def load_payloads(vuln_type):
    with open("vulnerabilities_payloads.txt", "r") as file:
        payloads = []
        start_collecting = False
        for line in file:
            if line.strip().startswith("#") and vuln_type in line.lower():
                start_collecting = True
                continue
            if start_collecting:
                if line.strip().startswith("#"):
                    break
                if line.strip():
                    payloads.append(line.strip())
        return payloads

def load_paths(vuln_type):
    with open("paths_database.txt", "r") as file:
        paths = []
        start_collecting = False
        for line in file:
            if line.strip().startswith("#") and vuln_type in line.lower():
                start_collecting = True
                continue
            if start_collecting:
                if line.strip().startswith("#"):
                    break
                if line.strip():
                    paths.append(line.strip())
        return paths

def detect_vulnerability(url, payloads, paths, vuln_type):
    print(Fore.BLUE + f"Detecting {vuln_type.upper()} vulnerabilities on {url}...")
    found_vulnerability = False
    for path in paths:
        for i, payload in enumerate(payloads):
            if i >= args.payloads:
                break
            test_url = f"{url}{path}{payload}"
            try:
                response = requests.get(test_url)
                if response.status_code == 200:
                    print(Fore.GREEN + f"Vulnerable path found: {test_url}")
                    found_vulnerability = True
            except Exception as e:
                print(Fore.RED + f"Error testing payload {payload}: {str(e)}")

    if not found_vulnerability:
        print(Fore.RED + "No vulnerabilities found.")

vuln_type = args.type.lower()
payloads = load_payloads(vuln_type)
paths = load_paths(vuln_type)

if payloads and paths:
    detect_vulnerability(args.url, payloads, paths, vuln_type)
else:
    print(Fore.RED + "Unsupported scan type or no payloads/paths found for this type.")
