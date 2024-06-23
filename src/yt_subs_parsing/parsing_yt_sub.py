import os
import argparse
import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi
# from pytube import YouTube


def yt_parse_url_params(yt_url: str):
    params = {}
    splits = yt_url.split('?')[1].split('&')
    for x in splits:
        name, value = x.split('=')
        params[name] = value

    return params


def video_Info(yt_link):
    yt = YouTube(yt_link)  # Create Youtube Object..
    res = {}

    res["Title"] = yt.title
    res["Length"] = yt.length
    res["Views"] = yt.views
    res["Restricted"] = yt.age_restricted
    res["Rating"] = round(yt.rating)
    res["Thumbnail_Url"] = yt.thumbnail_url
    return res


def yt_get_subtitles(yt_video_id: str):
    srt = YouTubeTranscriptApi.get_transcript(f"{yt_video_id}", languages=['en', 'es'])
    df = pd.json_normalize(srt)
    return df


def yt_save_subs_to_csv(df: pd.DataFrame, root_path: str, filename: str):
    df["youtube_id"] = os.path.basename(filename).split('.')[0]
    print(f"{root_path}/{filename}")
    df.to_csv(f"{root_path}/{filename}", index=False)


def fetch_youtube_subtitles(yt_video_url: str, root_path: str):
    yt_video_url = yt_video_url

    yt_video_id = yt_parse_url_params(yt_video_url)["v"]
    yt_subs = yt_get_subtitles(yt_video_id)
    yt_save_subs_to_csv(yt_subs, root_path, f"{yt_video_id}.csv")


# if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument("-u", "--yt_video_url", type=str)
    # parser.add_argument("-r", "--root_path", type=str)
    # args = parser.parse_args()
    # fetch_youtube_subtitles("https://www.youtube.com/watch?v=gsKuETFJr54", "")
