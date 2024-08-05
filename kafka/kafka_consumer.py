import asyncio
from aiokafka import AIOKafkaConsumer
import json
import aiohttp
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def consume():
    consumer = AIOKafkaConsumer(
        'youtube_tasks',
        bootstrap_servers='broker:29092',
        group_id='youtube_group',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))  # Десериализация сообщений
    )

    await consumer.start()
    try:
        async for msg in consumer:
            await process_message(msg.value)
    finally:
        await consumer.stop()


async def process_message(message):
    try:
        if message['action'] == 'get_top_videos':
            regioncode = message['regioncode']
            limit = message['limit']
            host_ip = '192.168.0.204'  # Замените на IP-адрес вашей хост-машины
            url = f'http://{host_ip}:8000/api/v1/videos/top_videos'
            logger.info(f"Fetching {url} with params: regioncode={regioncode}, limit={limit}")
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params={'regioncode': regioncode, 'limit': limit}) as response:
                    if response.status == 200:
                        logger.info("Successfully fetched top videos")
                    else:
                        logger.error(f"Failed to fetch top videos: {response.status} {await response.text()}")
    except Exception as e:
        logger.error(f"Error processing message: {e}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(consume())
