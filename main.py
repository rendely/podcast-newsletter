from summarizer import Summarizer
from transcriber import Transcriber

if __name__ == '__main__':
    # with open('verge.txt', 'r') as t:
    #     transcript = t.read()

    t = Transcriber('o')
    t.transcribe()

    pod1 = Summarizer(transcript=t.transcript, service='ollama')
    pod1.summarize()
