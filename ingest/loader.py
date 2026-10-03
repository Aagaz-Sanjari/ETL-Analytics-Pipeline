import os
import json
import hashlib

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

insert_stmt = text(
    "insert into raw.ingested_records "
    "(source, dataset, payload, payload_hash, batch_id, ingested_at) "
    "values (:source, :dataset, cast(:payload as jsonb), :payload_hash, "
    "cast(:batch_id as uuid), coalesce(cast(:ingested_at as timestamptz), now())) "
    "on conflict (source, dataset, payload_hash) do nothing"
)


def hash_payload(record):
    return hashlib.sha256(json.dumps(record, sort_keys=True).encode()).hexdigest()


def build_rows(source, dataset, records, batch_id, ingested_at=None):
    if isinstance(records, dict):
        records = [records]
    return [
        {
            "source": source,
            "dataset": dataset,
            "payload": json.dumps(record),
            "payload_hash": hash_payload(record),
            "batch_id": batch_id,
            "ingested_at": ingested_at,
        }
        for record in records
    ]


def insert_rows(rows):
    with engine.begin() as conn:
        conn.execute(insert_stmt, rows)
    return len(rows)