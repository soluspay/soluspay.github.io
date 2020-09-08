"""TA: a client to interact with noebs endpoints.

enhancements:
    build a robust CLI options
    - ./TA.py service_name [--params]

Payment services:
    - card_info
         PAN
         PIN
         expDate
    - tranAmount
    - tranCurrencyCode
"""

import argparse
import enum

import requests
import datetime
import random
import pprint
import click
from Crypto.Cipher import DES
from fire import Fire


EBS_MASTERKEY = "ABCDEF0123456789"
COMMON_REQUESTS_FIELDS = {
    "terminalId": "03000005",
    "terminalId1": "22000764",
    "systemTraceAuditNumber": random.randint(1, 999999),
    "tranDateTime": "",
}

PAYMENT_REQUEST_FIELDS = {"tranAmount": "", "tranCurrencyCode": ""}
CARD_INFO = {"PAN": "", "PIN": "", "expDate": ""}

parser = argparse.ArgumentParser(
    description="Morsal CLI client for perfoming various payments."
)
parser.add_argument(
    "--card-info", type=str, help="List of PAN, PIN, expDate of your card", nargs=3
)
parser.add_argument(
    "--service-path",
    type=str,
    help="Payment service path you want to request",
    required=True,
)
# parser.add_argument("--payee-id", type=str, help="EBS payee id", options=["zain", "mtn", "sudani"])
parser.add_argument("--to-card", type=str, help="The card you'd like to transfer to")
parser.add_argument("--tran-amount", type=float, help="The amount to be transfered")
parser.add_argument(
    "--additional-data",
    type=lambda kv: kv.split("="),
    dest="additional_data",
    help="Any other additional data our users might pass in",
)
parser.add_argument("--terminal-id", type=str, help="the terminal id of pos")
args = parser.parse_args()
print(dict(args._get_kwargs()))
print(dir(args))


class API:
    def __init__(self, request_fields, end_point):
        self.request_fields = request_fields
        self.end_point = end_point

    def get_current_time(self):
        return datetime.datetime.now().isoformat() + "+02:00"

    def get_headers(self):
        """This function returns the header for terminal api."""
        headers = {
            "Content-Type": "application/json",
        }
        return headers

    def prepare_request(self, service_path):
        """Returns common request fields request fields."""
        url = self.end_point + "/" + service_path + "/"
        COMMON_REQUESTS_FIELDS.update(self.request_fields)
        COMMON_REQUESTS_FIELDS.update({"tranDateTime": self.get_current_time()})
        headers = self.get_headers()
        return url, COMMON_REQUESTS_FIELDS, headers

    def send_request(self, url, payload, headers, method="POST"):
        if method == "POST":
            r = requests.post(
                url, json=payload, headers=headers, verify=False, timeout=100
            )
            if r.status_code >= 400:  # FIXME
                raise ValueError(pprint.pprint(r.content))
            return r.json()

    def change_pin_encryption(self, fields):
        return self.prepare_card_fields(fields)

    def get_working_key(self, service_path="workingKey", **kwargs):
        """
        Get EBS workingKey that is used to encrypt PIN block
        """
        url, payload, headers = self.prepare_request(service_path)
        json_response = self.send_request(url, payload, headers)
        return json_response.get("workingKey")


    def transaction(self, request_fields, service_path=None):
        """A generic interface for all Morsal APIs. It is the responsibility of our client to
        check for these fields."""
        url, payload, headers = self.prepare_request(service_path)
        card_fields = self.prepare_card_fields(request_fields)
        payload.update(request_fields)
        try:
        	r = self.send_request(url, payload, headers)
        	print("The response is {}, url is {}".format(r, url))
        except ValueError as e:
        	return e
        return r


    def prepare_card_fields(self, fields, **kwargs):
        """Returns the encrypted PIN block
        fields: dict: contains the pan, pin, and expDate

        output: 
        card_fields: dict: contains pan, pin_block, expDate
        """
        master_key = kwargs.get("master_key", EBS_MASTERKEY)
        pan, pin = fields.get("PAN"), fields.get("PIN")
        new_pin = fields.get("newPIN", "")
        clear_pin_block = self.clear_pin_block(pan, pin)
        working_key = self.get_working_key()
        pin_block = self.encrypted_pin_block(clear_pin_block, working_key, master_key)
        fields.update({"PIN": pin_block})
        if new_pin:
            clear_new_pin_block = self.clear_pin_block(pan, new_pin)
            new_pin_block = self.encrypted_pin_block(
                clear_new_pin_block, working_key, master_key
            )
            fields.update({"newPIN": new_pin_block})
        return fields

    def clear_pin_block(self, pan, pin):
        """This function computes pin block given that we have acquired the working key.
        It computes as following:
            p1 = [0] + [pin_length] + [pin] + [10*f]
            p2 = [0000] + last_12_digits_of_pan_length-1
            clear PIN Block = p1 XOR p2

        #FIXME Maybe this function can be factored into encrpyted_pin_block method
        """
        p1 = "0" + str(len(pin)) + str(pin) + 10 * "f"
        # pan = '6280223242008717812'
        p2 = 4 * "0" + pan[:-1][-12:]  # i hate slicing
        assert len(p2) == len(p1)
        clear_pin_block = hex(int(p1, 16) ^ int(p2, 16))
        return "0" + clear_pin_block[2:]

    def encrypted_pin_block(self, clear_pin_block, working_key, master_key):
        """This function computes the pin block.
        1. decrypt the working key using the masterkey
        2. encrypt the clear pin block using the decrypted working key
        3. return the encrypted pin block
        """
        des_master_key = DES.new(bytes.fromhex(master_key))
        decrypted_working_key = des_master_key.decrypt(bytes.fromhex(working_key))
        assert isinstance(decrypted_working_key, bytes)
        d = DES.new(decrypted_working_key)
        pin_block = d.encrypt(bytes.fromhex(clear_pin_block))
        return pin_block.hex()


