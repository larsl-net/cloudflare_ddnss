# Cloudflare ddnss
This script updates the DNS A and AAAA records of specified domains and subdomains for different DNS zones and different Accounts.

# Features
Updates specified A and AAAA records for different zones


# Usage

## With API Token (recommended)

* Create API Token via the Cloudflare Dashborad.
* Required permissions Zone read and DNs edit for all zones with domains to be updated.

* Enter the Token in domains.json (config -> token, email and key not requiered)
* Set "token_mode": true

Enter your Domains under zones with sub entry for the zone in ther the Doamin is.
```json
{
	"Demo Auth": {
		"config": {
			"token": "<your-api-token>",
			"token_mode": true
		},
		"zones": {
			"example.com": {
				"0": "example.com",
				"1": "www.example.com"
			},
			"example.de": {
				"0": "example.de",
				"1": "www.example.de"
			}
		}
	},
	"Demo Auth 2": {
		"config": {
			"token": "<other-api-token>",
			"token_mode": true
		},
		"zones": {
			"example.us": {
				"0": "example.com",
				"1": "www.example.com"
			},
			"example.gb": {
				"0": "example.de",
				"1": "www.example.de"
			}
		}
	}
}
```


## With Global API Key
Get Api Key via Cloudflare Dashbord.
* Cloudflare Dashboard
* My Profile - Account Home
* API Tokens - Global API Key
* Add API Key to domains.json (config -> key , email is requiered, token is not requiered)
* Set "token_mode": false

Enter your Domains under zones with sub entry for the zone in ther the Doamin is.
```json
{
	"Demo Auth": {
		"config": {
			"email": "<your-email-adress>",
			"key": "<your-global-api-key>",
			"token_mode": false
		},
		"zones": {
			"example.com": {
				"0": "example.com",
				"1": "www.example.com"
			},
			"example.de": {
				"0": "example.de",
				"1": "www.example.de"
			}
		}
	},
	"Demo Auth 2": {
		"config": {
			"email": "<other-email-adress>",
			"key": "<other-global-api-key>",
			"token_mode": false
		},
		"zones": {
			"example.us": {
				"0": "example.com",
				"1": "www.example.com"
			},
			"example.gb": {
				"0": "example.de",
				"1": "www.example.de"
			}
		}
	}
}
```


## Mixed Mode Example
```json
{
	"Demo Auth": {
		"config": {
			"token": "<your-api-token>",
			"token_mode": true
		},
		"zones": {
			"example.com": {
				"0": "example.com",
				"1": "www.example.com"
			},
			"example.de": {
				"0": "example.de",
				"1": "www.example.de"
			}
		}
	},
	"Demo Auth 2": {
		"config": {
			"email": "<other-email-adress>",
			"key": "<other-global-api-key>",
			"token_mode": false
		},
		"zones": {
			"example.us": {
				"0": "example.com",
				"1": "www.example.com"
			},
			"example.gb": {
				"0": "example.de",
				"1": "www.example.de"
			}
		}
	}
}
```
# Options

You can set preferences for each auth block and record.

* To set TTL you must add
```
"ttl": <time>
```
(default: 1 = auto)

* To set Proxy you must add
```
"proxied": true or false
```
(default: true)

* To set IPv4 you must add
```
"ip4": true or false
```
(default: true)

* To set IPv6 you must add
```
"ip6": true or false
```
(default: true)

* To set Force Settings update to Cloudflare you must add
```
"foce_settingsip6": true or false
```
(default: true)


to the config section or to the record in the domains.json file

*If several records with the same name exist, the record id can be passed in the record entry.
```
"record4_id": "<Record-IPv4-ID>",
"record6_id": "<Record-IPv6-ID>"
```


# Schedule Script Execution

```
sudo crontab -e
```

Add new Line to the End
```
*/1 * * * * python3 /<path>/cloudfare_ddnss.py
```
