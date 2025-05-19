from hunter.core import *
from hunter.localuseragent import *
import random
import re
import json
import asyncio


async def pinterest(email, client, out):
    name = "pinterest"
    domain = "pinterest.com"
    method = "register"
    frequent_rate_limit = True

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://www.pinterest.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://www.pinterest.com/signup',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Cache-Control': 'max-age=0',
    }

    try:
        # Add random delay to avoid rate limiting
        await asyncio.sleep(random.uniform(1, 2))
        
        # Method 1: Check email availability via signup
        try:
            # Get initial page and extract CSRF token
            response = await client.get(
                "https://www.pinterest.com/signup",
                headers=headers,
                follow_redirects=True
            )
            
            if response.status_code != 200:
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

            # Extract CSRF token using different regex patterns
            csrf_match = re.search(r'name="csrf_token" value="([^"]+)"', response.text)
            if not csrf_match:
                csrf_match = re.search(r'"csrfToken":"([^"]+)"', response.text)
                
            if not csrf_match:
                csrf_match = re.search(r'csrf_token = "([^"]+)"', response.text)
                
            if csrf_match:
                token = csrf_match.group(1)
                headers["X-CSRFToken"] = token
                
                # Check email availability
                check = await client.post(
                    "https://www.pinterest.com/_api/resource/EmailExistsResource/get/",
                    params={
                        "source_url": "/signup/",
                        "data": json.dumps({
                            "options": {
                                "email": email
                            }
                        })
                    },
                    headers=headers
                )
                
                if check.status_code == 429:
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

                if check.status_code == 200:
                    try:
                        response_data = check.json()
                        if "resource_response" in response_data:
                            exists = response_data["resource_response"].get("data", {}).get("exists", False)
                            if exists:
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
                return
            # Continue to next method if this one fails
            pass
        
        # Add random delay between methods
        await asyncio.sleep(random.uniform(1, 2))
        
        # Method 2: Try login with email
        try:
            login_page = await client.get(
                "https://www.pinterest.com/login/",
                headers={
                    'User-Agent': random.choice(ua["browsers"]["chrome"]),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Referer': 'https://www.pinterest.com/',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                },
                follow_redirects=True
            )
            
            if login_page.status_code == 200:
                # Extract CSRF token
                csrf_match = re.search(r'name="csrf_token" value="([^"]+)"', login_page.text)
                if not csrf_match:
                    csrf_match = re.search(r'"csrfToken":"([^"]+)"', login_page.text)
                    
                if not csrf_match:
                    csrf_match = re.search(r'csrf_token = "([^"]+)"', login_page.text)
                    
                if csrf_match:
                    token = csrf_match.group(1)
                    
                    # Try login with email to check if it exists
                    login_headers = headers.copy()
                    login_headers['Content-Type'] = 'application/x-www-form-urlencoded'
                    login_headers['X-CSRFToken'] = token
                    
                    login_data = {
                        'email': email,
                        'password': 'WrongPassword123!',
                        'csrf_token': token
                    }
                    
                    login_response = await client.post(
                        "https://www.pinterest.com/resource/UserSessionResource/create/",
                        headers=login_headers,
                        params={
                            "source_url": "/login/",
                            "data": json.dumps({
                                "options": {
                                    "username_or_email": email,
                                    "password": "WrongPassword123!"
                                }
                            })
                        }
                    )
                    
                    if login_response.status_code == 429:
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
                    
                    if login_response.status_code == 200:
                        try:
                            response_data = login_response.json()
                            # Check response for indicators that account exists
                            if "resource_response" in response_data:
                                error = response_data["resource_response"].get("error", {})
                                message = error.get("message", "").lower()
                                
                                # These error messages indicate the email exists but password is wrong
                                if "password" in message and "incorrect" in message:
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
                                
                                # These indicate the email doesn't exist
                                if "email" in message and "find" in message:
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
                        except:
                            pass
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
                return
            # Continue to next method if this one fails
            pass
        
        # Add random delay between methods
        await asyncio.sleep(random.uniform(1, 2))
        
        # Method 3: Try password reset
        try:
            reset_url = "https://www.pinterest.com/password/reset/"
            reset_page = await client.get(
                reset_url,
                headers={
                    'User-Agent': random.choice(ua["browsers"]["chrome"]),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Referer': 'https://www.pinterest.com/login/',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                },
                follow_redirects=True
            )
            
            if reset_page.status_code == 200:
                # Extract CSRF token
                csrf_match = re.search(r'name="csrf_token" value="([^"]+)"', reset_page.text)
                if not csrf_match:
                    csrf_match = re.search(r'"csrfToken":"([^"]+)"', reset_page.text)
                    
                if not csrf_match:
                    csrf_match = re.search(r'csrf_token = "([^"]+)"', reset_page.text)
                    
                if csrf_match:
                    token = csrf_match.group(1)
                    
                    # Try password reset to check if account exists
                    reset_headers = headers.copy()
                    reset_headers['Content-Type'] = 'application/json'
                    reset_headers['X-CSRFToken'] = token
                    
                    reset_response = await client.post(
                        "https://www.pinterest.com/resource/UserResetPasswordResource/create/",
                        headers=reset_headers,
                        params={
                            "source_url": "/password/reset/",
                            "data": json.dumps({
                                "options": {
                                    "email": email
                                }
                            })
                        }
                    )
                    
                    if reset_response.status_code == 429:
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
                    
                    if reset_response.status_code == 200:
                        try:
                            response_data = reset_response.json()
                            
                            # Success message indicates email was found and reset email sent
                            if "resource_response" in response_data:
                                # If reset was successful, account exists
                                if response_data["resource_response"].get("status") == "success":
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
                                
                                # Error message indicates email not found
                                error = response_data["resource_response"].get("error", {})
                                message = error.get("message", "").lower()
                                if "email" in message and ("not found" in message or "doesn't exist" in message):
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
                        except:
                            pass
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
                return
            # Continue if this method fails
            pass
        
        # If we've tried all methods and can't confirm, default to not found
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
