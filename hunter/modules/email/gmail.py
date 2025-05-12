from hunter.core import *
from hunter.localuseragent import *
import random
import re

async def gmail(email, client, out):
    name = "gmail"
    domain = "gmail.com"
    method = "register"
    frequent_rate_limit = True

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'X-Same-Domain': '1',
        'Origin': 'https://accounts.google.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://accounts.google.com/signup',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    }

    try:
        # Get initial page and extract CSRF token
        response = await client.get(
            "https://accounts.google.com/signup",
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

        # Check email availability
        check = await client.post(
            "https://accounts.google.com/_/signup/validateemail",
            json={
                "email": email,
                "flowEntry": "SignUp",
                "flowName": "GlifWebSignIn",
                "hl": "en",
                "f.req": f'["{email}",null,[]]',
                "azt": token
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
        if "EmailExists" in str(response_data) or "EmailAlreadyExists" in str(response_data):
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