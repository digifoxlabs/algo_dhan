import requests
from config import *

HEADERS = {
    "access-token": ACCESS_TOKEN,
    "client-id": CLIENT_ID,
    "Content-Type": "application/json"
}

class DhanEngine:

    def place_order(self, security_id, qty):
        payload = {
            "transactionType": "BUY",
            "exchangeSegment": "NSE_FNO",
            "productType": "INTRADAY",
            "orderType": "MARKET",
            "securityId": str(security_id),
            "quantity": qty,
            "validity": "DAY"
        }

        r = requests.post(f"{BASE_URL}/orders", headers=HEADERS, json=payload)
        return r.json()

    def kill_switch(self):
        r = requests.post(f"{BASE_URL}/killSwitch", headers=HEADERS)
        return r.json()