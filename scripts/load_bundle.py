#!/usr/bin/env python3
import argparse, os, json, collections, datetime, re, sys

def load_events(bundle_path):
    events = []
    with open(bundle_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line: 
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return events

def summarize(events):
    reads = []
    key_findings = []
    primes = []
    prompts = []
    for e in events:
        k = e.get('kind')
        d = e.get('data', {})
        if k == 'read':
            item = d.get('path') or d.get('file') or d.get('target')
            if item: reads.append(item)
        elif k == 'key_findings':
            items = d.get('bullets') or d.get('items') or []
            key_findings.extend(items)
        elif k in ('prime','prompt'):
            primes.append(d)

    # dedupe reads preserving order
    seen = set()
    reads_dedup = []
    for r in reads:
        if r not in seen:
            reads_dedup.append(r)
            seen.add(r)

    summary = {
        "reads_dedup": reads_dedup,
        "key_findings": key_findings[:12],
        "primes": primes[-2:]  # last couple of primes/prompts
    }
    return summary

def write_report(summary, outdir='reports/prime'):
    os.makedirs(outdir, exist_ok=True)
    ts = datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    path = os.path.join(outdir, f'bundle_recap_{ts}.md')
    with open(path, 'w', encoding='utf-8') as f:
        f.write('# Bundle Recap\n\n')
        f.write('## Reads (dedup)\n')
        for r in summary['reads_dedup']:
            f.write(f'- {r}\n')
        f.write('\n## Key Findings\n')
        if summary['key_findings']:
            for k in summary['key_findings']:
                f.write(f'- {k}\n')
        else:
            f.write('- (none)\n')
        f.write('\n## Recent Primes/Prompts\n')
        for p in summary['primes']:
            f.write(f'- {json.dumps(p, ensure_ascii=False)}\n')
    return path

def main():
    ap = argparse.ArgumentParser(description='Load a context bundle and print a concise recap.')
    ap.add_argument('bundle', help='Path to bundle.jsonl (e.g., agents/context-bundles/20250101T000000Z_abcd1234/bundle.jsonl)')
    ap.add_argument('--write-report', action='store_true', help='Also write a recap file to reports/prime')
    args = ap.parse_args()

    if not os.path.exists(args.bundle):
        print(f'ERROR: {args.bundle} not found.', file=sys.stderr)
        raise SystemExit(1)

    events = load_events(args.bundle)
    summary = summarize(events)

    print('=== Concise Recap ===')
    print('Reads (dedup):')
    for r in summary['reads_dedup']:
        print(f'- {r}')
    print('\nKey findings:')
    for k in summary['key_findings'] or ['(none)']:
        print(f'- {k}')
    print('\nRecent primes/prompts:')
    for p in summary['primes']:
        print(f'- {json.dumps(p, ensure_ascii=False)}')

    if args.write_report:
        path = write_report(summary)
        print(f'\nReport written to: {path}')

if __name__ == '__main__':
    main()
