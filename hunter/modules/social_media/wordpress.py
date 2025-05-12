from hunter.core import *
from hunter.localuseragent import *

async def wordpress(email, client, out):
    # Stub implementation
    out.append({
        "name": "wordpress",
        "domain": "wordpress.com",
        "rateLimit": False,
        "error": True,
        "exists": False,
        "emailrecovery": None,
        "phoneNumber": None,
        "others": None
    }) 