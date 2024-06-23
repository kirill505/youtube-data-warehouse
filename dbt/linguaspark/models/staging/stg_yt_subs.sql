select *
from {{ source('staging','yt_video_sub_timecodes') }}
