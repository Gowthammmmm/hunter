from hunter.core import *
from hunter.localuseragent import *
import random
import re
import json

async def facebook(email, client, out):
    name = "facebook"
    domain = "facebook.com"
    method = "register"
    frequent_rate_limit = True

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://www.facebook.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://www.facebook.com/signup',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'TE': 'trailers'
    }

    try:
        # Get initial page and extract CSRF token
        response = await client.get(
            "https://www.facebook.com/signup",
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
        csrf_match = re.search(r'name="jazoest" value="([^"]+)"', response.text)
        if not csrf_match:
            raise Exception("CSRF token not found")

        token = csrf_match.group(1)
        headers["X-CSRF-Token"] = token

        # Generate random username
        username = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=8))

        # First check if email is valid format
        check = await client.post(
            "https://www.facebook.com/checkpoint/email-availability",
            json={
                "email": email,
                "jazoest": token,
                "username": username
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

        if check.status_code != 200:
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

        response_data = check.json()
        
        # Check if email exists based on response
        if response_data.get("exists") is True or "EmailAlreadyExists" in str(response_data):
            # Try to get additional account info
            try:
                # Try to get public profile info
                profile_check = await client.get(
                    f"https://www.facebook.com/search/top?q={email}",
                    headers=headers
                )
                
                if profile_check.status_code == 200:
                    # Extract profile info from response
                    profile_match = re.search(r'data-testid="search_result_profile"([^>]+)>([^<]+)</a>', profile_check.text)
                    if profile_match:
                        profile_url = profile_match.group(1)
                        profile_name = profile_match.group(2)
                        
                        # Try to get profile picture
                        pic_match = re.search(r'data-testid="search_result_profile_picture" src="([^"]+)"', profile_check.text)
                        profile_pic = pic_match.group(1) if pic_match else None
                        
                        others = {
                            "name": profile_name,
                            "profile_url": profile_url,
                            "profile_picture": profile_pic
                        }
                    else:
                        others = None
                else:
                    others = None
            except:
                others = None

            out.append({
                "name": name,
                "domain": domain,
                "method": method,
                "frequent_rate_limit": frequent_rate_limit,
                "rateLimit": False,
                "exists": True,
                "emailrecovery": None,
                "phoneNumber": None,
                "others": others
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
