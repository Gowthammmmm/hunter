from hunter.core import *
from hunter.localuseragent import *
import random
import json
import time

async def facebook(email, client, out):
    name = "facebook"
    domain = "facebook.com"
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
                "email": email,
                "pass": "Hunter123!@#",
                "login": "Log In"
            }

            login_check = await client.post(
                'https://www.facebook.com/login/device-based/regular/login/',
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

            if "checkpoint" in login_check.url or "login/save-device" in login_check.url:
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
                "reg_email": email,
                "reg_pass": "Hunter123!@#",
                "reg_pass_confirmation": "Hunter123!@#",
                "reg_submit": "Sign Up"
            }

            register_check = await client.post(
                'https://www.facebook.com/',
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

            if "email_already_registered" in register_check.text.lower():
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
                "email": email,
                "did_submit": "1"
            }

            reset_check = await client.post(
                'https://www.facebook.com/recover/initiate/',
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

            if "email_sent" in reset_check.text.lower() or "recovery_email_sent" in reset_check.text.lower():
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
                f'https://www.facebook.com/{username}',
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
