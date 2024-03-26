import requests
import os
import subprocess
import hashlib

class Downloader:
    '''Downloads audio files'''
    def __init__(self, url):
        self.url:str = url
        self.file_name:str = self.hash_string(url)
        self.file_name_mp3:str = f'{self.file_name}.mp3'
        self.file_name_wav:str = f'{self.file_name}.wav'
        self.run_wave_cmd:str = f'ffmpeg -i {self.file_name_mp3} -ar 16000 -ac 1 -c:a pcm_s16le {self.file_name_wav}'
        self.download()        
    
    def download(self):
        if self.file_name_mp3 in os.listdir():
            print('File already downloaded')
            return self.file_name

        if f'{self.file_name}.txt' in os.listdir():
            print('File already transcribed')
            return self.file_name

        print(f'Starting download to {self.file_name_mp3}')
        response = requests.get(self.url)
        response.raise_for_status()
        with open(self.file_name_mp3, "wb") as file:
            file.write(response.content)
        print('Complete')
        self.convert_to_wav()
        return self.file_name
    
    def convert_to_wav(self):
        if self.file_name_wav in os.listdir():
            print('Already converted to wav')
        
        subprocess.run(self.run_wave_cmd.split(' '))        
    
    def hash_string(self, string):
        encoded_string = string.encode('utf-8')
        hasher = hashlib.sha256()
        hasher.update(encoded_string)
        return hasher.hexdigest()
    
    def __repr__(self):
        return f'<Downloader file_name={self.file_name}>'