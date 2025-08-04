import browser_cookie3

import sys

if len(sys.argv) < 2:
    print("Usage: python extract_chrome_cookies.py DOMAIN_NAME")
    sys.exit(1)

DOMAIN = sys.argv[1]

cj = browser_cookie3.chrome(domain_name=DOMAIN)

with open(f'AppData/Cookies/{DOMAIN}.txt', 'w', encoding='utf-8') as f:
	f.write("# Netscape HTTP Cookie File\n")
	f.write("# https://curl.haxx.se/rfc/cookie_spec.html\n\n")

	for cookie in cj:
		domain_flag = 'TRUE' if cookie.domain.startswith('.') else 'FALSE'
		secure_flag = 'TRUE' if cookie.secure else 'FALSE'
		expires = str(cookie.expires) if cookie.expires else '0'

		line = (
			f"{cookie.domain}\t"
			f"{domain_flag}\t"
			f"{cookie.path}\t"
			f"{secure_flag}\t"
			f"{expires}\t"
			f"{cookie.name}\t"
			f"{cookie.value}\n"
		)

		f.write(line)

print("cookies.txt updated!")