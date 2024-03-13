import subprocess

class Transcriber:
    '''Class for transcribing audio'''
    def __init__(self, file_name:str):
        self.file_name:str = file_name
        self.transcript:str|None = None
        self.transcribe()
        self.run_whisper_cmd:str = f'whisper-cpp/main -f whisper-cpp/data/{file_name}.wav -m whisper-cpp/models/ggml-tiny.en.bin -of whisper-cpp/data/{file_name} -otxt'
    
    
    def transcribe(self):
        if self.file_name in os.listdir():
            print('Already transcribed')
            return 
    
        subprocess.run(self.run_whisper_cmd.split(' '))
        with open(f'whisper-cpp/data/{self.file_name}.txt', 'r') as f:
            self.transcript = f.read()