"""
Africa's Talking SMS Integration for STREETMARKET AI
Sandbox environment – completely free for hackathon testing
"""

import os
from pathlib import Path
import africastalking
from dotenv import load_dotenv

# ---- Debug: show current directory and load .env ----
print("Current working directory:", os.getcwd())
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)
print("AT_API_KEY from env:", os.getenv("AT_API_KEY"))
# -----------------------------------------------------

class AfricaTalkingSMS:
    """
    Handles sending SMS via Africa's Talking sandbox.
    Requires AT_USERNAME and AT_API_KEY in .env file.
    """
    def __init__(self):
        # Get credentials from environment
        self.username = os.getenv("AT_USERNAME", "sandbox")   # default is "sandbox"
        self.api_key = os.getenv("AT_API_KEY")

        if not self.api_key:
            raise ValueError(
                "❌ AT_API_KEY not found! "
                "Please set AT_API_KEY in your .env file.\n"
                "Your key looks like: atsk_4fd41b752abd3421c4e427c106e8db83f1a1bc95449b08246fdd25c7fa2b350989847c78"
            )

        # Initialize Africa's Talking SDK
        africastalking.initialize(self.username, self.api_key)
        self.sms = africastalking.SMS

    def send_sms(self, to_number, message):
        """
        Send an SMS to a single recipient.
        Args:
            to_number (str): Phone number with country code (e.g., +2348012345678)
            message (str): SMS content
        Returns:
            dict: Response with status and details
        """
        try:
            # Ensure number has '+' prefix
            if not to_number.startswith('+'):
                to_number = '+' + to_number.lstrip('0')

            # Send the message
            response = self.sms.send(message, [to_number])
            print(f"✅ SMS sent successfully: {response}")
            return {"status": "sent", "response": response}
        except Exception as e:
            print(f"❌ Failed to send SMS: {e}")
            return {"status": "failed", "error": str(e)}

    def send_loan_alert(self, vendor_name, phone_number, loan_amount):
        """
        Send a loan approval alert.
        Args:
            vendor_name (str): Name of the vendor (e.g., "Mama Amina")
            phone_number (str): Recipient phone number
            loan_amount (int): Loan amount in Naira (e.g., 250000)
        Returns:
            dict: Result of send_sms
        """
        # Calculate approximate USD equivalent (using 500 NGN = 1 USD for demo)
        usd_equiv = loan_amount // 500

        message = f"""
🎉 Congratulations {vendor_name}!

Your STREETMARKET AI credit score has reached 0.75. You now qualify for a microloan of ₦{loan_amount:,} (~${usd_equiv:,})!

Reply YES to apply or visit your nearest cooperative office.

- STREETMARKET AI
        """.strip()
        return self.send_sms(phone_number, message)

    def send_price_alert(self, vendor_name, phone_number, product, markup, weekly_savings):
        """
        Send a price arbitrage alert.
        Args:
            vendor_name (str): Name of the vendor
            phone_number (str): Recipient phone number
            product (str): Product name (e.g., "tomatoes")
            markup (int): Markup percentage (e.g., 35)
            weekly_savings (int): Potential weekly savings in Naira
        Returns:
            dict: Result of send_sms
        """
        usd_savings = weekly_savings // 500

        message = f"""
📊 Price Alert for {vendor_name}!

Your {product} prices are {markup}% above wholesale. By joining bulk buying, you could save ₦{weekly_savings:,} per week (~${usd_savings:,})!

Reply HELP for cooperative contacts.

- STREETMARKET AI
        """.strip()
        return self.send_sms(phone_number, message)


# ----------------------------------------------------------------------
# Quick test block – run this file directly to test SMS functionality
# ----------------------------------------------------------------------
if __name__ == "__main__":
    print("🚀 Testing Africa's Talking SMS integration...")
    sms = AfricaTalkingSMS()

    # Ask user for a test phone number
    test_number = input("Enter your phone number with country code (e.g., +2348012345678): ")

    # Send a loan alert test
    result = sms.send_loan_alert(
        vendor_name="Mama Amina",
        phone_number=test_number,
        loan_amount=250000
    )

    if result["status"] == "sent":
        print("\n✅ Test successful! Check your phone or the web simulator.")
        print("If you don't receive the SMS, make sure your number is added to the Sandbox contacts.")
    else:
        print(f"\n❌ Test failed: {result.get('error', 'Unknown error')}")