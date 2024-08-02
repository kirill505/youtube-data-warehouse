import aiohttp


class YouTubeClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3"

    async def _get(self, url: str, params: dict):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                return await response.json()

    async def get_channel_info(self, channel_id: str):
        url = f"{self.base_url}/channels"
        params = {
            "part": "snippet,statistics",
            "id": channel_id,
            "key": self.api_key
        }
        return await self._get(url, params)

    async def get_video_info(self, video_id: str):
        url = f"{self.base_url}/videos"
        params = {
            "part": "snippet,statistics",
            "id": video_id,
            "key": self.api_key
        }
        return await self._get(url, params)

    async def get_top_videos(self, limit: int = 50):
        url = f"{self.base_url}/videos"
        params = {
            "part": "snippet,statistics",
            "chart": "mostPopular",
            "maxResults": limit,
            "regionCode": "AR",  # Change region code as needed
            "key": self.api_key
        }
        return await self._get(url, params)
