# crt-sub-domain
Crawl subdomains from crt.sh and check if they are alive
# Usage


```
usage: crt.py [-h] (-t TARGET | -T TARGET_FILE)

options:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        Single domain to scan
  -T TARGET_FILE, --target-file TARGET_FILE
                        File containing list of domains to scan
```

Example:

```crt.py -t example.com```
