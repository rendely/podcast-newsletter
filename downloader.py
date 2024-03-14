import requests
import os

class Downloader:
    '''Downloads audio files'''
    def __init__(self, url):
        self.url:str = url
        self.file_name:str = str(hash(url))
    
    def download(self):
        if f'{self.file_name}.mp3' in os.listdir():
            print('File already downloaded')
            return self.file_name

        print(f'Starting download to {self.file_name}.mp3')
        response = requests.get(self.url)
        response.raise_for_status()
        with open(f'{self.file_name}.mp3', "wb") as file:
            file.write(response.content)
        print('Complete')
    
    def convert_to_wav(self):
        #TODO
        pass
    
    def __repr__(self):
        return f'<Downloader file_name={self.file_name}>'