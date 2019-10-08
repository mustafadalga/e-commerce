from django.conf import settings
import requests
import json
import hashlib
import re



MAILCHIP_API_KEY=getattr(settings,"MAILCHIP_API_KEY",None)
MAILCHIP_DATA_CENTER=getattr(settings,"MAILCHIP_DATA_CENTER",None)
MAILCHIP_EMAIL_LIST_ID=getattr(settings,"MAILCHIP_EMAIL_LIST_ID",None)

def check_email(email):
    if not re.match(r".+@.+\..+", email):
        raise ValueError('Geçersiz e-posta adresi!')
    return

def get_subscriber_hash(member_email):
    #check email
    check_email(member_email)
    member_email=member_email.lower().encode()
    m=hashlib.md5(member_email)
    return m.hexdigest()


class Mailchimp(object):
    def __init__(self):
        super(Mailchimp,self).__init__()
        self.key=MAILCHIP_API_KEY
        self.api_url="https://{dc}.api.mailchimp.com/3.0".format(dc=MAILCHIP_DATA_CENTER)
        self.list_id=MAILCHIP_EMAIL_LIST_ID
        self.list_endpoint = '{api_url}/lists/{list_id}'.format(
            api_url=self.api_url,
            list_id=self.list_id
        )

    def get_members_endpoint(self):
        return self.list_endpoint+"/members"


    #  # Abonelik durumunu değiştir
    # def change_subcription_status(self,email,status="unsubscribed"):
    #     hashed_email=get_subscriber_hash(email)
    #     endpoint=self.get_members_endpoint()+"/"+hashed_email
    #     data={
    #         "status":self.check_valid_status(status)
    #     }
    #     r=requests.put(endpoint,auth=("",self.key),data=json.dumps(data))
    #     return r.json()


    def change_subcription_status(self, email, status='unsubscribed'):
        hashed_email = get_subscriber_hash(email)
        endpoint = self.get_members_endpoint() + "/" +  hashed_email
        data = {
            "status": self.check_valid_status(status)
        }
        r = requests.put(endpoint, auth=("", self.key), data=json.dumps(data))
        return r.status_code, r.json()


    def check_valid_status(self,status):
        choices=['subscribed','unsubscribed','cleaned','pending']
        if status not in choices:
            raise ValueError("E-posta durumu için geçerli bir seçim değil") #Not a valid choice for email status
        return status

    # Abonelik durumu
    def check_subcription_status(self,email):
        hashed_email=get_subscriber_hash(email)
        endpoint=self.get_members_endpoint()+"/"+hashed_email
        r=requests.get(endpoint,auth=("",self.key))
        return r.status_code, r.json()

    # Mail adresi ekle
    def add_email(self,email):
        status="subscribed"
        self.check_valid_status(status)
        data={
            "email_address":email,
            "status":status
        }
        endpoint=self.get_members_endpoint()
        r=requests.post(endpoint,auth=("",self.key),data=json.dumps(data))
        return r.status_code, r.json()
        # return self.change_subcription_status(email=email,status=status)

    # Abonelik iptal etme
    def unsubscribe(self,email):
        return self.change_subcription_status(email,status="unsubscribed")

    # Abone olma
    def subscribe(self,email):
        return self.change_subcription_status(email,status="subscribed")

    # Abonelik -> bekleyen
    def pending(self,email):
        return self.change_subcription_status(email,status="pending")