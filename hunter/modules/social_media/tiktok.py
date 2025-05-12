from hunter.core import *
from hunter.localuseragent import *
import random

async def tiktok(email, client, out):
    name = "tiktok"
    domain = "tiktok.com"
    method = "register"
    frequent_rate_limit = True

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://www.tiktok.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://www.tiktok.com/signup',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'TE': 'trailers'
    }

    try:
        # First check if email is valid format
        check = await client.post(
            "https://www.tiktok.com/api/user/check_email/",
            json={
                "email": email,
                "aid": "1233",
                "app_language": "en",
                "device_platform": "web",
                "device_id": "".join(random.choices('0123456789abcdef', k=16))
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
        if response_data.get("data", {}).get("is_registered", False):
            # Try to get additional account info
            try:
                # Try to get public profile info
                profile_check = await client.get(
                    f"https://www.tiktok.com/api/user/detail/?uniqueId={email}",
                    headers=headers
                )
                
                if profile_check.status_code == 200:
                    profile_data = profile_check.json()
                    if profile_data.get("userInfo"):
                        user = profile_data["userInfo"]
                        others = {
                            "name": user.get("nickname"),
                            "profile_url": f"https://www.tiktok.com/@{user.get('uniqueId')}",
                            "profile_picture": user.get("avatarLarger"),
                            "followers": user.get("followerCount"),
                            "following": user.get("followingCount"),
                            "likes": user.get("heartCount"),
                            "verified": user.get("verified", False)
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