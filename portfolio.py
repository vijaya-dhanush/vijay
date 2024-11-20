import streamlit as st
import random
import string
from twilio.rest import Client  # For SMS (optional, if sending OTP via SMS)
import  smtplib


st.title("Sign Up Form") 
st.header("Enter The Details Carefully,* Marked Fields are Mandatory") 
st.subheader("Personal Details:")
st.text_input("Enter Your First Name:*",placeholder="Vijay")
st.text_input("Enter Your Last Name:*",placeholder="Dhanush")
st.date_input("Enter Your Date Of Birth:*")
st.text_input("Enter Your Email Address:*",placeholder="johnbritto12@GMAIL.com")
st.number_input("Enter Your Contact Number*", format="%d")


# 1. Define the OTP generation function
def generate_otp():
    otp = ''.join(random.choices(string.digits, k=6))
    return otp

# 2. Define function to send OTP via email
def send_otp_email(email, otp):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("vijayadhanush07@gmail.com", "vijaya@117")  # replace with your credentials
        message = f"Subject: Your OTP Code\n\nYour OTP is {otp}"
        server.sendmail("vijayadhanush07@gmail.com", email, message)
        server.quit()
        return True
    except smtplib.SMTPAuthenticationError:
        st.error("Authentication failed. Please check your email credentials.")
        return False
    except smtplib.SMTPException as e:
        st.error(f"Failed to send OTP: {e}")
        return False


# 3. Define function to send OTP via SMS using Twilio
def send_otp_sms(phone_number, otp):
    account_sid = "AC2c727b97f3859bb0b4621cef03be78c1"
    auth_token = "059291bc468762accd46e26935254f40"
    client = Client(account_sid, auth_token)
    try:
        message = client.messages.create(
            body=f"Your OTP is {otp}",
            from_="9994702656",
            to=phone_number
        )
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

# 4. Streamlit app code
st.title("OTP Authentication System")

if "otp" not in st.session_state:
    st.session_state.otp = None

option = st.selectbox("Select OTP Delivery Method", ("Email", "SMS"))
user_input = st.text_input("Enter your Email" if option == "Email" else "Enter your Phone_Number")

if st.button("Send OTP"):
    otp = generate_otp()
    st.session_state.otp = otp
    if option == "Email":
        if send_otp_email(user_input, otp):
            st.success("OTP sent successfully to your email.")
        else:
            st.error("Failed to send OTP. Check your email and try again.")
    else:
        if send_otp_sms(user_input, otp):
            st.success("OTP sent successfully to your phone.")
        else:
            st.error("Failed to send OTP. Check your phone number and try again.")

user_otp = st.text_input("Enter the OTP", type="password")
if st.button("Verify OTP"):
    if user_otp == st.session_state.otp:
        st.success("OTP verified successfully!")
    else:
        st.error("Incorrect OTP. Please try again.")
 


st.subheader("Educational Details:")
st.text_input("Enter Your School Name:*",placeholder="LFS")
st.number_input("Enter Your 10Th Mark:*", format="%d")
st.number_input("Enter Your 12Th Mark:*", format="%d")
st.number_input("Enter Your Cutoff In 12Th*")
