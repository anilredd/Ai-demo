import os
import sys
from google import genai
from google.genai import types

print("\n🔍 ===== STARTING AI CODE REVIEW (2026 STABLE) =====")

# 1. API Key Cleaning
raw_api_key = os.getenv("GEMINI_API_KEY")
if not raw_api_key:
    print("❌ ERROR: GEMINI_API_KEY not found.")
    sys.exit(1)

api_key = raw_api_key.strip().replace('"', '').replace("'", "")

# 2. Initialize Client for v1 Production
# We explicitly set the api_version to 'v1' to avoid the 404/v1beta issue
client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(api_version="v1")
)

# 3. Code Collection
java_code = ""
for root, dirs, files in os.walk("src/main/java"):
    for file in files:
        if file.endswith(".java"):
            with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                java_code += f"// File: {file}\n{f.read()}\n\n"

if not java_code:
    print("✅ No Java files found.")
    sys.exit(0)

# 4. Generate Review
prompt = "Review this Java code for bugs and security. Start with 'STATUS: FAIL' if critical issues exist.\n\n" + java_code

try:
    # UPDATED MODEL: gemini-2.5-flash is the 2026 stable replacement
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=prompt
    )
    
    print("\n--- AI ANALYSIS ---")
    print(response.text)
    
    if "STATUS: FAIL" in response.text.upper():
        print("\n🚫 Critical issues detected. Pipeline failed.")
        sys.exit(1)

except Exception as e:
    print(f"❌ Gemini Error: {e}")
    # If gemini-2.5-flash isn't available in your region yet, try "gemini-2.0-flash"
    sys.exit(1)

print("\n✅ AI REVIEW PASSED")