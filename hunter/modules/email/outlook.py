from hunter.core import *
from hunter.localuseragent import *
import random
import json
import time

async def outlook(email, client, out):
    name = "outlook"
    domain = "outlook.com"
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
                "login": email,
                "passwd": "Hunter123!@#",
                "type": "11"
            }

            login_check = await client.post(
                'https://login.live.com/ppsecure/post.srf',
                headers=headers,
                data=login_data
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

            if "account.live.com" in login_check.url or "login.live.com/ppsecure/post.srf" in login_check.url:
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

        # Method 2: Try registration endpoint
        try:
            register_data = {
                "signup": "1",
                "login": email,
                "passwd": "Hunter123!@#",
                "passwd2": "Hunter123!@#",
                "type": "11"
            }

            register_check = await client.post(
                'https://signup.live.com/signup',
                headers=headers,
                data=register_data
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

            if "email_already_exists" in register_check.text.lower() or "email_already_taken" in register_check.text.lower():
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

        # Method 3: Try password reset endpoint
        try:
            reset_data = {
                "login": email,
                "type": "11"
            }

            reset_check = await client.post(
                'https://account.live.com/resetpassword',
                headers=headers,
                data=reset_data
            )

            if reset_check.status_code == 429:
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

            if "recovery_email_sent" in reset_check.text.lower() or "recovery_identifier_sent" in reset_check.text.lower():
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

        # Method 4: Try username lookup
        try:
            username = email.split('@')[0]
            lookup_check = await client.get(
                f'https://login.live.com/GetCredentialType.srf?opid=4B7C0A0A-0A0A-0A0A-0A0A-0A0A0A0A0A0A&mkt=EN-US&lc=1033&username={username}',
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