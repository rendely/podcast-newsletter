from downloader import Downloader
from summarizer import Summarizer
from transcriber import Transcriber

if __name__ == '__main__':
    example_url = 'https://pdst.fm/e/media.transistor.fm/f9a6fd57/c5a738c3.mp3'
    d = Downloader(url=example_url)
    t = Transcriber(file_name = d.file_name)
    s = Summarizer(transcript=t.transcript, service='openai', file_name=t.file_name)
    s.summarize()
