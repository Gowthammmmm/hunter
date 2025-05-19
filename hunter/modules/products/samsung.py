from hunter.core import *
from hunter.localuseragent import *
import random
import re
import json
import asyncio


async def samsung(email, client, out):
    name = "samsung"
    domain = "samsung.com"
    method = "password recovery"
    frequent_rate_limit = True

    try:
        # Add random delay to avoid rate limiting
        await asyncio.sleep(random.uniform(1, 2))
        
        # Method 1: Check if email exists using signup flow
        try:
            # Get the initial signup page to extract tokens
            signup_headers = {
                'User-Agent': random.choice(ua["browsers"]["chrome"]),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Referer': 'https://account.samsung.com/',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'max-age=0',
            }
            
            req = await client.get(
                "https://account.samsung.com/accounts/v1/Samsung_com_US/signUp",
                headers=signup_headers,
                follow_redirects=True
            )
            
            if req.status_code != 200:
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
                
            # Extract tokens using regex for better reliability
            session_token = None
            csrf_token = None
            
            # Try different methods to extract session token
            session_match = re.search(r'sJSESSIONID["\']?\s*[":=]\s*["\']([^"\']+)["\']', req.text)
            if session_match:
                session_token = session_match.group(1)
                
            # Try different methods to extract CSRF token
            csrf_match = re.search(r'token["\']?\s*[":=]\s*["\']([^"\']+)["\']', req.text)
            if csrf_match:
                csrf_token = csrf_match.group(1)
                
            if session_token and csrf_token:
                cookies = {
                    'EUAWSIAMSESSIONID': session_token,
                }

                headers = {
                    'User-Agent': random.choice(ua["browsers"]["chrome"]),
                    'Accept': 'application/json, text/plain, */*',
                    'Accept-Language': 'en,en-US;q=0.5',
                    'Referer': 'https://account.samsung.com/accounts/v1/Samsung_com_US/signUp',
                    'Content-Type': 'application/json; charset=UTF-8',
                    'X-CSRF-TOKEN': csrf_token,
                    'Origin': 'https://account.samsung.com',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                }

                params = {
                    'v': random.randrange(1000, 9999),
                }

                data = json.dumps({"emailID": email})

                response = await client.post(
                    'https://account.samsung.com/accounts/v1/Samsung_com_US/signUpCheckEmailIDProc',
                    headers=headers,
                    params=params,
                    cookies=cookies,
                    data=data
                )

                if response.status_code == 429:
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
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        
                        # Check response to determine if email exists
                        if "rtnCd" in data and "success" in str(data.get("rtnCd")).lower():
                            # If success, email is available (doesn't exist)
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
                            
                        # Specific error codes that indicate email exists
                        if "rtnCd" in data and data.get("rtnCd") in ["FAIL_ALREADY_EXIST_ID", "ALREADY_EXIST_ID", "ALREADY_REG_USER"]:
                            # Email already exists
                            phone_number = await get_phone_number(email, client, cookies, headers)
                            out.append({
                                "name": name,
                                "domain": domain,
                                "method": method,
                                "frequent_rate_limit": frequent_rate_limit,
                                "rateLimit": False,
                                "exists": True,
                                "emailrecovery": None,
                                "phoneNumber": phone_number,
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
        
        # Method 2: Try password reset flow
        try:
            # Get the password reset page
            reset_headers = {
                'User-Agent': random.choice(ua["browsers"]["chrome"]),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Referer': 'https://account.samsung.com/',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            
            reset_page = await client.get(
                "https://account.samsung.com/accounts/v1/Samsung_com_US/resetPassword",
                headers=reset_headers,
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
            
            # Extract tokens for the reset password request
            session_match = re.search(r'sJSESSIONID["\']?\s*[":=]\s*["\']([^"\']+)["\']', reset_page.text)
            csrf_match = re.search(r'token["\']?\s*[":=]\s*["\']([^"\']+)["\']', reset_page.text)
            
            if session_match and csrf_match:
                session_token = session_match.group(1)
                csrf_token = csrf_match.group(1)
                
                cookies = {
                    'EUAWSIAMSESSIONID': session_token,
                }

                headers = {
                    'User-Agent': random.choice(ua["browsers"]["chrome"]),
                    'Accept': 'application/json, text/plain, */*',
                    'Accept-Language': 'en,en-US;q=0.5',
                    'Referer': 'https://account.samsung.com/accounts/v1/Samsung_com_US/resetPassword',
                    'Content-Type': 'application/json; charset=UTF-8',
                    'X-CSRF-TOKEN': csrf_token,
                    'Origin': 'https://account.samsung.com',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                }
                
                params = {
                    'v': random.randrange(1000, 9999),
                }
                
                reset_data = json.dumps({
                    "signUpID": email,
                    "signUpIDType": "003"  # Email type
                })
                
                reset_response = await client.post(
                    'https://account.samsung.com/accounts/v1/Samsung_com_US/resetPasswordProc',
                    headers=headers,
                    params=params,
                    cookies=cookies,
                    data=reset_data
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
                
                if reset_response.status_code == 200:
                    try:
                        data = reset_response.json()
                        
                        # Check return code
                        if data.get("rtnCd") == "NEXT" or data.get("rtnCd") == "SUCCESS":
                            # Password reset initiated, account exists
                            phone_number = None
                            if "nextURL" in data:
                                # Get the full URL for the next step
                                next_url = "https://account.samsung.com" + data["nextURL"]
                                req = await client.get(next_url, headers=headers, cookies=cookies)
                                
                                # Try to extract phone number
                                phone_number_pattern = re.compile(r'(\d{4}[*]{2}\d{2}[*]{2}\d{2})')
                                found = re.search(phone_number_pattern, req.text)
                                if found:
                                    phone_number = found.group()
                            
                            out.append({
                                "name": name,
                                "domain": domain,
                                "method": method,
                                "frequent_rate_limit": frequent_rate_limit,
                                "rateLimit": False,
                                "exists": True,
                                "emailrecovery": None,
                                "phoneNumber": phone_number,
                                "others": None
                            })
                            return
                        
                        # Error codes that indicate account doesn't exist
                        if data.get("rtnCd") in ["INVALID_USER", "NOT_FOUND", "INVALID_EMAIL"]:
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
                
        # If we've tried all methods and can't confirm, return with an error to be safe
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


async def get_phone_number(email, client, cookies, headers):
    phone_number_pattern = re.compile(r'(\d{4}[*]{2}\d{2}[*]{2}\d{2})')

    try:
        headers['Referer'] = 'https://account.samsung.com/accounts/v1/Samsung_com_US/resetPassword'
        params = {'v': random.randrange(int(1.5E12), int(2E12))}
        data = {"signUpID": email, "signUpIDType": "003"}

        response = await client.post(
            'https://account.samsung.com/accounts/v1/Samsung_com_US/resetPasswordProc',
            headers=headers,
            params=params,
            cookies=cookies,
            json=data)
            
        if response.status_code == 200:
            data = response.json()

            phone_number = None
            if data.get('rtnCd') == 'NEXT':
                req = await client.get('https://account.samsung.com' + data["nextURL"], headers=headers, cookies=cookies)
                found = re.search(phone_number_pattern, req.text)
                if found:
                    phone_number = found.group()
                elif 'btnResetPasswordWithRecovery' in req.text:
                    recovery_params = {
                        'v': random.randrange(int(1.5E12), int(2E12))
                    }
                    recovery_response = await client.post(
                        "https://account.samsung.com/accounts/v1/Samsung_com_US/resetPasswordWithRecoveryProc",
                        headers=headers, 
                        params=recovery_params, 
                        cookies=cookies
                    )
                    if recovery_response.status_code == 200:
                        recovery_data = recovery_response.json()
                        if recovery_data.get('rtnCd') == 'NEXT':
                            recovery_req = await client.get('https://account.samsung.com' + recovery_data["nextURL"], headers=headers, cookies=cookies)
                            found = re.search(phone_number_pattern, recovery_req.text)
                            if found:
                                phone_number = found.group()
        return phone_number
    except:
        return None
