up:
	docker compose --env-file .env up --build -d

etl:
	docker exec etl python /app/src/yt_subs_parsing/parsing_yt_sub.py -r ./data/raw -u https://www.youtube.com/watch?v=uF76d5EmdtU&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=44&ab_channel=DataTalksClub%E2%AC%9B

down:
	docker compose down