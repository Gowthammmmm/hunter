from hunter.core import *
from hunter.localuseragent import *

is_stub = True

async def vk(email, client, out):
    # Stub implementation
    out.append({
        "name": "vk",
        "domain": "vk.com",
        "rateLimit": False,
        "error": True,
        "exists": False,
        "emailrecovery": None,
        "phoneNumber": None,
        "others": None
    }) 