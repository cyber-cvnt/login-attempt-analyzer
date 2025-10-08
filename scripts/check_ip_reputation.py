import requests
import json

# Load your API key
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("ABUSEIPDB_API_KEY")

def check_ip(ip_address):
    """
    Query the AbuseIPDB API to check if an IP address has been reported.
    """
    url = "https://api.abuseipdb.com/api/v2/check"
    headers = {
        "Accept": "application/json",
        "Key": API_KEY
    }
    params = {
        "ipAddress": ip_address,
        "maxAgeInDays": 90
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()["data"]
        
        # Return a formatted summary
        return {
            "ip": ip_address,
            "abuseConfidenceScore": data["abuseConfidenceScore"],
            "totalReports": data["totalReports"],
            "countryCode": data["countryCode"],
            "isp": data.get("isp", "N/A"),
            "usageType": data.get("usageType", "N/A"),
        }

    except Exception as e:
        return {"ip": ip_address, "error": str(e)}

# Example usage
if __name__ == "__main__":
    test_ip = "192.168.0.1"
    result = check_ip(test_ip)
    print(json.dumps(result, indent=4))
