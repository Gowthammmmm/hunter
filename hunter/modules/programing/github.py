from hunter.core import *
from hunter.localuseragent import *
import random
import re
import json


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
        'TE': 'trailers'
    }

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
            raise Exception("CSRF token not found")

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
                    f"https://api.github.com/search/users?q={email}",
                    headers={
                        **headers,
                        'Accept': 'application/vnd.github.v3+json'
                    }
                )
                
                if profile_check.status_code == 200:
                    profile_data = profile_check.json()
                    if profile_data and 'items' in profile_data and len(profile_data['items']) > 0:
                        user = profile_data['items'][0]
                        # Get additional user details
                        user_details = await client.get(
                            user['url'],
                            headers={
                                **headers,
                                'Accept': 'application/vnd.github.v3+json'
                            }
                        )
                        
                        if user_details.status_code == 200:
                            details = user_details.json()
                            others = {
                                "username": user.get("login"),
                                "name": details.get("name"),
                                "company": details.get("company"),
                                "blog": details.get("blog"),
                                "location": details.get("location"),
                                "bio": details.get("bio"),
                                "public_repos": details.get("public_repos"),
                                "public_gists": details.get("public_gists"),
                                "followers": details.get("followers"),
                                "following": details.get("following"),
                                "created_at": details.get("created_at"),
                                "updated_at": details.get("updated_at"),
                                "avatar_url": details.get("avatar_url")
                            }
                        else:
                            others = {
                                "username": user.get("login"),
                                "avatar_url": user.get("avatar_url"),
                                "url": user.get("url")
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
