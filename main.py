from downloader import Downloader
from summarizer import Summarizer
from transcriber import Transcriber

if __name__ == '__main__':
    # with open('verge.txt', 'r') as t:
    #     transcript = t.read()

    file_name='dctg.mp3'

    d = Downloader(url='https://chrt.fm/track/F62CA2/podcasts.captivate.fm/media/9f0b8b67-02c1-495e-8d87-d90f1e273059/Hasan-Piker-MF.mp3', file_name=file_name)

    d.download()

    breakpoint()

    t = Transcriber(file_name = file_name)
    t.transcribe()

    pod1 = Summarizer(transcript=t.transcript, service='ollama')
    pod1.summarize()
