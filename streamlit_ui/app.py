import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000/")

# Page configuration
st.set_page_config(
    page_title="AI Medical Diagnostics Assistant",
    page_icon="🩺",
    layout="wide"
)

st.title("🩺 AI Medical Diagnostics Assistant")
st.markdown("---")

# Sidebar with information
with st.sidebar:
    st.header("ℹ️ Information")
    st.info("""
    This AI assistant helps analyze symptoms and provide preliminary diagnostic suggestions.
    
    **Important:** This is for informational purposes only and should not replace professional medical advice.
    """)
    
    st.header("🔧 Settings")
    debug_mode = st.checkbox("Debug Mode", value=False)

# Main interface
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Describe Your Symptoms")
    symptom_input = st.text_area(
        "Please describe your symptoms in detail:",
        height=150,
        placeholder="Example: I have been experiencing headaches for the past 3 days, along with mild fever and fatigue..."
    )
    
    # Input validation
    if symptom_input and len(symptom_input.strip()) < 10:
        st.warning("Please provide more detailed symptoms (at least 10 characters)")
    
    analyze_button = st.button("🔍 Analyze Symptoms", type="primary", disabled=not symptom_input or len(symptom_input.strip()) < 10)

with col2:
    st.header("💡 Tips")
    st.markdown("""
    **For better results:**
    - Be specific about symptoms  
    - Include duration and severity  
    - Mention any relevant medical history  
    - Note any triggers or patterns
    """)

# Results section
if analyze_button and symptom_input:
    with st.spinner("Analyzing your symptoms..."):
        # Prepare the input according to your DiagnosticState structure
        diagnostic_state = {
            "input": symptom_input.strip(),
            "symptom_area": "",
            "diagnosis": ""
        }

        try:
            # Send request to LangServe endpoint
            response = requests.post(
                f"{BACKEND_URL}/diagnose/invoke",
                headers={"Content-Type": "application/json"},
                json={"input": diagnostic_state},  # LangServe wraps input in an "input" key
                timeout=60
            )
            
            if response.status_code == 200:
                outer_result = response.json()
                result = outer_result.get("output", outer_result)

                if debug_mode:
                    with st.expander("🐛 Debug Information"):
                        st.json(result)
                        st.write("Response type:", type(result))
                        st.write("Response keys:", list(result.keys()) if isinstance(result, dict) else "Not a dict")
                
                # Parse the response - should now be the DiagnosticState
                if isinstance(result, dict):
                    symptom_area = result.get("symptom_area", "").strip()
                    diagnosis = result.get("diagnosis", "").strip()
                    
                    # Display results
                    st.markdown("---")
                    st.header("📋 Analysis Results")
                    
                    # Symptom Area Section
                    st.subheader("🎯 Symptom Area Detected")
                    if symptom_area and symptom_area not in ["", "Not identified"]:
                        formatted_area = symptom_area.title()
                        st.success(f"**{formatted_area}**")
                        
                        area_info = {
                            "Infection": "🦠 Possible infectious condition detected",
                            "Respiratory": "🫁 Respiratory system related symptoms",
                            "Neurological": "🧠 Nervous system related symptoms", 
                            "Gastrointestinal": "🍽️ Digestive system related symptoms"
                        }
                        
                        if formatted_area in area_info:
                            st.info(area_info[formatted_area])
                    else:
                        st.warning("Could not identify specific symptom area - general examination recommended")
                    
                    st.markdown("---")
                    
                    # AI Diagnosis Section
                    st.subheader("🔬 AI Diagnosis & Recommendations")
                    if diagnosis and diagnosis not in ["", "No diagnosis available"]:
                        st.markdown("### 📋 Medical Analysis")
                        st.markdown(diagnosis)
                        st.success("✅ AI analysis completed successfully")
                    else:
                        st.warning("Could not generate specific diagnosis")
                        st.info("This might be due to:")
                        st.write("- Insufficient symptom details")
                        st.write("- API connectivity issues") 
                        st.write("- Temporary service unavailability")
                    
                    # Summary section
                    if symptom_area or diagnosis:
                        st.markdown("---")
                        st.subheader("📝 Summary")
                        summary_parts = []
                        if symptom_area:
                            summary_parts.append(f"**Symptom Category:** {symptom_area.title()}")
                        if diagnosis:
                            summary_parts.append(f"**AI Analysis:** Available above")
                        for part in summary_parts:
                            st.write(part)
                    
                    # Disclaimer
                    st.markdown("---")
                    st.error("""
                    ⚠️ **Medical Disclaimer**: This AI analysis is for informational purposes only. 
                    Always consult with qualified healthcare professionals for proper medical diagnosis and treatment.
                    """)
                else:
                    st.error("Unexpected response format from backend")
                    if debug_mode:
                        st.write("Raw response:", result)
            else:
                st.error(f"Backend error: HTTP {response.status_code}")
                if debug_mode:
                    st.write("Response text:", response.text)
                    
        except requests.exceptions.Timeout:
            st.error("⏱️ Request timed out. The AI analysis is taking longer than expected. Please try again.")
        except requests.exceptions.ConnectionError:
            st.error(f"🔌 Cannot connect to backend at {BACKEND_URL}. Please ensure:")
            st.write("- Backend server is running on the correct port")
            st.write("- No firewall is blocking the connection")
            st.write("- The backend URL is correct")
        except requests.exceptions.RequestException as e:
            st.error(f"🌐 Network error: {str(e)}")
        except Exception as e:
            st.error(f"❌ An unexpected error occurred: {str(e)}")
            if debug_mode:
                st.exception(e)

# Footer
st.markdown("---")
st.markdown("*Powered by EuriAI and LangGraph*")
