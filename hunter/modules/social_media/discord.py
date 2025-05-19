from hunter.core import *
from hunter.localuseragent import *
import random
import string
import json
import time


async def discord(email, client, out):
    name = "discord"
    domain = "discord.com"
    method = "register"
    frequent_rate_limit = True

    def get_random_string(length):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'Origin': 'https://discord.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://discord.com/register',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'TE': 'trailers'
    }

    try:
        # Method 1: Try password reset endpoint
        try:
            reset_data = {
                "email": email,
                "captcha_key": None,
                "captcha_rqtoken": None
            }
            
            reset_check = await client.post(
                'https://discord.com/api/v9/auth/forgot-password',
                headers=headers,
                json=reset_data
            )

            if reset_check.status_code == 200:
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

        # Method 2: Try login endpoint
        try:
            login_data = {
                "login": email,
                "password": get_random_string(20),
                "undelete": False,
                "captcha_key": None,
                "login_source": None,
                "gift_code_sku_id": None
            }

            login_check = await client.post(
                'https://discord.com/api/v9/auth/login',
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
                if "errors" in login_response:
                    if "login" in login_response["errors"]:
                        for error in login_response["errors"]["login"]["_errors"]:
                            if error.get("code") == "INVALID_LOGIN":
                                # Account exists but password is wrong
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

        # Method 3: Try registration endpoint
        try:
            register_data = {
                "fingerprint": "",
                "email": email,
                "username": get_random_string(20),
                "password": get_random_string(20),
                "invite": None,
                "consent": True,
                "date_of_birth": "",
                "gift_code_sku_id": None,
                "captcha_key": None
            }

            register_check = await client.post(
                'https://discord.com/api/v9/auth/register',
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
                        for error in register_response["errors"]["email"]["_errors"]:
                            if error.get("code") == "EMAIL_ALREADY_REGISTERED":
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
                f'https://discord.com/api/v9/users/{username}',
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
