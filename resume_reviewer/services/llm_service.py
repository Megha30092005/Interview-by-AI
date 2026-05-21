
from google import genai

client = genai.Client(api_key="AIzaSyBsJcXKYh1pl_CHIfwTVuqky6TsOxPguzY")

def generate(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        print("Gemini error:", e)
        return ""



