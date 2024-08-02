from datetime import datetime, timezone
from app.schemas.channel import ChannelCreate, ChannelUpdate
from app.schemas.video import VideoCreate, VideoUpdate
from app.schemas.channel_stats import ChannelStatsCreate
from app.schemas.video_stats import VideoStatsCreate
from app.utils.datetime_utils import remove_timezone


async def parse_channel_info(channel_data):
    snippet = channel_data["snippet"]
    statistics = channel_data["statistics"]

    channel = ChannelUpdate(
        channel_id=channel_data["id"],
        channel_name=snippet["title"],
        description=snippet.get("description", ""),
        created_at=snippet["publishedAt"],
        last_updated_at=remove_timezone(datetime.now(timezone.utc))
    )

    stats = ChannelStatsCreate(
        channel_id=channel_data["id"],
        subscriber_count=int(statistics["subscriberCount"]),
        video_count=int(statistics["videoCount"]),
        view_count=int(statistics["viewCount"]),
        last_updated_at=remove_timezone(datetime.now(timezone.utc))
    )

    return channel, stats


async def parse_video_info(video_data):
    try:
        snippet = video_data["snippet"]
        statistics = video_data["statistics"]

        published_at = datetime.strptime(snippet["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
        video = VideoCreate(
            video_id=video_data["id"],  # Добавляем video_id
            channel_id=snippet["channelId"],
            title=snippet["title"],
            description=snippet.get("description", ""),
            published_at=published_at
        )
        print("Parsed video data:", video)  # Отладочное сообщение

        stats = VideoStatsCreate(
            video_id=video_data["id"],
            view_count=int(statistics["viewCount"]),
            like_count=int(statistics.get("likeCount", 0)),
            comment_count=int(statistics.get("commentCount", 0)),
            last_updated_at=remove_timezone(datetime.now(timezone.utc))
        )
        print("Parsed stats data:", stats)  # Отладочное сообщение

        return video, stats

    except KeyError as e:
        print("KeyError:", e)
        raise ValueError("Invalid data format received") from e
    except Exception as e:
        print("Exception:", e)
        raise ValueError("Unexpected error occurred while parsing video info") from e
