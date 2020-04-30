# cloudflare_ddnss
This script updates the DNS A and AAAA records of specified domains and subdomains for different DNS zones.

# Features
Aktualisiert festgelegte A und AAAA Tecords für verschiedene zonen

# Usage
Get Api Key via Cloudflare Dashbord.
* Cloudflare Dashboard
* My Profile - Account Home
* API Tokens - Global API Key

* Add API Key to accountss.json with your account Email

* Add your Zones with Domains in domains.json

# Schedule Script Execution

```
sudo crontab -e
```

Add new Line to the End
```
*/1 * * * * python3 /<path>/cloudfare_ddnss.py
```
