from hunter.core import *
from hunter.localuseragent import *
import json
import random
import re


async def ebay(email, client, out):
    name = "ebay"
    domain = "ebay.com"
    method = "login"
    frequent_rate_limit = True

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://www.ebay.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://www.ebay.com/signin/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'TE': 'trailers'
    }

    try:
        # Get CSRF token
        req = await client.get(
            "https://www.ebay.com/signin/", 
            headers=headers
        )

        if req.status_code == 429:
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

        if req.status_code != 200:
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

        try:
            srt = req.text.split('"csrfAjaxToken":"')[1].split('"')[0]
        except IndexError:
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

        # Check email existence
        data = {
            'identifier': email,
            'srt': srt
        }

        check = await client.post(
            'https://signin.ebay.com/signin/srv/identifer',
            data=data, 
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

        results = check.json()

        if "err" in results:
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

        # Try to get additional account info
        try:
            # Try to get public profile info
            profile_check = await client.get(
                f"https://www.ebay.com/usr/{email.split('@')[0]}",
                headers=headers
            )
            
            if profile_check.status_code == 200:
                # Extract profile info from response
                profile_match = re.search(r'<h1 class="mbg-nw">([^<]+)</h1>', profile_check.text)
                if profile_match:
                    profile_name = profile_match.group(1)
                    
                    # Try to get member since date
                    since_match = re.search(r'Member since\s+([^<]+)</span>', profile_check.text)
                    member_since = since_match.group(1) if since_match else None
                    
                    # Try to get feedback score
                    feedback_match = re.search(r'Feedback Score\s+(\d+)</span>', profile_check.text)
                    feedback_score = feedback_match.group(1) if feedback_match else None
                    
                    others = {
                        "name": profile_name,
                        "profile_url": f"https://www.ebay.com/usr/{email.split('@')[0]}",
                        "member_since": member_since,
                        "feedback_score": feedback_score
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
