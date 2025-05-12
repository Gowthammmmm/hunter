from hunter.core import *
from hunter.localuseragent import *
import random
import re
import json

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
        'Referer': 'https://www.linkedin.com/signup',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'TE': 'trailers'
    }

    try:
        # Get initial page and extract CSRF token
        response = await client.get(
            "https://www.linkedin.com/signup",
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
        csrf_match = re.search(r'name="csrfToken" value="([^"]+)"', response.text)
        if not csrf_match:
            raise Exception("CSRF token not found")

        token = csrf_match.group(1)
        headers["X-CSRF-Token"] = token

        # First check if email is valid format
        check = await client.post(
            "https://www.linkedin.com/checkpoint/rp/request-password-reset",
            json={
                "email": email,
                "csrfToken": token
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
                    f"https://www.linkedin.com/voyager/api/identity/profiles?q=memberIdentity&memberIdentity={email}",
                    headers={
                        **headers,
                        'X-Restli-Protocol-Version': '2.0.0',
                        'X-Li-Lang': 'en_US',
                        'X-Li-Track': '{"clientVersion":"1.12.8505","mpVersion":"1.12.8505","osName":"web","timezoneOffset":0,"timezone":"GMT","deviceFormFactor":"DESKTOP","mpName":"voyager-web"}'
                    }
                )
                
                if profile_check.status_code == 200:
                    profile_data = profile_check.json()
                    if profile_data and 'included' in profile_data:
                        profile = next((item for item in profile_data['included'] if item.get('$type') == 'com.linkedin.voyager.identity.profile.Profile'), None)
                        if profile:
                            others = {
                                "firstName": profile.get("firstName"),
                                "lastName": profile.get("lastName"),
                                "headline": profile.get("headline"),
                                "location": profile.get("locationName"),
                                "industry": profile.get("industryName"),
                                "profilePicture": profile.get("profilePicture", {}).get("displayImage")
                            }
                        else:
                            others = None
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