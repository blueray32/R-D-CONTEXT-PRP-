#!/usr/bin/env python3
import argparse, os, json, uuid, datetime

def ensure_dir(p):
    os.makedirs(p, exist_ok=True)

def new_bundle_dir():
    ts = datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    sid = str(uuid.uuid4())[:8]
    return f"agents/context-bundles/{ts}_{sid}"

def write_event(bundle_dir, kind, payload):
    ensure_dir(bundle_dir)
    path = os.path.join(bundle_dir, 'bundle.jsonl')
    rec = {
        "ts": datetime.datetime.utcnow().isoformat() + "Z",
        "kind": kind,
        "data": payload,
    }
    with open(path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return path

def main():
    ap = argparse.ArgumentParser(description='Append an event to a context bundle (append-only).')
    ap.add_argument('--bundle', default=None, help='Bundle directory (default: create a new one)')
    ap.add_argument('--kind', required=True, choices=['prime','prompt','read','search','key_findings','note'])
    ap.add_argument('--payload', required=True, help='JSON string payload for the event')
    args = ap.parse_args()

    bundle_dir = args.bundle or new_bundle_dir()
    try:
        payload = json.loads(args.payload)
    except Exception as e:
        raise SystemExit(f'Invalid JSON for --payload: {e}')

    path = write_event(bundle_dir, args.kind, payload)
    print(f'Wrote event to {path}')
    print(f'Bundle dir: {bundle_dir}')

if __name__ == '__main__':
    main()
