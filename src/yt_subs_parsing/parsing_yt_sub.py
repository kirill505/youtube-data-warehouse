import os
import argparse
import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi


def yt_parse_url_params(yt_url: str):
    params = {}
    splits = yt_url.split('?')[1].split('&')
    for x in splits:
        name, value = x.split('=')
        params[name] = value

    return params


def yt_get_subtitles(yt_video_id: str):
    srt = YouTubeTranscriptApi.get_transcript(f"{yt_video_id}", languages=['en', 'es'])
    df = pd.json_normalize(srt)
    return df


def yt_save_subs_to_csv(df: pd.DataFrame, root_path: str, filename: str):
    df["youtube_id"] = os.path.basename(filename).split('.')[0]
    df.to_csv(f"{root_path}/{filename}", index=False)


def main(params):
    yt_video_url = params.yt_video_url

    yt_video_id = yt_parse_url_params(yt_video_url)["v"]
    yt_subs = yt_get_subtitles(yt_video_id)
    yt_save_subs_to_csv(yt_subs, params.root_path, f"{yt_video_id}.csv")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--yt_video_url", type=str)
    parser.add_argument("-r", "--root_path", type=str)
    args = parser.parse_args()
    main(args)
