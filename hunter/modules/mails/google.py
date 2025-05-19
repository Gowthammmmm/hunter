from hunter.core import *
from hunter.localuseragent import *
import random
import json
import time
import asyncio
import re


async def google(email, client, out):
    name = "google"
    domain = "google.com"
    method= "register"
    frequent_rate_limit=False

    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': '*/*',
        'Accept-Language': 'en,en-US;q=0.5',
        'X-Same-Domain': '1',
        'Google-Accounts-XSRF': '1',
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
        'Origin': 'https://accounts.google.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://accounts.google.com/signup/v2/webcreateaccount?continue=https%3A%2F%2Faccounts.google.com%2F&gmb=exp&biz=false&flowName=GlifWebSignIn&flowEntry=SignUp',
        'TE': 'Trailers',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Cache-Control': 'max-age=0',
    }

    try:
        # Add random delay to avoid rate limiting
        await asyncio.sleep(random.uniform(1, 2))

        # Method 1: The original username availability check
        try:
            req = await client.get(
                "https://accounts.google.com/signup/v2/webcreateaccount?continue=https%3A%2F%2Faccounts.google.com%2FManageAccount%3Fnc%3D1&gmb=exp&biz=false&flowName=GlifWebSignIn&flowEntry=SignUp",
                headers=headers,
                follow_redirects=True)

            # Try to extract the request parameter
            try:
                freq = req.text.split('quot;,null,null,null,&quot;')[1].split('&quot')[0]
            except Exception:
                # Try alternate patterns
                freq_match = re.search(r'"[0-9a-zA-Z_-]{40,}"', req.text)
                if freq_match:
                    freq = freq_match.group(0).strip('"')
                else:
                    # One more attempt with a broader pattern
                    freq_match = re.search(r'"([0-9a-zA-Z_-]{20,})"', req.text)
                    if freq_match:
                        freq = freq_match.group(1)
                    else:
                        # If we can't find the parameter, try the second method
                        raise Exception("Couldn't extract request parameter")

            params = {
                'hl': 'en',
                'rt': 'j',
            }

            data = {
                'continue': 'https://accounts.google.com/',
                'dsh': '',
                'hl': 'en',
                'f.req': '["' + freq + '","","","' + email + '",false]',
                'azt': '',
                'cookiesDisabled': 'false',
                'deviceinfo': '[null,null,null,[],null,"US",null,null,[],"GlifWebSignIn",null,[null,null,[],null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,[],null,null,null,[],[]],null,null,null,null,0,null,false]',
                'gmscoreversion': 'unined',
                '': ''
            }

            response = await client.post('https://accounts.google.com/_/signup/webusernameavailability',
                                       headers=headers,
                                       params=params,
                                       data=data)

            if '"gf.wuar",2' in response.text or "That username is taken" in response.text:
                out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                            "rateLimit": False,
                            "exists": True,
                            "emailrecovery": None,
                            "phoneNumber": None,
                            "others": None})
                return
            elif '"gf.wuar",1' in response.text or "EmailInvalid" in response.text:
                # Continue to next method for confirmation
                pass
            elif "429" in str(response.status_code):
                out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                            "rateLimit": True,
                            "exists": False,
                            "emailrecovery": None,
                            "phoneNumber": None,
                            "others": None})
                return
        except Exception as e:
            # If method 1 fails, continue to method 2
            if "Too Many Requests" in str(e) or "429" in str(e):
                out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                            "rateLimit": True,
                            "exists": False,
                            "emailrecovery": None,
                            "phoneNumber": None,
                            "others": None})
                return
            pass

        # Add random delay between methods
        await asyncio.sleep(random.uniform(1, 2))

        # Method 2: Try recovery flow to check if account exists
        try:
            # First get the page to extract parameters
            recovery_page = await client.get(
                "https://accounts.google.com/signin/v2/identifier?flowName=GlifWebSignIn&flowEntry=ServiceLogin",
                headers={
                    'User-Agent': random.choice(ua["browsers"]["chrome"]),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Referer': 'https://www.google.com/',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                },
                follow_redirects=True
            )

            # Extract parameters
            gxf_match = re.search(r'name="gxf" value="([^"]+)"', recovery_page.text)
            if gxf_match:
                gxf = gxf_match.group(1)

                # Now attempt a login with the email
                login_data = {
                    'identifier': email,
                    'identifierInput': email,
                    'flowName': 'GlifWebSignIn',
                    'flowEntry': 'ServiceLogin',
                    'gxf': gxf,
                }

                check_response = await client.post(
                    "https://accounts.google.com/signin/v2/identifier",
                    headers={
                        'User-Agent': random.choice(ua["browsers"]["chrome"]),
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'Origin': 'https://accounts.google.com',
                        'Referer': 'https://accounts.google.com/signin/v2/identifier?flowName=GlifWebSignIn&flowEntry=ServiceLogin',
                        'Connection': 'keep-alive',
                        'Upgrade-Insecure-Requests': '1',
                    },
                    data=login_data,
                    follow_redirects=True
                )

                # Check if we're asked for password (account exists) or if we get invalid email error
                if "password" in check_response.text.lower() or "Enter your password" in check_response.text or "Wrong password" in check_response.text:
                    # Account exists - Google is asking for password
                    out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                                "rateLimit": False,
                                "exists": True,
                                "emailrecovery": None,
                                "phoneNumber": None,
                                "others": None})
                    return
                elif "couldn't find your google account" in check_response.text.lower() or "couldn't find your account" in check_response.text.lower():
                    out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                                "rateLimit": False,
                                "exists": False,
                                "emailrecovery": None,
                                "phoneNumber": None,
                                "others": None})
                    return
        except Exception as e:
            if "Too Many Requests" in str(e) or "429" in str(e):
                out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                            "rateLimit": True,
                            "exists": False,
                            "emailrecovery": None,
                            "phoneNumber": None,
                            "others": None})
                return
            pass

        # Add random delay between methods
        await asyncio.sleep(random.uniform(1, 2))

        # Method 3: Try password recovery to check if account exists
        try:
            recovery_init = await client.get(
                "https://accounts.google.com/signin/v2/recoveryidentifier",
                headers={
                    'User-Agent': random.choice(ua["browsers"]["chrome"]),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Referer': 'https://www.google.com/',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                },
                follow_redirects=True
            )

            # Extract parameters
            gxf_match = re.search(r'name="gxf" value="([^"]+)"', recovery_init.text)
            if gxf_match:
                gxf = gxf_match.group(1)

                # Submit recovery request
                recovery_data = {
                    'email': email,
                    'flowName': 'GlifWebSignIn',
                    'flowEntry': 'ServiceLogin',
                    'gxf': gxf,
                }

                recovery_response = await client.post(
                    "https://accounts.google.com/signin/v2/recoveryidentifier",
                    headers={
                        'User-Agent': random.choice(ua["browsers"]["chrome"]),
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'Origin': 'https://accounts.google.com',
                        'Referer': 'https://accounts.google.com/signin/v2/recoveryidentifier',
                        'Connection': 'keep-alive',
                        'Upgrade-Insecure-Requests': '1',
                    },
                    data=recovery_data,
                    follow_redirects=True
                )

                if "account recovery" in recovery_response.text.lower() or "recover your account" in recovery_response.text.lower():
                    # Google is offering account recovery options
                    out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                                "rateLimit": False,
                                "exists": True,
                                "emailrecovery": None,
                                "phoneNumber": None,
                                "others": None})
                    return
                elif "couldn't find your google account" in recovery_response.text.lower() or "couldn't find your account" in recovery_response.text.lower():
                    out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                                "rateLimit": False,
                                "exists": False,
                                "emailrecovery": None,
                                "phoneNumber": None,
                                "others": None})
                    return
        except Exception as e:
            if "Too Many Requests" in str(e) or "429" in str(e):
                out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                            "rateLimit": True,
                            "exists": False,
                            "emailrecovery": None,
                            "phoneNumber": None,
                            "others": None})
                return
            pass

        # If we've tried all methods and can't confirm, default to not found
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": False,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})

    except Exception as e:
        if "Too Many Requests" in str(e) or "429" in str(e):
            out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": True,
                        "exists": False,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
        else:
            out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": False,
                        "exists": False,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