class PayeeId(enum.Enum):
    zain_topup = "0010010001"
    mtn_topup = "0010010003"
    sudani_topup = "0010010005"
    zain_billpayment = "0010010002"
    mtn_billpayment = "0010010004"
    sudani_billpayment = "0010010006"
    nec = "0010020001"
    mohe = "0010030002"
    customs = "0010030003"
    mohe_arab = "0010030004"
    e15 = "0010030006"


if __name__ == "__main__":
    local_end_point = "http://localhost:9000/terminal_api"
    prod_end_point = "https://212.0.129.118/terminal_api"
    apn_end_point = "https://192.168.22.99:8080/terminal_api"

    request_fields = {"PAN": "922208170051345212", "PIN": "0000", "expDate": "2203", "newPIN": "0000"}
    m = API(request_fields, end_point=prod_end_point)
    card_transfer_fields = {
       "toCard111": "6391862268977920",
       "toCard1": "9222061700801345465",
       "tranAmount": 2,
    }
    # card_transfer_fields.update(request_fields)
    # card_transfer = m.transaction(card_transfer_fields, service_path="transactions/cardTransfer")
    
    to_card, tran_amount, service_path = (
       args.to_card,
       args.tran_amount,
       args.service_path,
       )
    card_transfer_fields = {
       "toCard": to_card,
       "toCard1": "92220617008013454653",
       "tranAmount": tran_amount,
    }
    card_transfer_fields.update(request_fields)
    bill_payments_fields = {
       "personalPaymentInfo": "0965412059",
       "payeeId": "0010010001",
    }
    card_transfer_fields.update(bill_payments_fields)
    card_registration_fields = {
       "pan": "9222081700040072090",
       "mobile_number": "0925343834",
    }
    card_transfer_fields.update(card_registration_fields)
    card_transfer = m.transaction(card_transfer_fields, service_path=service_path)
    print(card_transfer)
