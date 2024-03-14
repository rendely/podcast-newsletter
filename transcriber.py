import subprocess
import os

class Transcriber:
    '''Class for transcribing audio'''
    def __init__(self, file_name:str):
        self.file_name:str = file_name
        self.transcript:str|None = None        
        self.run_whisper_cmd:str = f'whisper-cpp/main -f {file_name}.wav -m whisper-cpp/models/ggml-tiny.en.bin -of {file_name} -otxt'
    
    def transcribe(self):        
        if f'{self.file_name}.txt' not in os.listdir():
            subprocess.run(self.run_whisper_cmd.split(' '))
        
        with open(f'{self.file_name}.txt', 'r') as f:
            self.transcript = f.read()