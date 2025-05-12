from hunter.core import *
from hunter.localuseragent import *


async def amazon(email, client, out):
    name = "amazon"
    domain = "amazon.com"
    method = "login"
    frequent_rate_limit=False

    headers = {
        "User-agent": random.choice(ua["browsers"]["chrome"]),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }

    try:
        # First try the sign-in page
        url = "https://www.amazon.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3F_encoding%3DUTF8%26ref_%3Dnav_ya_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&"
        req = await client.get(url, headers=headers)
        
        if req.status_code != 200:
            out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": True,
                        "exists": False,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
            return

        body = BeautifulSoup(req.text, 'html.parser')
        data = dict([(x["name"], x["value"]) for x in body.select(
            'form input') if ('name' in x.attrs and 'value' in x.attrs)])
        data["email"] = email

        # Try the sign-in endpoint
        req = await client.post('https://www.amazon.com/ap/signin/', data=data, headers=headers)
        body = BeautifulSoup(req.text, 'html.parser')

        # Check for various indicators of account existence
        if (body.find("div", {"id": "auth-password-missing-alert"}) or 
            "Enter your password" in req.text or
            "Password" in req.text):
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
