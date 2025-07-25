# app.py
import streamlit as st
import time
import smtplib
from email.message import EmailMessage
import requests
import plotly.graph_objs as go
from twilio.rest import Client as TwilioClient

# Twilio Credentials
TWILIO_SID = 'xxxxxxhadhc'
TWILIO_AUTH = 'xxxxxxhadhc'
TWILIO_PHONE = '+165516548'  # Your Twilio number

# App 
st.title("💸 Crypto Price Tracker")
coin = st.selectbox("Select Cryptocurrency", ["bitcoin", "ethereum", "dogecoin"])
currency = st.selectbox("Currency", ["usd", "inr"])
threshold = st.number_input("Set Alert Price", min_value=0.0, step=1.0)
email = st.text_input("Alert Email (Gmail only)")
start_tracking = st.button("Start Tracking")
phone_number = st.text_input("Alert Phone +91354864684")

# Store historical data
if 'prices' not in st.session_state:
    st.session_state.prices = []

# Email Alert
def send_email_alert(email_to, coin, price):
    msg = EmailMessage()
    msg['Subject'] = f'Crypto Price Alert for {coin.capitalize()}'
    msg['From'] = 'harshilpathak6498@gmail.com'
    msg['To'] = email_to
    msg.set_content(f"The price of {coin} has reached ${price}")
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('harshilpathak6498@gmail.com', 'your_app_password')
        smtp.send_message(msg)

# SMS Alert
def send_sms_alert(to_number, coin, price):
    client = TwilioClient(TWILIO_SID, TWILIO_AUTH)
    message = client.messages.create(
        body=f"🚨 {coin.capitalize()} has reached {price} {currency.upper()}!",
        from_=TWILIO_PHONE,
        to=to_number
    )
    
# Get live price
def get_live_price():
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies={currency}"
    res = requests.get(url).json()
    return res[coin][currency]

if start_tracking:
    placeholder = st.empty()
    while True:
        price = get_live_price()
        st.session_state.prices.append(price)

        with placeholder.container():
            st.metric(label=f"{coin.upper()} Price in {currency.upper()}", value=f"{price:.2f}")
            st.line_chart(st.session_state.prices)

        # Alert if threshold crossed
        if price >= threshold:
            if email:
                send_email_alert(email, coin, price)
                st.warning(f"📧 Email sent to {email}")
                with open("price_alert_log.txt", "a") as f:
                    f.write(f"EMAIL ALERT: {coin} hit {price} {currency.upper()}\n")

            if phone_number:
                send_sms_alert(phone_number, coin, price)
                st.warning(f"📱 SMS sent to {phone_number}")
                with open("price_alert_log.txt", "a") as f:
                    f.write(f"SMS ALERT: {coin} hit {price} {currency.upper()}\n")

        time.sleep(30)  # Refresh every 30 seconds