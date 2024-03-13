import requests

class Downloader:
    '''Downloads audio files'''
    def __init__(self, url, filename):
        self.url = url
        self.filename = filename 
    
    def download(self):
        response = requests.get(self.url)
        response.raise_for_status()
        with open(self.filename, "wb") as file:
            file.write(response.content)
    
    def __repr__(self):
        return f'<Downloader filename={self.filename}>'