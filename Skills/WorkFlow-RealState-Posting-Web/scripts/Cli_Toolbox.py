#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
RUNTIME_ROOT = SKILL_ROOT / 'references' / 'runtime_contracts'
CONTRACT_PATH = RUNTIME_ROOT / 'SKILL_RUNTIME_CONTRACT.json'

def main() -> int:
    parser = argparse.ArgumentParser(description='Static runtime contract reader')
    parser.add_argument('command', choices=['contract'])
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    payload = json.loads(CONTRACT_PATH.read_text(encoding='utf-8'))
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    print(payload.get('contract_name', 'runtime_contract'))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
