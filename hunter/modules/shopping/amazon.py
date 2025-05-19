from hunter.core import *
from hunter.localuseragent import *
import random
import json
import time
import asyncio
import re

async def amazon(email, client, out):
    name = "amazon"
    domain = "amazon.com"
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
        'Cache-Control': 'max-age=0',
        'TE': 'trailers'
    }

    try:
        # Add random delay between 1-3 seconds
        await asyncio.sleep(random.uniform(1, 3))

        # Method 1: Check account existence with password reset
        try:
            # First get the page to extract form parameters
            init_page = await client.get(
                'https://www.amazon.com/ap/forgotpassword',
                headers=headers,
                follow_redirects=True
            )
            
            # Extract CSRF token and other form data
            appActionToken = re.search(r'name="appActionToken" value="([^"]+)"', init_page.text)
            appAction = re.search(r'name="appAction" value="([^"]+)"', init_page.text)
            
            if appActionToken and appAction:
                reset_data = {
                    "email": email,
                    "appActionToken": appActionToken.group(1),
                    "appAction": appAction.group(1),
                    "forgotPasswordAction": "request_code"
                }

                reset_check = await client.post(
                    'https://www.amazon.com/ap/forgotpassword',
                    headers=headers,
                    data=reset_data,
                    follow_redirects=True
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

                # Successful password reset request suggests account exists
                if "verification code was sent" in reset_check.text.lower() or "confirmation code was sent" in reset_check.text.lower() or "an email has been sent" in reset_check.text.lower():
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
                # If we see a message about no account found
                elif "no account found" in reset_check.text.lower() or "we cannot find an account" in reset_check.text.lower():
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
            # First get the registration page to extract form parameters
            reg_page = await client.get(
                'https://www.amazon.com/ap/register?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3F_encoding%3DUTF8%26ref_%3Dnav_ya_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0',
                headers=headers,
                follow_redirects=True
            )
            
            # Extract CSRF token and other form data
            appActionToken = re.search(r'name="appActionToken" value="([^"]+)"', reg_page.text)
            workflowState = re.search(r'name="workflowState" value="([^"]+)"', reg_page.text)
            
            if appActionToken and workflowState:
                register_data = {
                    "customerName": "Hunter User",
                    "email": email,
                    "password": "Hunter123!@#",
                    "passwordCheck": "Hunter123!@#",
                    "appActionToken": appActionToken.group(1),
                    "workflowState": workflowState.group(1),
                    "create": "Create your Amazon account"
                }

                register_check = await client.post(
                    'https://www.amazon.com/ap/register',
                    headers=headers,
                    data=register_data,
                    follow_redirects=True
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

                # These strings indicate the email is already in use
                email_exists_indicators = [
                    "email-already-in-use",
                    "email-already-exists",
                    "account already exists",
                    "already exists with the email",
                    "already linked to another account",
                    "email address is already being used"
                ]
                
                if any(indicator in register_check.text.lower() for indicator in email_exists_indicators):
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

        # Method 3: Try login page
        try:
            # First get the signin page to extract form parameters
            signin_page = await client.get(
                'https://www.amazon.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3Fref_%3Dnav_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0',
                headers=headers,
                follow_redirects=True
            )
            
            # Extract CSRF token and other form data
            appActionToken = re.search(r'name="appActionToken" value="([^"]+)"', signin_page.text)
            workflowState = re.search(r'name="workflowState" value="([^"]+)"', signin_page.text)
            
            if appActionToken and workflowState:
                login_data = {
                    "email": email,
                    "password": "WrongPassword123!@#",
                    "appActionToken": appActionToken.group(1),
                    "workflowState": workflowState.group(1),
                    "signIn": "Sign in"
                }

                login_check = await client.post(
                    'https://www.amazon.com/ap/signin',
                    headers=headers,
                    data=login_data,
                    follow_redirects=True
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

                # These strings suggest the account exists (password error rather than account not found)
                account_exists_indicators = [
                    "incorrect password",
                    "password is incorrect",
                    "we will ask you to enter your password",
                    "authentication required",
                    "to authenticate your account",
                    "sign-in details are incorrect"
                ]
                
                # These indicate the account doesn't exist
                account_not_exists_indicators = [
                    "no account found",
                    "cannot find an account",
                    "we cannot find an account with that email"
                ]
                
                if any(indicator in login_check.text.lower() for indicator in account_exists_indicators):
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
                
                if any(indicator in login_check.text.lower() for indicator in account_not_exists_indicators):
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

        # If we reach here, we couldn't determine account status with confidence
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
