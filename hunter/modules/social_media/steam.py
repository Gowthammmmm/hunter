from hunter.core import *
from hunter.localuseragent import *
import random

is_stub = True

async def steam(email, client, out):
    name = "steam"
    domain = "steam.com"
    method = "register"
    frequent_rate_limit=False

    headers = {
        "User-Agent": random.choice(ua["browsers"]["chrome"]),
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "X-Requested-With": "XMLHttpRequest",
        "DNT": "1",
        "Connection": "keep-alive",
        "Referer": "https://store.steampowered.com/join/",
        "Origin": "https://store.steampowered.com"
    }

    try:
        # First get the session ID
        session = await client.get("https://store.steampowered.com/join/", headers=headers)
        if session.status_code != 200:
            out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": True,
                        "exists": False,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
            return

        # Check email availability
        params = {
            "email": email,
            "count": "1",
            "l": "english"
        }
        
        check = await client.get(
            "https://store.steampowered.com/actions/ValidateEmail",
            headers=headers,
            params=params
        )

        if check.status_code != 200:
            out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": True,
                        "exists": False,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
            return

        response = check.json()
        
        # If email is already in use, account exists
        if response.get("bAvailable") is False:
            out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": False,
                        "exists": True,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
        else:
            out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": False,
                        "exists": False,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})

    except Exception as e:
        if "Too Many Requests" in str(e) or "429" in str(e):
            out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": True,
                        "exists": False,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
        else:
            out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": False,
                        "exists": False,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None}) 