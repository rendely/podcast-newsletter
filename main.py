from downloader import Downloader
from summarizer import Summarizer
from transcriber import Transcriber

if __name__ == '__main__':
    example_url = 'https://anchor.fm/s/ef00b398/podcast/play/84555288/https%3A%2F%2Fd3ctxlq1ktw2nl.cloudfront.net%2Fstaging%2F2024-2-26%2F372270935-44100-2-cbeec87f404ad.mp3'
    d = Downloader(url=example_url)
    t = Transcriber(file_name = d.file_name)
    s = Summarizer(transcript=t.transcript, service='openai', file_name=t.file_name)
    s.insights()
