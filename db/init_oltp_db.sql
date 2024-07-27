CREATE TABLE channels (
    channel_id VARCHAR PRIMARY KEY,
    channel_name VARCHAR,
    description TEXT,
    created_at TIMESTAMP,
    last_updated_at TIMESTAMP
);

CREATE TABLE videos (
    video_id VARCHAR PRIMARY KEY,
    channel_id VARCHAR REFERENCES channels(channel_id),
    title VARCHAR,
    description TEXT,
    published_at TIMESTAMP,
    last_updated_at TIMESTAMP
);

CREATE TABLE channel_stats (
    id SERIAL PRIMARY KEY,
    channel_id VARCHAR REFERENCES channels(channel_id),
    subscriber_count INT,
    video_count INT,
    view_count BIGINT,
    last_updated_at TIMESTAMP
);

CREATE TABLE video_stats (
    id SERIAL PRIMARY KEY,
    video_id VARCHAR REFERENCES videos(video_id),
    view_count BIGINT,
    like_count INT,
    comment_count INT,
    last_updated_at TIMESTAMP
);
