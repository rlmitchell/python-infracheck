import requests


class Endpoint:
    def __init__(self, url):
        self.response = requests.get(url) 
    
    def text_in_response(self, text):
        return text in self.response.text 


