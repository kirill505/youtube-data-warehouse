from datetime import datetime
from app.schemas.channel import ChannelCreate, ChannelUpdate
from app.schemas.video import VideoCreate, VideoUpdate
from app.schemas.channel_stats import ChannelStatsCreate
from app.schemas.video_stats import VideoStatsCreate


def parse_channel_info(data):
    channel_data = data["items"][0]
    snippet = channel_data["snippet"]
    statistics = channel_data["statistics"]

    channel = ChannelUpdate(
        channel_id=channel_data["id"],
        channel_name=snippet["title"],
        description=snippet.get("description", ""),
        # created_at=datetime.strptime(snippet["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
        created_at=snippet["publishedAt"]
    )

    stats = ChannelStatsCreate(
        channel_id=channel_data["id"],
        subscriber_count=int(statistics["subscriberCount"]),
        video_count=int(statistics["videoCount"]),
        view_count=int(statistics["viewCount"]),
        last_updated_at=datetime.utcnow()
    )

    return channel, stats


def parse_video_info(data):
    try:
        video_data = data["items"][0]
        snippet = video_data["snippet"]
        statistics = video_data["statistics"]

        published_at = datetime.strptime(snippet["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
        print(f'dfsd {published_at}')
        video = VideoCreate(
            video_id=video_data["id"],  # Добавляем video_id
            channel_id=snippet["channelId"],
            title=snippet["title"],
            description=snippet.get("description", ""),
            published_at=published_at
            # last_updated_at=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        )
        print("Parsed video data:", video)  # Отладочное сообщение

        stats = VideoStatsCreate(
            video_id=video_data["id"],
            view_count=int(statistics["viewCount"]),
            like_count=int(statistics.get("likeCount", 0)),
            comment_count=int(statistics.get("commentCount", 0)),
            last_updated_at=datetime.utcnow()
        )
        print("Parsed stats data:", stats)  # Отладочное сообщение

        return video, stats

    except KeyError as e:
        print("KeyError:", e)
        raise ValueError("Invalid data format received") from e
    except Exception as e:
        print("Exception:", e)
        raise ValueError("Unexpected error occurred while parsing video info") from e
