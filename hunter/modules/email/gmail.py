from hunter.core import *
from hunter.localuseragent import *
import random
import json
import time
import asyncio

async def gmail(email, client, out):
    name = "gmail"
    domain = "gmail.com"
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
        # Add random delay between 1-3 seconds
        await asyncio.sleep(random.uniform(1, 3))

        # Method 1: Try login endpoint
        try:
            login_data = {
                "Email": email,
                "Passwd": "Hunter123!@#",
                "continue": "https://mail.google.com/mail/",
                "service": "mail"
            }

            login_check = await client.post(
                'https://accounts.google.com/ServiceLogin',
                headers=headers,
                data=login_data
            )

            if login_check.status_code == 429:
                # Add longer delay on rate limit
                await asyncio.sleep(random.uniform(5, 10))
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

            if "myaccount.google.com" in login_check.url or "accounts.google.com/signin/v2/challenge" in login_check.url:
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

        # Add random delay between 1-3 seconds
        await asyncio.sleep(random.uniform(1, 3))

        # Method 2: Try registration endpoint
        try:
            register_data = {
                "Email": email,
                "Passwd": "Hunter123!@#",
                "PasswdAgain": "Hunter123!@#",
                "service": "mail",
                "continue": "https://mail.google.com/mail/",
                "signup": "1"
            }

            register_check = await client.post(
                'https://accounts.google.com/SignUp',
                headers=headers,
                data=register_data
            )

            if register_check.status_code == 429:
                # Add longer delay on rate limit
                await asyncio.sleep(random.uniform(5, 10))
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

        # Add random delay between 1-3 seconds
        await asyncio.sleep(random.uniform(1, 3))

        # Method 3: Try password reset endpoint
        try:
            reset_data = {
                "Email": email,
                "continue": "https://accounts.google.com/signin/recovery"
            }

            reset_check = await client.post(
                'https://accounts.google.com/signin/v2/recoveryidentifier',
                headers=headers,
                data=reset_data
            )

            if reset_check.status_code == 429:
                # Add longer delay on rate limit
                await asyncio.sleep(random.uniform(5, 10))
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

        # Add random delay between 1-3 seconds
        await asyncio.sleep(random.uniform(1, 3))

        # Method 4: Try username lookup
        try:
            username = email.split('@')[0]
            lookup_check = await client.get(
                f'https://mail.google.com/mail/gxlu?email={username}',
                headers=headers
            )

            if lookup_check.status_code == 429:
                # Add longer delay on rate limit
                await asyncio.sleep(random.uniform(5, 10))
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