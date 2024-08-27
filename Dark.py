import pyfiglet
import colorama
from colorama import Fore, Style
import argparse

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

def detect_vulnerability(url, payloads, vuln_type):
    print(Fore.BLUE + f"Detecting {vuln_type.upper()} vulnerabilities on {url}...")
    for i, payload in enumerate(payloads):
        if i >= args.payloads:
            break
        print(Fore.GREEN + f"Testing payload: {payload} on {url}")

vuln_type = args.type.lower()
payloads = load_payloads(vuln_type)

if payloads:
    detect_vulnerability(args.url, payloads, vuln_type)
else:
    print(Fore.RED + "Unsupported scan type or no payloads found for this type.")
