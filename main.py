from downloader import Downloader
from summarizer import Summarizer
from transcriber import Transcriber
from mail import Mail 

if __name__ == '__main__':
    example_url = 'https://traffic.libsyn.com/secure/wakingup/Making_Sense_361_Will_MacAskill_subscriber.mp3?dest-id=480596'
    d = Downloader(url=example_url)
    t = Transcriber(file_name = d.file_name)
    s = Summarizer(transcript=t.transcript, service='anthropic', file_name=t.file_name)
    s.summarize()
    m = Mail(file_name=t.file_name)
    m.send()
