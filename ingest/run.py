import importlib
import uuid

import yaml

from ingest.loader import build_rows, insert_rows


def build_connector(entry):
    module_path, class_name = entry["connector"].rsplit(".", 1)
    connector_class = getattr(importlib.import_module(module_path), class_name)
    return connector_class(entry.get("params"))


def main():
    with open("sources.yml") as f:
        config = yaml.safe_load(f)

    for entry in config["sources"]:
        connector = build_connector(entry)
        records = connector.fetch()
        rows = build_rows(
            connector.source, connector.dataset, records, str(uuid.uuid4())
        )
        insert_rows(rows)
        print(f"{connector.source}/{connector.dataset}: fetched {len(rows)} records")


if __name__ == "__main__":
    main()