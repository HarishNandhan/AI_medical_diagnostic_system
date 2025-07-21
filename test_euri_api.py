#!/usr/bin/env python3
"""
Quick test script for EuriAI API
Run this to test if your API key and connection work
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("EURI_API_KEY")
BASE_URL = "https://api.euron.one/api/v1/chat/completions"

def test_api():
    print("🧪 Testing EuriAI API Connection...")
    print(f"API Key: {API_KEY[:20] if API_KEY else 'NOT FOUND'}...")
    print(f"Base URL: {BASE_URL}")
    
    if not API_KEY:
        print("❌ ERROR: EURI_API_KEY not found in environment variables")
        return False
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    payload = {
        "messages": [{"role": "user", "content": "Hello, this is a test message. Please respond with 'API test successful'."}],
        "model": "gpt-4.1-nano",
        "max_tokens": 50,
        "temperature": 0.7
    }
    
    try:
        print("📡 Making API request...")
        response = requests.post(BASE_URL, headers=headers, json=payload, timeout=30)
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            print(f"✅ SUCCESS! Response: {content}")
            return True
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return False

if __name__ == "__main__":
    success = test_api()
    if success:
        print("\n🎉 API test passed! Your EuriAI integration should work.")
    else:
        print("\n💥 API test failed. Check your API key and network connection.")