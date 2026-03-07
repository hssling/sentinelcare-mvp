from __future__ import annotations

import os
import sys
from pathlib import Path

import requests


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: execute_supabase_sql.py <sql-file>", file=sys.stderr)
        return 2

    access_token = os.environ["SUPABASE_ACCESS_TOKEN"]
    project_ref = os.environ["SUPABASE_PROJECT_REF"]
    statements = [item.strip() for item in Path(sys.argv[1]).read_text(encoding="utf-8").split(";") if item.strip()]

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    for statement in statements:
        response = requests.post(
            f"https://api.supabase.com/v1/projects/{project_ref}/database/query",
            headers=headers,
            json={"query": statement + ";", "read_only": False},
            timeout=120,
        )
        if response.status_code >= 400:
            print(f"Failed statement:\n{statement};", file=sys.stderr)
            print(response.text, file=sys.stderr)
            response.raise_for_status()
        if response.text and response.text != "[]":
            print(response.text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
