"""Code lines on documents (ACF 1.3, ADR-0017).

Any document may carry `code_lines: [id, ...]`: the code lines the document is true for. Absent or empty means every line. With an
`environment_registry` configured, every id must be the `code_line` of a known environment (ACF035); without one the ids are free
text. `ackit validate --code-line` and `ackit prompt --code-line` keep only the documents that apply to the line.
"""
from __future__ import annotations


def doc_lines(meta: dict) -> tuple[list[str], str | None]:
    """(the document's code lines, a problem text). An absent or empty field gives ([], None): every line."""
    raw = meta.get("code_lines")
    if raw is None or raw == []:
        return [], None
    if not isinstance(raw, list) or any(not isinstance(x, str) or not x.strip() for x in raw):
        return [], "`code_lines` must be a list of non-empty strings"
    return [x.strip() for x in raw], None


def applies_to_line(meta: dict, line: str | None) -> bool:
    """True when no line is asked for, the document names no line, or it names `line`."""
    line = (line or "").strip()
    if not line:
        return True
    lines, problem = doc_lines(meta)
    return problem is not None or not lines or line in lines


def known_lines(registry) -> set[str]:
    return {e.code_line for e in registry.environments if e.code_line}


def unknown_line_message(registry, line: str) -> str | None:
    """A message when a registry is configured and `line` is not one of its code lines, else None."""
    if registry is None or line.strip() in known_lines(registry):
        return None
    known = sorted(known_lines(registry))
    return f"code line {line!r} is not in the registry (known: {', '.join(known)})" if known else \
        f"code line {line!r} is not in the registry: no environment declares a `code_line`"
