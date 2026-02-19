"""
SMS Mock Logger for STREETMARKET AI Demo
Simulates SMS sending by logging to console and file
"""
from datetime import datetime
import json

class MockSMS:
    """Simulates SMS sending for hackathon demo"""
    
    def __init__(self):
        self.log_file = "sms_log.json"
        self.messages = []
    
    def send_sms(self, to_number, message):
        """Simulate sending SMS"""
        timestamp = datetime.now().isoformat()
        
        sms_record = {
            "timestamp": timestamp,
            "to": to_number,
            "message": message,
            "status": "SIMULATED",
            "delivery": "would_be_sent_in_production"
        }
        
        # Log to console
        print("\n" + "="*60)
        print("📱 SMS SIMULATION")
        print("="*60)
        print(f"To: {to_number}")
        print(f"Time: {timestamp}")
        print(f"Message:\n{message}")
        print("="*60)
        print("✅ In production, this would be sent via Africa's Talking API")
        print("="*60 + "\n")
        
        # Save to log file
        self.messages.append(sms_record)
        with open(self.log_file, 'w') as f:
            json.dump(self.messages, f, indent=2)
        
        return {
            "status": "simulated",
            "message": "SMS logged successfully (production would send via API)",
            "record": sms_record
        }
    
    def send_loan_alert(self, vendor_name, phone_number, loan_amount):
        """Send loan approval alert (simulated)"""
        usd_equiv = loan_amount // 500
        
        message = f"""🎉 Congratulations {vendor_name}!

Your STREETMARKET AI credit score has reached 0.75.

You now qualify for a microloan of:
₦{loan_amount:,} (~${usd_equiv:,} USD)

Reply YES to apply or visit your nearest cooperative office.

- STREETMARKET AI"""
        
        return self.send_sms(phone_number, message)
    
    def send_price_alert(self, vendor_name, phone_number, product, markup, weekly_savings):
        """Send price arbitrage alert (simulated)"""
        usd_savings = weekly_savings // 500
        
        message = f"""📊 Price Alert for {vendor_name}!

Your {product} prices are {markup}% above wholesale.

By joining bulk buying, you could save:
₦{weekly_savings:,}/week (~${usd_savings:,} USD)

Reply HELP for cooperative contacts.

- STREETMARKET AI"""
        
        return self.send_sms(phone_number, message)


# Test the mock
if __name__ == "__main__":
    print("🚀 Testing Mock SMS System...")
    sms = MockSMS()
    
    # Test loan alert
    result = sms.send_loan_alert(
        vendor_name="Mama Amina",
        phone_number="+2347037928226",
        loan_amount=250000
    )
    
    print(f"\n✅ Mock SMS logged successfully!")
    print(f"📄 Check {sms.log_file} for SMS history")
    
    # Test price alert
    result2 = sms.send_price_alert(
        vendor_name="Mama Amina",
        phone_number="+2347037928226",
        product="tomatoes",
        markup=35,
        weekly_savings=3000
    )
    
    print("\n" + "="*60)
    print("DEMO TIP: In your video, show this console output")
    print("and explain: 'In production, this would integrate")
    print("with Africa's Talking API to send real SMS.'")
    print("="*60)