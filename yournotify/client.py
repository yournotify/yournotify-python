from __future__ import annotations
import requests
class Yournotify:
    def __init__(self, api_key: str, api_url: str = "https://api.yournotify.com/") -> None:
        self.api_key = api_key
        self.api_url = api_url.rstrip("/") + "/"
    def set_api_url(self, api_url: str): self.api_url = api_url.rstrip("/") + "/"; return self
    def request(self, endpoint: str, method: str = "GET", data: dict | None = None) -> dict:
        url = self.api_url + endpoint.lstrip("/")
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        kwargs = {"headers": headers, "timeout": 30}
        method = method.upper()
        if method == "GET": kwargs["params"] = data or {}
        elif data is not None: kwargs["json"] = data
        return requests.request(method, url, **kwargs).json()
    def send_email(self, name, subject, html, text="", status="draft", from_email="", to=None):
        lists = to if isinstance(to, list) else ([{"email": to}] if to else [])
        return self.request("campaigns/email", "POST", {"name": name, "subject": subject, "html": html, "body": html, "text": text, "from": from_email, "from_email": from_email, "status": status, "channel": "email", "lists": lists})
    def send_sms(self, name, from_sender, text, status="draft", to=None):
        lists = to if isinstance(to, list) else ([{"telephone": to}] if to else [])
        return self.request("campaigns/sms", "POST", {"name": name, "from": from_sender, "sender": from_sender, "text": text, "body": text, "status": status, "channel": "sms", "lists": lists})
    def add_contact(self, email=None, telephone=None, list_id=None, name="", attribs=None):
        lists = [] if list_id is None else (list_id if isinstance(list_id, list) else [list_id])
        return self.request("contacts", "POST", {"email": email, "telephone": telephone, "lists": lists, "name": name, "attribs": attribs or {}})
    def get_contact(self, contact_id): return self.request(f"contacts/{contact_id}")
    def get_contacts(self, params=None): return self.request("contacts", "GET", params or {})
    def update_contact(self, contact_id, email=None, telephone=None, lists=None, name="", attribs=None): return self.request(f"contacts/{contact_id}", "PUT", {"email": email, "telephone": telephone, "lists": lists or [], "name": name, "attribs": attribs or {}})
    def delete_contact(self, contact_id): return self.request(f"contacts/{contact_id}", "DELETE")
    def add_list(self, title, type="public", optin="single"): return self.request("lists", "POST", {"name": title, "title": title, "type": type, "optin": optin})
    def get_list(self, list_id): return self.request(f"lists/{list_id}")
    def get_lists(self, params=None): return self.request("lists", "GET", params or {})
    def update_list(self, list_id, title): return self.request(f"lists/{list_id}", "PUT", {"name": title, "title": title})
    def delete_list(self, list_id): return self.request(f"lists/{list_id}", "DELETE")
    def get_campaign(self, campaign_id): return self.request(f"campaigns/{campaign_id}")
    def get_campaigns(self, channel, params=None): return self.request("campaigns", "GET", {"channel": channel, **(params or {})})
    def update_campaign(self, campaign_id, data=None): return self.request(f"campaigns/{campaign_id}", "PUT", data or {})
    def delete_campaign(self, campaign_id): return self.request(f"campaigns/{campaign_id}", "DELETE")
    def get_campaign_stats(self, ids, channel="email"):
        id_param = ",".join(str(v) for v in ids) if isinstance(ids, list) else ids
        return self.request("campaigns/analytics/stats", "GET", {"id": id_param, "channel": channel})
    def get_campaign_reports(self, ids, channel="email"):
        id_param = ",".join(str(v) for v in ids) if isinstance(ids, list) else ids
        return self.request("campaigns/analytics/reports", "GET", {"id": id_param, "channel": channel})
    def get_profile(self): return self.request("account/profile")
