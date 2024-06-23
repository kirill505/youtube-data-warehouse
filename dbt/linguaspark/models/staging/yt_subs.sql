{{ config(materialized='view') }}

select *
from {{ ref('stg_yt_subs') }}
