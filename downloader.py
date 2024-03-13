import requests
import os

class Downloader:
    '''Downloads audio files'''
    def __init__(self, url, file_name):
        self.url = url
        self.file_name = file_name 
    
    def download(self):
        if self.file_name in os.listdir():
            print('File already downloaded')
            return 

        print(f'Starting download to {self.file_name}')
        response = requests.get(self.url)
        response.raise_for_status()
        with open(self.file_name, "wb") as file:
            file.write(response.content)
        print('Complete')
    
    def __repr__(self):
        return f'<Downloader file_name={self.file_name}>'