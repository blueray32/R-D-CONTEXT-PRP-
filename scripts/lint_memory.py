#!/usr/bin/env python3
import sys, os

PATH = 'memory/concise.md'
MAX_LINES = 50
MAX_TOKENS = 500  # rough cap, whitespace-separated

def main():
    if not os.path.exists(PATH):
        print(f'ERROR: {PATH} not found.', file=sys.stderr)
        sys.exit(1)
    with open(PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.strip().splitlines()
    tokens = content.split()

    ok = True
    if len(lines) > MAX_LINES:
        print(f'FAIL: {PATH} has {len(lines)} lines (max {MAX_LINES}).', file=sys.stderr)
        ok = False
    if len(tokens) > MAX_TOKENS:
        print(f'FAIL: {PATH} has ~{len(tokens)} tokens (max {MAX_TOKENS}).', file=sys.stderr)
        ok = False

    if ok:
        print(f'OK: {PATH} within limits ({len(lines)} lines, ~{len(tokens)} tokens).')
        sys.exit(0)
    else:
        sys.exit(2)

if __name__ == '__main__':
    main()
