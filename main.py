from downloader import Downloader
from summarizer import Summarizer
from transcriber import Transcriber

if __name__ == '__main__':
    example_url = 'https://dts.podtrac.com/redirect.mp3/chrt.fm/track/8DB4DB/pdst.fm/e/pfx.vpixl.com/6qj4J/nyt.simplecastaudio.com/3026b665-46df-4d18-98e9-d1ce16bbb1df/episodes/f282943c-a003-407d-b66a-4c740966cf5c/audio/128/default.mp3?aid=rss_feed&awCollectionId=3026b665-46df-4d18-98e9-d1ce16bbb1df&awEpisodeId=f282943c-a003-407d-b66a-4c740966cf5c&feed=82FI35Px'
    d = Downloader(url=example_url)
    t = Transcriber(file_name = d.file_name)
    s = Summarizer(transcript=t.transcript, service='openai', file_name=t.file_name)
    s.summarize()
