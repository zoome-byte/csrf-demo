# csrf_crawler.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def crawl_for_csrf(url):
    visited = set()
    to_visit = [url]
    session = requests.Session()

    while to_visit:
        current = to_visit.pop()
        if current in visited:
            continue
        visited.add(current)

        try:
            res = session.get(current)
            soup = BeautifulSoup(res.text, 'html.parser')
            forms = soup.find_all('form')
            print(f"\n[+] {len(forms)} forms found in {current}")
            for i, form in enumerate(forms):
                inputs = form.find_all('input')
                has_csrf = any('csrf' in (inp.get('name') or '').lower() for inp in inputs)
                if not has_csrf:
                    print(f"    [!] Form {i+1} might be vulnerable – No CSRF token.")
                else:
                    print(f"    [+] Form {i+1} has CSRF protection.")
            for link in soup.find_all('a', href=True):
                full = urljoin(current, link['href'])
                if full.startswith(url) and full not in visited:
                    to_visit.append(full)
        except Exception as e:
            print(f"[ERROR] Failed to load {current} – {e}")

# Replace with your test site
if __name__ == "__main__":
    crawl_for_csrf("http://testphp.vulnweb.com")
