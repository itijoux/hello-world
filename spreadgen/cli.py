"""CLI: generate a travel-book spread from an input JSON file.

    python -m spreadgen.cli samples/bangkok_chinatown.json
    python -m spreadgen.cli samples/bangkok_chinatown.json -o out.json
    python -m spreadgen.cli samples/bangkok_chinatown.json --dry-run

Needs ANTHROPIC_API_KEY in the environment for a live run.
"""

from __future__ import annotations

import argparse
import json
import sys

from .generate import dry_run, generate_spread


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="spreadgen", description=__doc__)
    parser.add_argument("input", help="Path to the spread input JSON file")
    parser.add_argument(
        "-o", "--output", help="Write the generated spread JSON here (default: stdout)"
    )
    parser.add_argument(
        "--effort",
        default="high",
        choices=["low", "medium", "high", "xhigh", "max"],
        help="Thinking/effort level (default: high)",
    )
    parser.add_argument("--max-tokens", type=int, default=8000)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the prompt and output schema without calling the API",
    )
    args = parser.parse_args(argv)

    with open(args.input, encoding="utf-8") as f:
        spread = json.load(f)

    if args.dry_run:
        d = dry_run(spread)
        print("===== SYSTEM PROMPT =====\n")
        print(d.system)
        print("\n===== USER CONTENT =====\n")
        print(d.user_content)
        print("\n===== OUTPUT SCHEMA =====\n")
        print(json.dumps(d.output_schema, ensure_ascii=False, indent=2))
        return 0

    result = generate_spread(
        spread, effort=args.effort, max_tokens=args.max_tokens
    )
    rendered = json.dumps(
        result.output.model_dump(), ensure_ascii=False, indent=2
    )

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(rendered + "\n")
        print(f"Wrote spread to {args.output}", file=sys.stderr)
    else:
        print(rendered)

    u = result.usage
    print(
        f"[usage] input={u.input_tokens} output={u.output_tokens} "
        f"cache_read={getattr(u, 'cache_read_input_tokens', 0)}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
