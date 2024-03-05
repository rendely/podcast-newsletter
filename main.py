from summarize import Summarizer

if __name__ == '__main__':
    with open('verge.txt', 'r') as t:
        transcript = t.read()

    pod1 = Summarizer(transcript=transcript, service='openai')
    pod1.summarize()
