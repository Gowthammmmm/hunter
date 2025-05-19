from hunter.core import *
from hunter.localuseragent import *
import random
import json
import time
import asyncio

async def adobe(email, client, out):
    name = "adobe"
    domain = "adobe.com"
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
                "username": email,
                "password": "Hunter123!@#",
                "rememberMe": "true"
            }

            login_check = await client.post(
                'https://auth.services.adobe.com/signin/v2',
                headers=headers,
                json=login_data
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
            except json.JSONDecodeError:
                # If response is not JSON, check text content
                if "password" in login_check.text.lower() or "enter your password" in login_check.text.lower():
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
        except Exception as e:
            if "Too Many Requests" in str(e) or "429" in str(e):
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
            pass

        # Add random delay between 1-3 seconds
        await asyncio.sleep(random.uniform(1, 3))

        # Method 2: Try registration endpoint
        try:
            register_data = {
                "email": email,
                "password": "Hunter123!@#",
                "firstName": "Hunter",
                "lastName": "User"
            }

            register_check = await client.post(
                'https://auth.services.adobe.com/signup/v2',
                headers=headers,
                json=register_data
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

            try:
                register_response = register_check.json()
                if "email_already_exists" in str(register_response).lower() or "email_already_taken" in str(register_response).lower():
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
            except json.JSONDecodeError:
                # If response is not JSON, check text content
                if "email already exists" in register_check.text.lower() or "email already taken" in register_check.text.lower():
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
        except Exception as e:
            if "Too Many Requests" in str(e) or "429" in str(e):
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
            pass

        # Add random delay between 1-3 seconds
        await asyncio.sleep(random.uniform(1, 3))

        # Method 3: Try password reset endpoint
        try:
            reset_data = {
                "email": email
            }

            reset_check = await client.post(
                'https://auth.services.adobe.com/reset-password/v2',
                headers=headers,
                json=reset_data
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

            try:
                reset_response = reset_check.json()
                if reset_response.get("email_sent") or reset_response.get("recovery_email_sent"):
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
            except json.JSONDecodeError:
                # If response is not JSON, check text content
                if "email sent" in reset_check.text.lower() or "recovery email sent" in reset_check.text.lower():
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
        except Exception as e:
            if "Too Many Requests" in str(e) or "429" in str(e):
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
            pass

        # Add random delay between 1-3 seconds
        await asyncio.sleep(random.uniform(1, 3))

        # Method 4: Try profile lookup
        try:
            username = email.split('@')[0]
            lookup_check = await client.get(
                f'https://profile.adobe.com/{username}',
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
        except Exception as e:
            if "Too Many Requests" in str(e) or "429" in str(e):
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