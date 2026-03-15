import smtplib
from email.message import EmailMessage


sender_email = "yug.mistry33@gmail.com"
sender_password = "cegp oxcl aikr qifb"



def send_aurora_alert(target_email:str, lat:float, lon:float, visibility_score:float):
    msg = EmailMessage()
    msg["subject"] = "AURORA ALERT: High Visibility Detected!"

    msg["From"] = sender_email
    msg["TO"] = target_email


    body = f"""
    Space Weather Command Center Alert
    -----------------------------------
    Conditions are optimal for an Aurora sighting at your saved location!
    
    Location: {lat}, {lon}
    Current Visibility Score: {visibility_score}/100
    
    Look north and find a dark spot away from city lights. 
    Good luck hunting!
    
    - Aurora Bot
    """
    msg.set_content(body)



    try:
        print(f"📧 Attempting to send alert to {target_email}...")
        # Connect to Google's SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        print("✅ Alert sent successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False
    
# --- STANDALONE TEST ---
if __name__ == "__main__":
    # Put your own email here so it sends a test to yourself
    test_target = "b25350@students.iitmandi.ac.in" 
    send_aurora_alert(test_target, 45.0, -90.0, 85.5)




