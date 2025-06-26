import httpx

def scrapeRewe():
    url = f'https://shop.rewe.de/api/receipts'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://shop.rewe.de/",
        "Accept": "application/json",
    }

    cookies = {
        #"_rdfa" : "s:6b6a237c-4431-4a09-a896-b1e7c7f8b1e6.clvt55EBCihYF1zyiIvhi5hAZQZCUacqLPigdf4OEAs",
        #"consentSettings" : "{%22Usercentrics-Consent-Management-Platform%22:1%2C%22Adobe-Launch%22:1%2C%22AWIN%22:1%2C%22Cloudflare%22:1%2C%22Keycloak%22:1%2C%22gstatic-com%22:1%2C%22JSDelivr%22:1%2C%22jQuery%22:1%2C%22Google-Ad-Manager-Basis%22:1%2C%22Funktionale-Cookies-und-Speicher%22:1%2C%22GfK-SENSIC%22:1%2C%22Realperson-Chat-Suite%22:1%2C%22Cloudflare-Turnstile%22:1%2C%22ChannelPilot%22:0%2C%22artegic-ELAINE-Software%22:0%2C%22Outbrain%22:0%2C%22RDFA-Technologie-Statistik-%22:0%2C%22Adobe-Analytics%22:0%2C%22Mouseflow%22:0%2C%22Facebook-Pixel%22:0%2C%22Microsoft-Advertising-Remarketing%22:0%2C%22Google-Maps%22:0%2C%22YouTube-Video%22:0%2C%22Google-Ads-Conversion-Tracking%22:0%2C%22Google-Ads-Remarketing%22:0%2C%22Snapchat-Advertising%22:0%2C%22Pinterest-Tags%22:0%2C%22trbo%22:0%2C%22TikTok-Advertising%22:0%2C%22LinkedIn-Ads%22:0%2C%22Taboola%22:0%2C%22Vimeo%22:0%2C%22Cmmercl-ly%22:0%2C%22Google-Ad-Manager%22:0%2C%22RDFA-Technologie-Marketing-%22:0%2C%22The-Trade-Desk%22:0%2C%22tms%22:1%2C%22necessaryCookies%22:1%2C%22cmpPlatform%22:1%2C%22marketingBilling%22:1%2C%22fraudProtection%22:1%2C%22basicAnalytics%22:1%2C%22marketingOnsite%22:1%2C%22extendedAnalytics%22:0%2C%22serviceMonitoring%22:0%2C%22abTesting%22:0%2C%22conversionOptimization%22:0%2C%22feederAnalytics%22:0%2C%22personalAdsOnsite%22:0%2C%22remarketingOffsite%22:0%2C%22userProfiling%22:0%2C%22sessionMonitoring%22:0%2C%22targetGroup%22:0%2C%22advertisingOnsite%22:0}",
        #"websitebot-launch" : "human-mousemove",
        #"__cf_bm" : "18hUhtbWhJaNyywoOdBLTHhZFDPWFGZ7vYZJ1g32Io8-1750861343-1.0.1.1-13N2RuZ5VhTpmeoFgtRL.hFxjEGuxLGurspkqoyszOB2a600TKKXRJiZW47DsF_1ZnqaEhmna8goYbdvVHD4PHwl3Je71L93weEkgce4_70",
        #"_cfuvid" : "3InU_R3h1jIzy1YN01yLHj16DwUZ5mZ4Ico2AnV05jk-1750861343899-0.0.1.1-604800000",
        #"cf_clearance" : "zgpPZnbZVoUmEp2pig2ihCt1WWD.tcVDvfYs_.vC5d8-1750861454-1.2.1.1-BWRVXzxm52yW_Ds68yEv75JHK3QKmEM8cgf_7i96aBSR9MX5ViJbpziyotJBtJMQ3PmUrVxGyS8XsFuvhN26lkF5Ffv13Vv0wNsu28wMETAJ9ScFXXN_S_jUzFgwBjr0rrTb..5HZ0w_bVpfd6_6F7NfN_EpCK90F5wCLLSTCE2Hm5FNTtRCiSCP5zxwzdQJYf_zw5pRn2KYgzK5Ue.BVCOQo_UQZKcNTzSvIJK4GAJLsT2LBDqhrT._Z.kiE39Mhec0b7MJJ5Ae8MQzjsEo6P4pjhxE04r.Z1dhnAjpOpTXU8B_zqBDh8Li3PEgTAZg2ASPqIF5vQsJ6_7Zc5QdmD3f4c2ZHD7t2EMeO6292jkDGNFIHsPJoGBe2wWbH7h3",
        #"MRefererUrl" : "direct",
        #"mtc" : "s:eyJ0ZXN0Z3JvdXBzSGFzaCI6IjQwNzIzYjk1YjZlYTQyZjk4ZmFiY2MxZDljZmMwMjhmMjkwOGNlNWZjYTg4NTI3OWJkMzJlZjM5Nzg5Nzg4OWIiLCJoYXNoIjoiSktWT2tsTldNSnZDWVh6Y085aVV6QT09Iiwic3RhYmxlIjpbImNhdGVnb3J5LW92ZXJ2aWV3LXJlbmRlcmVyLXJlbG9hZCIsImxkLXJlY2lwZS1yZXZpZXdzLXYyIiwibGQtcmVjaXBlLXJldmlld3MtdjIiLCJwcmVmaWxsZWQtbG93cmF0ZSIsInRyb3kiLCJwcmVmaWxsZWQtaGlnaHJhdGUiLCJiYXNrZXQtYXMtcHJvZ3Jlc3NiYXIiLCJzcHMtc3RvY2stYnktaWRlbnQiLCJwYXliYWNrLXJld2UtbmV3c2xldHRlciIsImNoZWNrb3V0LW1scy1jdXN0b21lci1hc3NpZ25tZW50IiwicGF5bWVudC1lbmFibGUtZ29vZ2xlLXBheSIsImFkZHJlc3MtYXV0b2NvbXBsZXRlIiwicGF5YmFjay10YXJnZXRlZC1idXJuIiwic2ZzLXBpY2t1cC1zdGFnZ2VyaW5nLWluZm9ib3giLCJwYXliYWNrLWVjb3Vwb24tYXBpIiwicmV3ZS1zc28iLCJvZmZlci1kZXRhaWxzLXRyYWNraW5nIiwicGF5YmFjay10YXJnZXRlZC1ib251cy1jb3Vwb24iLCJwYXliYWNrLWV2b3VjaGVyIiwicGF5YmFjay1jYXJkLWNoYW5nZSIsImNhdGVnb3J5LW92ZXJ2aWV3LXJlbmRlcmVyIiwicGF5bWVudC1uZXctZGlyZWN0LWRlYml0LWlucHV0IiwicGF5bWVudC1lbmFibGUtYXBwbGUtcGF5IiwiYWJ0LXBkcC1jb21iaW5lZC1kZXNjcmlwdGlvbiIsImhpZGUtcGF5YmFjayIsInNwcy1zdG9jayJdLCJyZHRnYSI6W10sIm10Y0V4cGlyZXMiOjB9.yqnrlYShdiSKAgLN0LTr/UwGqpgMKzksrkXZRIMmhNA",
        "rstp" : "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhZXMxOTIiOiJiZGVhMTA4MmU4MzdiZDVmMTA0NjlhZjQzOTFlMjIwYjdhYmJlZDhmZmEzMDQ2MTU3M2RkMzgyYWRiZjE4NDcxM2M2NmIyMTQ4NWQxZDlkNzQyNmUxOGU3Y2ZjZGVjNzkyYmY1Yzc2NDMzNDY1YzZlYWMzNWRmZGUxMzc2Mjk0YTI1ODJjNGIwMDhjMmU2NTIwNDdmZGNhMmMzMDFjZDRjNGNiZjQ2ZDA1ZTNiYWM0NGVjMDg5NWQwYjFlNGVmMjI0OWY1ZWY0NzAzODBmZTViYTljZjFkMjVmMGQ0ZmY4Yjk1ZGFmNjczM2EyN2Y2YjViZWIxMTI5MGY4YWU2ZDcxY2I3NDdiYTc2MmQ3NzhkMmNiYmM0NTk4YTFkYzQwNTMzNDc0NmNmZTVlNmY4NTM0NzJhZWRmZmU2YTk2OTVmNzBmNzI2Y2QwNThhYWU4MzhmOTcxY2U5NDg1MmMxM2EwODk0ZThlOWJhMWU1YmY3YTcxMDZjNTBlM2U5NmQ0ZjMzNjY0YjgxYzUyOWEyYTFhY2NmZjUyZWZmZTM1MGVjMWY5MmQwNWUwZWI2NjI0NGZmNzZiOTY5ZTc0MDEyZTBiYTE3MzVjODBhYmU4YzU3MTU0MzY0YzRmMTRjMzI1ZWEzM2JhZTg3NDlhZTU3YTY1MjIwNjMzMmNjNTc3OGE5MGVkMzQ2YTE2MDdkM2I3OGM4MzExMDBjYzYyOGM1MDU3MjA5MjYxNjIyMWFhMzM4NmUzM2I5MjQ2NWNiMTE4Nzg0NjNhZjg4YjUzNjdiMTEyMGVmMjkzNzllNDc2OWJhNzY5NWM4M2IwZDNiNThmNjI3MGVlNGRmY2Y3NzRiMWYzN2ZkODJhOWNmMjEyMWFmM2Q1MzFiODQyNjc0MThjMDE0NGY3M2RkYmRiNzFkNDQ5YjQxMGM3MGFjNTRlMDNhZDhkZDM4OTYwMjRkZmJmNjMxYzUwYzlmNmUzZDYyNGVjNmIyNmM4ZWRiNmYzOWJlZjRjNDgyNGNjZGQ4NzBjZTVjYzhlY2IyYjFmYjhhYWNhODJkNGQ4MDBiMTkyNWFiODQyYjI0MmNjMDBlYjExYjc5ZGE4YTcwNGQ2NTg4MzA2NjM3MzJkZDA3ZTA0ZWIwN2JlYmE4ZTY5OWM1NjY0NDU5NzlkNWUxMTc0NzUxYTRlMzFlOTlmYzQ2ZWQ1MjhkNSIsImV4cCI6MTc1MDg2MjE4OCwiaWF0IjoxNzUwODYxNTg4LCJpdiI6IldxZ1RpYmljSlFRV213Q3hTSk94U2cifQ.xrrCweSTrpOLCGhJsBBJij9G3TU2fVnkXjqZQFVH2VQMjrR3gs5ievNdFUgIRGH0nKy7SMvQVLSdfXmKLkZLqQ",
        #"perfTimings" : "event188=0.94%2Cevent189",
        #"perfLoad" : "0.94"
    }

        # Anfrage senden
    
    try:
        with httpx.Client() as client:
            global data
            response = client.get(url, headers=headers, cookies=cookies)
            print(response.status_code)
            data = response.json()
            print(data)
    except httpx.RequestError as e:
        print(f"An error occurred while requesting data: {e}")
        
if __name__ == "__main__":
    scrapeRewe()