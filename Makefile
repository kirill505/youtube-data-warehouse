up:
	docker compose --env-file .env up -d --build

etl:
	docker exec etl python /app/src/yt_subs_parsing/parsing_yt_sub.py -r ./data/raw -u https://www.youtube.com/watch?v=uF76d5EmdtU

down:
	docker compose down