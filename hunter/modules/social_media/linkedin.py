from hunter.core import *
from hunter.localuseragent import *
import random
import re
import json
import asyncio

async def linkedin(email, client, out):
    name = "linkedin"
    domain = "linkedin.com"
    method = "register"
    frequent_rate_limit = True

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://www.linkedin.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://www.linkedin.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Cache-Control': 'max-age=0',
        'TE': 'trailers'
    }

    try:
        # Add a small random delay to avoid rate limiting
        await asyncio.sleep(random.uniform(1, 2))
        
        # Method 1: Try login page with email to check if recognized
        try:
            # Get login page to extract CSRF token and other parameters
            login_page = await client.get(
                "https://www.linkedin.com/login",
                headers={
                    'User-Agent': random.choice(ua["browsers"]["chrome"]),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Referer': 'https://www.linkedin.com/',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                },
                follow_redirects=True
            )
            
            if login_page.status_code != 200:
                # Rate limited or connection issue
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

            # Extract CSRF token and other parameters using regex
            csrf_param = re.search(r'name="csrfToken" value="([^"]+)"', login_page.text)
            csrf_token = None
            if csrf_param:
                csrf_token = csrf_param.group(1)
            else:
                # Try alternative method to find CSRF token
                csrf_match = re.search(r'"csrfToken":"([^"]+)"', login_page.text)
                if csrf_match:
                    csrf_token = csrf_match.group(1)
                
            if csrf_token:
                login_headers = headers.copy()
                login_headers['Content-Type'] = 'application/x-www-form-urlencoded'
                
                login_data = {
                    'session_key': email,
                    'session_password': 'WrongPassword123',  # Using a wrong password to check if account exists
                    'csrfToken': csrf_token,
                    'loginCsrfParam': csrf_token
                }

                login_response = await client.post(
                    "https://www.linkedin.com/login-submit",
                    headers=login_headers,
                    data=login_data,
                    follow_redirects=True
                )
                
                if login_response.status_code == 429:
                    # Rate limited
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
                
                # Check response for indicators that the account exists
                if "incorrect password" in login_response.text.lower() or "please enter your password" in login_response.text.lower() or "we didn't recognize that password" in login_response.text.lower() or "that's not the right password" in login_response.text.lower():
                    # Password is wrong, but email is recognized - account exists
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
                
                # Check if email not recognized
                if "we don't recognize that email" in login_response.text.lower() or "we couldn't find that email" in login_response.text.lower() or "couldn't find a linkedin account associated with this email" in login_response.text.lower():
                    # Email not recognized - account doesn't exist
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
            
        # Add a small random delay between methods
        await asyncio.sleep(random.uniform(1, 2))
        
        # Method 2: Try password reset to check if account exists
        try:
            # Get forgot password page
            reset_page = await client.get(
                "https://www.linkedin.com/uas/request-password-reset",
                headers={
                    'User-Agent': random.choice(ua["browsers"]["chrome"]),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                },
                follow_redirects=True
            )
            
            if reset_page.status_code != 200:
                # Rate limited or connection issue
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
                
            # Extract CSRF token and other parameters using regex
            csrf_param = re.search(r'name="csrfToken" value="([^"]+)"', reset_page.text)
            csrf_token = None
            if csrf_param:
                csrf_token = csrf_param.group(1)
            else:
                # Try alternative method to find CSRF token
                csrf_match = re.search(r'"csrfToken":"([^"]+)"', reset_page.text)
                if csrf_match:
                    csrf_token = csrf_match.group(1)
                
            if csrf_token:
                reset_headers = headers.copy()
                reset_headers['Content-Type'] = 'application/x-www-form-urlencoded'
                
                reset_data = {
                    'email': email,
                    'csrfToken': csrf_token,
                }

                reset_response = await client.post(
                    "https://www.linkedin.com/uas/request-password-reset-submit",
                    headers=reset_headers,
                    data=reset_data,
                    follow_redirects=True
                )
                
                if reset_response.status_code == 429:
                    # Rate limited
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
                
                # Check response for indicators that the account exists
                account_exists_indicators = [
                    "password reset link has been sent",
                    "we've sent a link to reset your password",
                    "check your email inbox",
                    "reset password email was sent",
                    "we've sent a one-time link to your email",
                    "please check your mail for reset instructions"
                ]
                
                # Indicators that account doesn't exist
                account_not_exists_indicators = [
                    "couldn't find that email address",
                    "we couldn't find that email",
                    "we don't recognize that email",
                    "no account with that email"
                ]
                
                if any(indicator in reset_response.text.lower() for indicator in account_exists_indicators):
                    # Reset email was sent - account exists
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
                    
                if any(indicator in reset_response.text.lower() for indicator in account_not_exists_indicators):
                    # Account doesn't exist
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
            
        # Add a small random delay between methods
        await asyncio.sleep(random.uniform(1, 2))
        
        # Method 3: Try signup to check if email already used
        try:
            # Get signup page
            signup_page = await client.get(
                "https://www.linkedin.com/signup",
                headers={
                    'User-Agent': random.choice(ua["browsers"]["chrome"]),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                },
                follow_redirects=True
            )
            
            if signup_page.status_code != 200:
                # Rate limited or connection issue
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
                
            # Extract CSRF token using regex
            csrf_param = re.search(r'name="csrfToken" value="([^"]+)"', signup_page.text)
            csrf_token = None
            if csrf_param:
                csrf_token = csrf_param.group(1)
            else:
                # Try alternative method to find CSRF token
                csrf_match = re.search(r'"csrfToken":"([^"]+)"', signup_page.text)
                if csrf_match:
                    csrf_token = csrf_match.group(1)
                    
            if csrf_token:
                # Check if email is available during signup
                check_headers = headers.copy()
                check_headers['Content-Type'] = 'application/json'
                check_headers['X-Li-Track'] = '{"clientVersion":""}' 
                check_headers['X-RestLi-Protocol-Version'] = '2.0.0'
                
                check_data = {
                    "email": email,
                    "csrfToken": csrf_token
                }
                
                check_response = await client.post(
                    "https://www.linkedin.com/checkpoint/api/email-validation",
                    headers=check_headers,
                    json=check_data
                )
                
                if check_response.status_code == 429:
                    # Rate limited
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
                
                if check_response.status_code == 200:
                    try:
                        response_data = check_response.json()
                        
                        # Check if email exists based on validation response
                        if response_data.get("emailIsExist") == True or "existing member" in str(response_data).lower() or "already have an account" in str(response_data).lower():
                            # Email exists
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
                        elif "valid" in str(response_data).lower() and "existing" not in str(response_data).lower():
                            # Email is valid but doesn't exist
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
                        # Continue to next method if JSON parsing fails
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
        
        # If we've tried all methods and can't confirm, default to "doesn't exist"
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