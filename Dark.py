import requests
import pyfiglet
from termcolor import colored

# تعريف ألوان الطباعة
def print_result(message, success=True):
    color = 'green' if success else 'red'
    print(colored(message, color))

# تحميل payloads من قاعدة البيانات
def load_payloads(file_path):
    payloads = {}
    current_type = None
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith('#'):
                    current_type = line[1:].strip().lower()
                    payloads[current_type] = []
                elif current_type and line:
                    payloads[current_type].append(line)
    except FileNotFoundError:
        print("Payloads file not found.")
    return payloads

# إجراء اختبار الثغرة
def test_vulnerability(url, scan_type, payloads):
    if scan_type not in payloads:
        print_result(f"Unsupported scan type: {scan_type}", success=False)
        return

    found_vulnerability = False
    for payload in payloads[scan_type]:
        test_url = f"{url}/{payload}"
        try:
            response = requests.get(test_url, timeout=10)
            if response.status_code == 200:
                print_result(f"Vulnerable path found: {test_url}", success=True)
                found_vulnerability = True
        except requests.RequestException:
            pass

    if not found_vulnerability:
        print_result(f"No vulnerabilities found for {url} with scan type {scan_type}", success=False)

# تنفيذ الأداة
def main():
    ascii_banner = pyfiglet.figlet_format("DARK 0")
    print(colored(ascii_banner, 'cyan'))

    url = input("Enter target URL: ")
    scan_type = input("Enter scan type: ").lower()
    payload_file = "vulnerabilities_payloads.txt"

    payloads = load_payloads(payload_file)
    test_vulnerability(url, scan_type, payloads)

if __name__ == "__main__":
    main()
