from downloader import Downloader
from summarizer import Summarizer
from transcriber import Transcriber

if __name__ == '__main__':
    example_url = 'https://chrt.fm/track/F62CA2/podcasts.captivate.fm/media/9f0b8b67-02c1-495e-8d87-d90f1e273059/Hasan-Piker-MF.mp3'
    d = Downloader(url=example_url)
    t = Transcriber(file_name = d.file_name)
    s = Summarizer(transcript=t.transcript, service='ollama')
    s.summarize()
