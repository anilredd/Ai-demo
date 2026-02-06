import json
import os
import sys
from google import genai
from google.genai import types

print("\n🔍 ===== STARTING AI DOCKER IMAGE REVIEW =====")

# Read Gemini API key
raw_api_key = os.getenv("GEMINI_API_KEY")
if not raw_api_key:
    print("❌ ERROR: GEMINI_API_KEY not found.")
    sys.exit(1)

api_key = raw_api_key.strip().replace('"', '').replace("'", "")

# Initialize Gemini client (v1)
client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(api_version="v1")
)

# Load Trivy scan results
try:
    with open("scan.json", "r") as f:
        scan_data = json.load(f)
except Exception as e:
    print(f"❌ Failed to read scan.json: {e}")
    sys.exit(1)

prompt = f"""
You are a DevSecOps AI assistant.
Analyze this Docker vulnerability scan report.
Flag STATUS: FAIL if:
- There are CRITICAL vulnerabilities
- Or HIGH risk vulnerabilities that are exploitable

Otherwise say STATUS: PASS.

Here is the scan report:
{json.dumps(scan_data, indent=2)}
"""

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    print("\n--- AI DOCKER IMAGE ANALYSIS ---")
    print(response.text)

    if "STATUS: FAIL" in response.text.upper():
        print("\n🚫 Critical security risk detected in image. Pipeline failed.")
        sys.exit(1)

except Exception as e:
    print(f"❌ Gemini Error: {e}")
    sys.exit(1)

print("\n✅ Docker Image Passed AI Security Review")
