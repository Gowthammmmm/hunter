from hunter.core import *
from hunter.localuseragent import *
import random
import re
import json
import asyncio


async def github(email, client, out):
    name = "github"
    domain = "github.com"
    method = "register"
    frequent_rate_limit = True

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://github.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://github.com/signup',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Cache-Control': 'max-age=0',
        'TE': 'trailers'
    }

    try:
        # Add a small random delay to avoid rate limiting
        await asyncio.sleep(random.uniform(1, 2))
        
        # Method 1: Use the /signup_check/email endpoint
        try:
            # Get initial page and extract CSRF token
            response = await client.get(
                "https://github.com/signup",
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

            # Extract CSRF token using regex
            csrf_match = re.search(r'name="authenticity_token" value="([^"]+)"', response.text)
            if not csrf_match:
                # Try alternative extraction method
                csrf_match = re.search(r'"csrf_token":"([^"]+)"', response.text)
                if not csrf_match:
                    # One more attempt with different pattern
                    csrf_match = re.search(r'data-csrf="([^"]+)"', response.text)
                    
            if csrf_match:
                token = csrf_match.group(1)
                headers["X-CSRF-Token"] = token
                
                # First check if email is valid format
                check = await client.post(
                    "https://github.com/signup_check/email",
                    json={
                        "email": email,
                        "authenticity_token": token
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
                        
                        # Check if email exists based on response
                        if response_data.get("exists") is True or "EmailAlreadyExists" in str(response_data) or "email is already taken" in str(response_data).lower():
                            # Account exists, try to get additional info
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
                        # If we can't parse JSON but see text indicators
                        if "already exists" in check.text.lower() or "email is taken" in check.text.lower() or "email already exists" in check.text.lower():
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
        
        # Method 2: Try password reset endpoint
        try:
            # Get forgot password page for CSRF token
            forgot_page = await client.get(
                "https://github.com/password_reset",
                headers=headers,
                follow_redirects=True
            )
            
            if forgot_page.status_code == 200:
                # Extract CSRF token
                csrf_match = re.search(r'name="authenticity_token" value="([^"]+)"', forgot_page.text)
                if not csrf_match:
                    # Try alternative extraction
                    csrf_match = re.search(r'"csrf_token":"([^"]+)"', forgot_page.text)
                    
                if csrf_match:
                    token = csrf_match.group(1)
                    
                    # Submit password reset request
                    reset_headers = headers.copy()
                    reset_headers["Content-Type"] = "application/x-www-form-urlencoded"
                    
                    reset_data = {
                        "authenticity_token": token,
                        "email": email,
                        "commit": "Send password reset email"
                    }
                    
                    reset_response = await client.post(
                        "https://github.com/password_reset",
                        headers=reset_headers,
                        data=reset_data,
                        follow_redirects=True
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
                    
                    # Check response indicators
                    if "check your email" in reset_response.text.lower() or "reset link sent" in reset_response.text.lower() or "email sent" in reset_response.text.lower():
                        # Reset email was sent, account exists
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
                    
                    # No account messages
                    if "can't find that email" in reset_response.text.lower() or "no user with that email" in reset_response.text.lower():
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
        
        # Method 3: Check using GitHub API search
        try:
            # Try to get user info from API
            username_base = email.split('@')[0]
            
            # Remove common numbers and special chars for better search
            clean_username = re.sub(r'[0-9_\.\-]+', '', username_base)
            if len(clean_username) < 3:
                clean_username = username_base
                
            api_headers = {
                'User-Agent': random.choice(ua["browsers"]["chrome"]),
                'Accept': 'application/vnd.github.v3+json',
                'Authorization': None  # Anonymous request
            }
            
            # First try direct email search
            email_search = await client.get(
                f"https://api.github.com/search/users?q={email}+in:email",
                headers=api_headers
            )
            
            if email_search.status_code == 200:
                try:
                    search_data = email_search.json()
                    if search_data.get("total_count", 0) > 0:
                        # Found user with this email
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
                
            # Try username-based search
            username_search = await client.get(
                f"https://api.github.com/search/users?q={clean_username}",
                headers=api_headers
            )
            
            if username_search.status_code == 200:
                try:
                    search_data = username_search.json()
                    if search_data.get("total_count", 0) > 0:
                        # Check if any result matches exactly
                        for item in search_data.get("items", []):
                            user_detail = await client.get(
                                item["url"],
                                headers=api_headers
                            )
                            
                            if user_detail.status_code == 200:
                                detail_data = user_detail.json()
                                if detail_data.get("email") == email:
                                    # Direct email match
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
            pass

        # If we've tried all methods and haven't returned yet, the account likely doesn't exist
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
