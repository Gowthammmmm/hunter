from hunter.core import *
from hunter.localuseragent import *
import random
import json
import time


async def instagram(email, client, out):
    name = "instagram"
    domain = "instagram.com"
    method = "register"
    frequent_rate_limit = True

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'TE': 'trailers'
    }

    try:
        # Method 1: Try login endpoint
        try:
            login_data = {
                "username": email,
                "password": "Hunter123!@#",
                "queryParams": {},
                "optIntoOneTap": False
            }

            login_check = await client.post(
                'https://www.instagram.com/accounts/login/ajax/',
                headers=headers,
                json=login_data
            )

            if login_check.status_code == 429:
                out.append({
                    "name": name,
                    "domain": domain,
                    "method": method,
                    "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None
                })
                return

            try:
                login_response = login_check.json()
                if login_response.get("user") or login_response.get("authenticated"):
                    out.append({
                        "name": name,
                        "domain": domain,
                        "method": method,
                        "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": False,
                        "exists": True,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None
                    })
                    return
            except:
                pass
        except:
            pass

        # Method 2: Try registration endpoint
        try:
            register_data = {
                "email": email,
                "username": email.split('@')[0],
                "password": "Hunter123!@#",
                "first_name": "Hunter",
                "client_id": "",
                "seamless_login_enabled": "1"
            }

            register_check = await client.post(
                'https://www.instagram.com/accounts/web_create_ajax/',
                headers=headers,
                json=register_data
            )

            if register_check.status_code == 429:
                out.append({
                    "name": name,
                    "domain": domain,
                    "method": method,
                    "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None
                })
                return

            try:
                register_response = register_check.json()
                if "errors" in register_response:
                    if "email" in register_response["errors"]:
                        for error in register_response["errors"]["email"]:
                            if "taken" in error.lower():
                                out.append({
                                    "name": name,
                                    "domain": domain,
                                    "method": method,
                                    "frequent_rate_limit": frequent_rate_limit,
                                    "rateLimit": False,
                                    "exists": True,
                                    "emailrecovery": None,
                                    "phoneNumber": None,
                                    "others": None
                                })
                                return
            except:
                pass
        except:
            pass

        # Method 3: Try password reset endpoint
        try:
            reset_data = {
                "email_or_username": email,
                "recaptcha_challenge_field": ""
            }

            reset_check = await client.post(
                'https://www.instagram.com/accounts/account_recovery_send_ajax/',
                headers=headers,
                json=reset_data
            )

            if reset_check.status_code == 200:
                try:
                    reset_response = reset_check.json()
                    if reset_response.get("user_found"):
                        out.append({
                            "name": name,
                            "domain": domain,
                            "method": method,
                            "frequent_rate_limit": frequent_rate_limit,
                            "rateLimit": False,
                            "exists": True,
                            "emailrecovery": None,
                            "phoneNumber": None,
                            "others": None
                        })
                        return
                except:
                    pass
        except:
            pass

        # Method 4: Try username lookup
        try:
            username = email.split('@')[0]
            lookup_check = await client.get(
                f'https://www.instagram.com/{username}/',
                headers=headers
            )

            if lookup_check.status_code == 200:
                out.append({
                    "name": name,
                    "domain": domain,
                    "method": method,
                    "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": False,
                    "exists": True,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None
                })
                return
        except:
            pass

        # If we get here, no account was found
        out.append({
            "name": name,
            "domain": domain,
            "method": method,
            "frequent_rate_limit": frequent_rate_limit,
            "rateLimit": False,
            "exists": False,
            "emailrecovery": None,
            "phoneNumber": None,
            "others": None
        })

    except Exception as e:
        if "Too Many Requests" in str(e) or "429" in str(e):
            out.append({
                "name": name,
                "domain": domain,
                "method": method,
                "frequent_rate_limit": frequent_rate_limit,
                "rateLimit": True,
                "exists": False,
                "emailrecovery": None,
                "phoneNumber": None,
                "others": None
            })
        else:
            out.append({
                "name": name,
                "domain": domain,
                "method": method,
                "frequent_rate_limit": frequent_rate_limit,
                "rateLimit": False,
                "exists": False,
                "emailrecovery": None,
                "phoneNumber": None,
                "others": None
            })
