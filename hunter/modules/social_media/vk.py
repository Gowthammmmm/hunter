from hunter.core import *
from hunter.localuseragent import *
import re
import random

async def vk(email, client, out):
    name = "vk"
    domain = "vk.com"
    method = "register"
    frequent_rate_limit = True

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://vk.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://vk.com/join',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'TE': 'trailers'
    }

    try:
        # First check if email is valid format
        check = await client.post(
            "https://vk.com/join",
            data={
                "email": email,
                "act": "check_email",
                "hash": "",
                "from": "join"
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
        if response_data.get("error", {}).get("code") == 4:  # Email already exists
            # Try to get additional account info
            try:
                # Try to get public profile info
                profile_check = await client.get(
                    f"https://vk.com/search?c[section]=auto&c[q]={email}",
                    headers=headers
                )
                
                if profile_check.status_code == 200:
                    # Extract profile info from response
                    profile_match = re.search(r'data-profile-id="(\d+)"[^>]*>([^<]+)</a>', profile_check.text)
                    if profile_match:
                        profile_id = profile_match.group(1)
                        profile_name = profile_match.group(2)
                        
                        # Try to get profile picture
                        pic_match = re.search(r'data-profile-id="' + profile_id + r'"[^>]*src="([^"]+)"', profile_check.text)
                        profile_pic = pic_match.group(1) if pic_match else None
                        
                        others = {
                            "name": profile_name,
                            "profile_url": f"https://vk.com/id{profile_id}",
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