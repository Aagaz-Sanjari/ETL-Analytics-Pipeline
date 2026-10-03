import os
import glob
import json
import uuid
from datetime import datetime, timezone

from ingest.loader import build_rows, insert_rows

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")


def main():
    for path in sorted(glob.glob(os.path.join(RAW_DIR, "prices_*.json"))):
        stamp = os.path.basename(path)[len("prices_"):-len(".json")]
        ingested_at = (
            datetime.strptime(stamp, "%Y%m%dT%H%M%SZ")
            .replace(tzinfo=timezone.utc)
            .isoformat()
        )
        with open(path) as f:
            records = json.load(f)
        rows = build_rows(
            "coingecko", "markets", records, str(uuid.uuid4()), ingested_at
        )
        insert_rows(rows)
        print(f"{os.path.basename(path)}: processed {len(rows)} records")


if __name__ == "__main__":
    main()