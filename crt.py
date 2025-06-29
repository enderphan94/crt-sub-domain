import requests
from bs4 import BeautifulSoup
import argparse
import os

# Function to check if the subdomain is alive using both HTTP and HTTPS
def is_subdomain_alive(subdomain):
    protocols = ['http://', 'https://']
    for protocol in protocols:
        try:
            response = requests.head(f"{protocol}{subdomain}", timeout=5)
            if 200 <= response.status_code < 400:
                return True
        except requests.exceptions.RequestException:
            continue
    return False

# Function to find alive subdomains for a single domain
def find_alive_subdomains(domain):
    print(f"\n[+] Processing: {domain}")
    target_url = f"https://crt.sh/?q={domain}"

    try:
        response = requests.get(target_url, timeout=10)
    except Exception as e:
        print(f"Error fetching crt.sh for {domain}: {e}")
        return []

    if response.status_code != 200:
        print(f"Failed to retrieve data from crt.sh for {domain}. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    subdomains = set()

    for row in soup.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) > 4:
            subdomain = cells[4].text.strip()
            if '*' in subdomain:
                subdomain = subdomain.replace('*.', '')  # Clean wildcard
            if '.' in subdomain:
                subdomains.add(subdomain)

    alive_subdomains = []
    for subdomain in subdomains:
        if is_subdomain_alive(subdomain):
            print(f"[+] Alive: {subdomain}")
            alive_subdomains.append(subdomain)

    return alive_subdomains

# Main script with argument parser
def main():
    parser = argparse.ArgumentParser(description="Crawl subdomains from crt.sh and check if they are alive")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-t', '--target', type=str, help='Single domain to scan')
    group.add_argument('-T', '--target-file', type=str, help='File containing list of domains to scan')

    args = parser.parse_args()

    domains = []
    if args.target:
        domains = [args.target]
    elif args.target_file:
        if not os.path.exists(args.target_file):
            print(f"File not found: {args.target_file}")
            return
        with open(args.target_file, 'r') as f:
            domains = [line.strip() for line in f if line.strip()]

    for domain in domains:
        alive_subdomains = find_alive_subdomains(domain)
        output_file = f"{domain}_alive_subdomains.txt"
        with open(output_file, 'w') as f:
            for subdomain in alive_subdomains:
                f.write(f"{subdomain}\n")
        print(f"[+] Saved alive subdomains to {output_file}")

if __name__ == "__main__":
    main()
