from hunter.core import *
from hunter.localuseragent import *
import random
import re
import json


async def twitter(email, client, out):
    name = "twitter"
    domain = "twitter.com"
    method = "register"
    frequent_rate_limit = True

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://twitter.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://twitter.com/i/flow/signup',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'TE': 'trailers'
    }

    try:
        # Get guest token first
        guest_token_response = await client.post(
            "https://api.twitter.com/1.1/guest/activate.json",
            headers={
                **headers,
                'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs=1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'
            }
        )

        if guest_token_response.status_code != 200:
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

        guest_token = guest_token_response.json().get('guest_token')
        if not guest_token:
            raise Exception("Failed to get guest token")

        # Check email availability
        check = await client.post(
            "https://api.twitter.com/i/users/email_available.json",
            params={
                "email": email
            },
            headers={
                **headers,
                'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs=1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                'x-guest-token': guest_token
            }
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
        if response_data.get("taken") is True:
            # Try to get additional account info
            try:
                # Try to get public profile info
                profile_check = await client.get(
                    f"https://api.twitter.com/1.1/users/lookup.json",
                    params={
                        "email": email
                    },
                    headers={
                        **headers,
                        'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs=1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                        'x-guest-token': guest_token
                    }
                )
                
                if profile_check.status_code == 200:
                    profile_data = profile_check.json()
                    if profile_data and len(profile_data) > 0:
                        user = profile_data[0]
                        others = {
                            "username": user.get("screen_name"),
                            "name": user.get("name"),
                            "description": user.get("description"),
                            "location": user.get("location"),
                            "followers_count": user.get("followers_count"),
                            "friends_count": user.get("friends_count"),
                            "statuses_count": user.get("statuses_count"),
                            "created_at": user.get("created_at"),
                            "verified": user.get("verified"),
                            "profile_image_url": user.get("profile_image_url_https"),
                            "profile_banner_url": user.get("profile_banner_url")
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
