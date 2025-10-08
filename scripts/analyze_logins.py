import re
import pandas as pd
from collections import Counter

LOG_FILE = "C:\\Users\\DELL\\Documents\\login-attempt-analyzer\\data\\auth.log"

pattern = r"(?P<month>\w+)\s+(?P<day>\d+)\s+(?P<time>[\d:]+).*?(?P<status>Failed|Accepted).*?user\s+(?P<user>\w+).*?from\s+(?P<ip>[\d.]+)"

data = []

with open(LOG_FILE, "r") as f:
    for line in f:
        match = re.search(pattern, line)
        if match:
            data.append(match.groupdict())

df = pd.DataFrame(data)
print("\n=== All Login Attempts ===")
print(df)

# Count failed attempts per IP
failed_ips = df[df['status'] == 'Failed']['ip']
counts = Counter(failed_ips)

print("\n=== Suspicious IPs (Multiple Failures) ===")
for ip, count in counts.items():
    if count > 2:
        print(f"{ip} -> {count} failed attempts")

import matplotlib.pyplot as plt

# --- Existing code above this line ---
# (your parsing, df creation, and print statements)

# === Visualize failed attempts per IP ===
failed_counts = df[df['status'] == 'Failed']['ip'].value_counts()

plt.figure(figsize=(8,5))
failed_counts.plot(kind='bar', color='crimson', edgecolor='black')
plt.title('Failed Login Attempts per IP Address')
plt.xlabel('IP Address')
plt.ylabel('Number of Failed Attempts')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("C:\\Users\\DELL\\Documents\\login-attempt-analyzer\\images\\failed_attempts_per_ip.png")  # saves chart for README
plt.show()

from check_ip_reputation import check_ip

print("\n🔍 Checking IP Reputation on AbuseIPDB...\n")
suspicious_ips = [ip for ip, count in counts.items() if count > 2]
for ip in suspicious_ips:
    result = check_ip(ip)
    if "error" in result:
        print(f"[!] Error checking {ip}: {result['error']}")
    else:
        print(f"IP: {result['ip']}")
        print(f"Abuse Confidence Score: {result['abuseConfidenceScore']}%")
        print(f"Total Reports: {result['totalReports']}")
        print(f"Country: {result['countryCode']} | ISP: {result['isp']}")
        print(f"Usage Type: {result['usageType']}")
        print("-" * 50)
