from hunter.core import *
from hunter.localuseragent import *

async def medium(email, client, out):
    # Stub implementation
    out.append({
        "name": "medium",
        "domain": "medium.com",
        "rateLimit": False,
        "error": True,
        "exists": False,
        "emailrecovery": None,
        "phoneNumber": None,
        "others": None
    }) 