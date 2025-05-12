from hunter.core import *
from hunter.localuseragent import *
import re
import random
import json

async def youtube(email, client, out):
    name = "youtube"
    domain = "youtube.com"
    method = "register"
    frequent_rate_limit = True

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'TE': 'trailers'
    }

    try:
        # Try to get additional account info
        try:
            # Try to get public profile info
            profile_check = await client.get(
                f"https://www.youtube.com/results?search_query={email}&sp=EgIQAg%253D%253D",
                headers=headers
            )
            
            if profile_check.status_code == 429:
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

            if profile_check.status_code != 200:
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

            # Extract profile info from response
            profile_match = re.search(r'data-testid="channel-title"[^>]*href="([^"]+)"[^>]*>([^<]+)</a>', profile_check.text)
            if profile_match:
                profile_url = profile_match.group(1)
                profile_name = profile_match.group(2)
                
                # Try to get profile picture
                pic_match = re.search(r'data-testid="channel-avatar"[^>]*src="([^"]+)"', profile_check.text)
                profile_pic = pic_match.group(1) if pic_match else None
                
                # Try to get subscriber count
                sub_match = re.search(r'(\d+(?:\.\d+)?[KMB]?)\s+subscribers?', profile_check.text)
                subscribers = sub_match.group(1) if sub_match else None
                
                # Try to get video count
                video_match = re.search(r'(\d+(?:\.\d+)?[KMB]?)\s+videos?', profile_check.text)
                videos = video_match.group(1) if video_match else None
                
                others = {
                    "name": profile_name,
                    "profile_url": f"https://www.youtube.com{profile_url}",
                    "profile_picture": profile_pic,
                    "subscribers": subscribers,
                    "videos": videos
                }

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
                return
            else:
                # Try alternative search method
                alt_check = await client.get(
                    f"https://www.youtube.com/results?search_query={email.split('@')[0]}",
                    headers=headers
                )
                
                if alt_check.status_code == 200:
                    alt_match = re.search(r'data-testid="channel-title"[^>]*href="([^"]+)"[^>]*>([^<]+)</a>', alt_check.text)
                    if alt_match:
                        profile_url = alt_match.group(1)
                        profile_name = alt_match.group(2)
                        
                        # Try to get profile picture
                        pic_match = re.search(r'data-testid="channel-avatar"[^>]*src="([^"]+)"', alt_check.text)
                        profile_pic = pic_match.group(1) if pic_match else None
                        
                        # Try to get subscriber count
                        sub_match = re.search(r'(\d+(?:\.\d+)?[KMB]?)\s+subscribers?', alt_check.text)
                        subscribers = sub_match.group(1) if sub_match else None
                        
                        # Try to get video count
                        video_match = re.search(r'(\d+(?:\.\d+)?[KMB]?)\s+videos?', alt_check.text)
                        videos = video_match.group(1) if video_match else None
                        
                        others = {
                            "name": profile_name,
                            "profile_url": f"https://www.youtube.com{profile_url}",
                            "profile_picture": profile_pic,
                            "subscribers": subscribers,
                            "videos": videos
                        }

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
                        return

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
                return

        # If we get here, no account was found
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