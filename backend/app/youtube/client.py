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

    async def get_top_videos(self, regioncode: str, limit: int = 200):
        url = f"{self.base_url}/videos"
        params = {
            "part": "snippet,statistics",
            "chart": "mostPopular",
            "maxResults": min(limit, 200),
            "regionCode": regioncode,  # Change region code as needed
            "key": self.api_key
        }

        top_videos = []
        while limit > 0:
            response_data = await self._get(url, params)
            top_videos.extend(response_data.get('items', []))
            limit -= len(response_data.get('items', []))
            if 'nextPageToken' in response_data and limit > 0:
                params['pageToken'] = response_data['nextPageToken']
            else:
                break

        return top_videos

    async def search_videos(self, query: str, limit: int = 200):
        url = f"{self.base_url}/search"
        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "maxResults": min(limit, 200),
            "key": self.api_key
        }

        search_results = []
        while limit > 0:
            response_data = await self._get(url, params)
            search_results.extend(response_data.get('items', []))
            limit -= len(response_data.get('items', []))
            if 'nextPageToken' in response_data and limit > 0:
                params['pageToken'] = response_data['nextPageToken']
            else:
                break
        return search_results
