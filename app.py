import requests
import re
import random
import string
import streamlit as st

# Set up page configuration
st.set_page_config(page_title="Password Strength Meter", page_icon="🔐", layout="centered")
st.title("🔐 Password Strength Meter")
st.markdown("Check if your password is strong and secure!")

# Input password field
password = st.text_input("Enter your password", type="password")

# Customizing the theme using CSS
st.markdown("""
    <style>
        /* Custom App Background and Layout */
        .stApp {
            --sz: 14px;
            --c1: #616161;  /* Darker Neutral Zinc */
            --c2: #505050;  /* Dark Zinc */
            --c3: #424242;  /* Deep Zinc */
            --c4: #353535;  /* Very Dark Zinc */
            --ts: 50% / calc(var(--sz)* 20) calc(var(--sz)* 20);
            margin: 0;
            padding: 0;
            height: 100vh;
            overflow: hidden;
            background-color: var(--c1);  /* Darker Neutral Zinc background */
            color: white;  /* White text for contrast */
        }
        
        /* Adjust header title font */
        h1 {
            color: #e0e0e0;  /* Light gray text */
            font-family: 'Arial', sans-serif;
            font-size: 48px;
            text-align: center;
            text-transform: uppercase;
        }

        /* Text input area customization */
        .stTextInput > div > div > input {
            background-color: #505050;  /* Dark Zinc input background */
            border-radius: 8px;
            border: 2px solid #424242;  /* Deep Zinc border */
            color: white;  /* White text inside input field */
        }

        /* Customize the button appearance */
        .stButton button {
            background-color: #424242;  /* Deep Zinc button background */
            color: white;
            border-radius: 8px;
            font-weight: bold;
            padding: 10px 20px;
        }

        /* Customize progress bar color */
        .stProgress > div > div {
            background-color: #353535;  /* Very Dark Zinc progress bar */
        }

        /* Customize warning messages */
        .stWarning {
            background-color: #424242;  /* Deep Zinc background */
            border-left: 4px solid #e0e0e0;  /* Light gray left border */
            color: white;
        }

        /* Footer/Divider Styling */
        .stDivider {
            border-top: 2px solid #505050;  /* Dark Zinc divider */
        }

    </style>
""", unsafe_allow_html=True)

# Analyze password strength
with st.spinner("Analyzing Strength...."):
    if st.button("Analyze Password Strength."):
        url = "https://www.ncsc.gov.uk/static-assets/documents/PwnedPasswordsTop100k.txt"
        response = requests.get(url)

        blacklist_set = set(response.text.splitlines())

        def is_blacklisted(password):
            return password in blacklist_set

        if is_blacklisted(password):
            st.error("❌ This password is too common and easily guessed by attackers. Choose a stronger one!")
        else:
            def checkPasswordStrength(password):
                score = 0
                feedback = []
                strength = ""
                if(len(password) >= 8):
                    score += 1
                else:
                    feedback.append("🚨 Password must be at least 8 characters long.")
                if(re.search("[A-Z]", password)):
                    score += 1
                else:
                    feedback.append("🚨 Password must include uppercase letters.")
                if(re.search("[a-z]", password)):
                    score += 1
                else:
                    feedback.append("🚨 Password must include lowercase letters.")
                if(re.search("[0-9]", password)):
                    score += 1
                else:
                    feedback.append("🚨 Password must include at least 1 digit.")
                if(re.search(f"[{re.escape(string.punctuation)}]", password)):
                    score += 1
                else:
                    feedback.append("🚨 Password must include at least 1 special character.")

                if(score == 5 or score == 4):
                    strength = "🟢 Strong Password"
                elif(score == 3):
                    strength = "🟡 Moderate Password, Consider adding more security features"
                else:
                    strength = "🔴 Weak Password"

                st.markdown(f"### {strength}")
                st.progress(score / 5)
                for msg in feedback:
                    st.warning(msg)

            checkPasswordStrength(password)

st.divider()

# Password generation feature
with st.spinner():
    if st.button("Generate Password"):
        def passwordGenerator():
            upper = random.choice(string.ascii_uppercase)
            lower = random.choice(string.ascii_lowercase)
            digit = random.choice(string.digits)
            char = random.choice(string.punctuation)

            remaining = string.ascii_letters + string.digits + string.punctuation
            generated_password = "".join([upper, lower, digit, char] + [random.choice(remaining) for i in range(5)])
            st.success("✅ Strong Password Generated!")
            st.code(generated_password)

        passwordGenerator()
 # Add copyright notice
    st.markdown("© 2025 Mehnazar Syed. All Rights Reserved.")
