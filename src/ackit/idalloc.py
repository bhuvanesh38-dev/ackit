"""Id allocation for `ackit new` (ACF 1.3, ADR-0018).

`ackit.yaml` may carry

    id_allocation:
      strategy: sequential            # default; the next number after the highest one in the bundle
      # strategy: reserved-range      # each author owns a numeric range
      ranges: {alice: [1000, 1999], bob: [2000, 2999]}

With `reserved-range`, two authors on different branches cannot create the same id, because each allocates inside a range
nobody else uses. Ids stay numeric, so every id pattern is unchanged. An author without a range, a missing author, or a full
range is refused with a message, never guessed.
"""
from __future__ import annotations

import re

STRATEGIES = ("sequential", "reserved-range")


class IdAllocationError(ValueError):
    """The id cannot be allocated as configured (missing author, no range for the author, range full)."""


def _is_int(v) -> bool:
    return isinstance(v, int) and not isinstance(v, bool)


def id_config(config: dict) -> tuple[dict, list[str]]:
    """Return (usable config, problems). A bad config falls back to sequential and reports why."""
    raw = (config or {}).get("id_allocation")
    out = {"strategy": "sequential", "ranges": {}}
    if raw is None:
        return out, []
    problems: list[str] = []
    if not isinstance(raw, dict):
        return out, [f"`id_allocation` must be a mapping, got {type(raw).__name__}"]
    strategy = raw.get("strategy", "sequential")
    if strategy not in STRATEGIES:
        problems.append(f"`id_allocation.strategy: {strategy!r}` is not one of {', '.join(STRATEGIES)}")
        strategy = "sequential"
    ranges: dict[str, tuple[int, int]] = {}
    raw_ranges = raw.get("ranges", {})
    if raw_ranges is None:
        raw_ranges = {}
    if not isinstance(raw_ranges, dict):
        problems.append("`id_allocation.ranges` must map an author to [low, high]")
        raw_ranges = {}
    for author, rng in raw_ranges.items():
        if not (isinstance(rng, (list, tuple)) and len(rng) == 2 and all(_is_int(x) for x in rng) and 1 <= rng[0] <= rng[1]):
            problems.append(f"`id_allocation.ranges.{author}: {rng!r}` must be [low, high] with 1 <= low <= high")
            continue
        ranges[str(author)] = (rng[0], rng[1])
    names = sorted(ranges)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            if ranges[a][0] <= ranges[b][1] and ranges[b][0] <= ranges[a][1]:
                problems.append(f"`id_allocation.ranges` of {a} {list(ranges[a])} and {b} {list(ranges[b])} overlap")
    if strategy == "reserved-range" and not ranges:
        problems.append("`id_allocation.strategy: reserved-range` needs at least one range under `ranges`")
    out.update(strategy=strategy, ranges=ranges)
    return out, problems


def allocate(existing: list[str], prefix: str, width: int, config: dict, author: str | None) -> str:
    """The next id for `prefix` given the ids already in the bundle."""
    cfg, problems = id_config(config)
    if problems:
        raise IdAllocationError("`id_allocation` is not usable: " + "; ".join(problems))
    nums = [int(m.group(1)) for i in existing if (m := re.match(rf"^{re.escape(prefix)}(\d+)$", i or ""))]
    if cfg["strategy"] == "sequential":
        n = max(nums) + 1 if nums else 1
    else:
        if not author:
            raise IdAllocationError("id_allocation is reserved-range: pass --author (or set ACKIT_AUTHOR)")
        if author not in cfg["ranges"]:
            raise IdAllocationError(f"author {author!r} has no range under `id_allocation.ranges` (known: {', '.join(sorted(cfg['ranges']))})")
        low, high = cfg["ranges"][author]
        inside = [n for n in nums if low <= n <= high]
        n = max(inside) + 1 if inside else low
        if n > high:
            raise IdAllocationError(f"the range [{low}, {high}] of author {author!r} is full for {prefix}; assign a new range")
    return f"{prefix}{n:0{width}d}"


DEFAULT_RANGE_SIZE = 1000
FIRST_RANGE_START = 1000


