import requests

url = "https://api.sandbox.africastalking.com/version1/messaging"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded",
    "apiKey": "atsk_4fd41b752abd3421c4e427c106e8db83f1a1bc95449b08246fdd25c7fa2b350989847c78"
}
data = {
    "username": "sandbox",
    "to": "+2347037928226",  # your test number
    "message": "Test SMS from STREETMARKET AI"
}
response = requests.post(url, headers=headers, data=data)
print(response.status_code, response.text)