"""Build the Rel-16 topic-ID lookup from the links in the topic records."""
import argparse
import json
import posixpath
from pathlib import Path


def projection(release):
    topics = json.loads((release / "topics.json").read_text(encoding="utf-8"))["topics"]
    ids, paths = set(), {}
    for topic in topics:
        ident, page = topic["id"], topic["path"]
        if ident in ids:
            raise ValueError(f"duplicate topic ID: {ident}")
        ids.add(ident)
        for name in (page, topic["knowledge_record"], posixpath.splitext(page)[0]):
            path = posixpath.normpath(name)
            if path in paths:
                raise ValueError(f"ambiguous path or alias {path}: {paths[path]} / {ident}")
            paths[path] = ident
        if not (release / page).is_file():
            raise ValueError(f"{ident}: missing Markdown page {page}")
    result = {}
    for topic in topics:
        record = json.loads((release / topic["knowledge_record"]).read_text(encoding="utf-8"))
        if record["topic_id"] != topic["id"]:
            raise ValueError(f"{topic['knowledge_record']}: expected topic_id {topic['id']}")
        directory = posixpath.dirname(topic["knowledge_record"])
        related = []
        for key in ("related", "related_topics"):
            for ref in record.get(key, []):
                # Both ID and relative-path spellings occur in existing records.
                local = paths.get(posixpath.normpath(posixpath.join(directory, ref)))
                if ref in ids and local is not None and local != ref:
                    raise ValueError(f"{topic['id']}: {ref} names both an ID and a path to {local}")
                if ref not in ids and local is None:
                    raise ValueError(f"{topic['id']}: unknown relation target {ref}")
                related.append(ref if ref in ids else local)
        if related:
            result[topic["id"]] = related
    return {"release": 16, "related_by_id": result}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="compare without writing")
    args = parser.parse_args()
    directory = Path(__file__).resolve().parents[1] / "releases" / "rel-16"
    view = directory / "topic-relations.json"
    data = (json.dumps(projection(directory), ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    if args.check:
        if not view.exists() or view.read_bytes() != data:
            raise SystemExit("Rel-16 topic-relations.json needs regeneration")
    else:
        view.write_bytes(data)