def assign_range(config_path, author: str, size: int = DEFAULT_RANGE_SIZE) -> tuple[int, int, str]:
    """Add `author: [low, high]` to `id_allocation.ranges` in `ackit.yaml` and return (low, high, note).

    The block starts after the highest existing range (or at 1000), so it cannot overlap one. Only that one line is added; the
    rest of the file, comments included, is left as it was. Nothing is written when the result would not validate. The line must
    reach the shared branch before the author creates items, otherwise two branches can pick the same block (ACF037 then reports
    the overlap at merge).
    """
    import yaml
    from pathlib import Path
    path = Path(config_path)
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", author or "") or not isinstance(yaml.safe_load(author), str):
        raise IdAllocationError(f"author {author!r} must use letters, digits, '.', '_' and '-' and must not read as a number or boolean in YAML")
    if not _is_int(size) or size < 1:
        raise IdAllocationError("--size must be a positive integer")
    if not path.is_file():
        raise IdAllocationError(f"{path} not found: run this in a bundle that has an ackit.yaml")
    text = path.read_bytes().decode("utf-8")
    crlf = "\r\n" in text
    text = text.replace("\r\n", "\n")
    data = yaml.safe_load(text) or {}
    cfg, problems = id_config(data)
    problems = [x for x in problems if "needs at least one range" not in x]   # the very thing this command fixes
    if problems:
        raise IdAllocationError("fix `id_allocation` first: " + "; ".join(problems))
    if author in cfg["ranges"]:
        raise IdAllocationError(f"author {author!r} already has the range {list(cfg['ranges'][author])}")
    low = max([FIRST_RANGE_START] + [high + 1 for _, high in cfg["ranges"].values()])
    high = low + size - 1
    entry = f"{author}: [{low}, {high}]"
    note = ""
    raw = data.get("id_allocation")
    if raw is None:
        new = text + ("" if text.endswith("\n") or not text else "\n") + f"id_allocation:\n  strategy: reserved-range\n  ranges:\n    {entry}\n"
    else:
        if cfg["strategy"] != "reserved-range":
            note = "the strategy is still `sequential`: set `id_allocation.strategy: reserved-range` for the range to be used"
        lines = text.split("\n")
        top = next((i for i, l in enumerate(lines) if re.match(r"^id_allocation:", l)), None)
        if top is None:
            raise IdAllocationError("cannot edit `id_allocation` automatically; add the line by hand: " + entry)
        end = next((j for j in range(top + 1, len(lines)) if lines[j].strip() and not lines[j].startswith((" ", "\t", "#"))), len(lines))
        block = range(top + 1, end)               # only the lines of the id_allocation block are searched
        idx = next((i for i in block if re.match(r"^\s+ranges:\s*(#.*)?$", lines[i])), None)
        flow = next((i for i in block if re.match(r"^\s+ranges:\s*\{.*\}\s*(#.*)?$", lines[i])), None)
        if idx is not None:                      # block style: add a line after the last indented entry
            base = len(lines[idx]) - len(lines[idx].lstrip())
            last = idx
            for j in range(idx + 1, end):
                if lines[j].strip() and (len(lines[j]) - len(lines[j].lstrip())) > base:
                    last = j
                elif lines[j].strip():
                    break
            indent = " " * ((len(lines[last]) - len(lines[last].lstrip())) if last > idx else base + 2)
            lines.insert(last + 1, f"{indent}{entry}")
        elif flow is not None:                   # one-line mapping: add inside the braces
            empty = re.search(r"\{\s*\}", lines[flow]) is not None
            lines[flow] = re.sub(r"\}(\s*(#.*)?)$", lambda m: ("" if empty else ", ") + entry + "}" + m.group(1), lines[flow])
        elif "ranges" not in raw:               # id_allocation without ranges: add the block under it
            lines.insert(top + 1, f"  ranges:\n    {entry}")
        else:
            raise IdAllocationError("cannot edit `id_allocation` automatically; add the line by hand: " + entry)
        new = "\n".join(lines)
    after, problems = id_config(yaml.safe_load(new) or {})
    if problems or after["ranges"].get(author) != (low, high):
        raise IdAllocationError("the edit would not validate (" + "; ".join(problems or ["range not found after edit"]) + "); add the line by hand: " + entry)
    path.write_bytes((new.replace("\n", "\r\n") if crlf else new).encode("utf-8"))
    return low, high, note
