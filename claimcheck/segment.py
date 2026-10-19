"""Sentence segmentation and quote location. All offsets are Python code-point indices
into the unmodified ai_answer string."""
from __future__ import annotations

import re
from dataclasses import dataclass

# A sentence ends at . ? or ! (optionally followed by a closing quote/bracket) when
# whitespace or end of text follows. Decimals like "0.35" have no whitespace after
# the dot, so they never end a sentence.
_SENTENCE_RE = re.compile(r"\S.*?[.?!][\"')\]]*(?=\s|$)|\S.*?$", re.DOTALL)


@dataclass(frozen=True)
class Sentence:
    index: int
    start: int
    end: int
    text: str


def split_sentences(text: str) -> list[Sentence]:
    out: list[Sentence] = []
    for m in _SENTENCE_RE.finditer(text):
        s, e = m.start(), m.end()
        # never let a sentence swallow a paragraph break (it would merge two sentences)
        chunk = text[s:e]
        if "\n\n" in chunk:
            for part in re.finditer(r"[^\n]+", chunk):
                ps, pe = s + part.start(), s + part.end()
                stripped = text[ps:pe].strip()
                if stripped:
                    lead = text[ps:pe].index(stripped[0])
                    out.append(Sentence(len(out), ps + lead, ps + lead + len(stripped), stripped))
            continue
        out.append(Sentence(len(out), s, e, chunk))
    return out


class LocateError(Exception):
    pass


def locate_quotes(text: str, quotes: list[str]) -> list[tuple[int, int]]:
    """Find each quote in the answer. Quotes are matched in the order given, searching
    forward from the previous match; if a quote only exists earlier in the text (model
    returned claims out of order) the first unused occurrence is taken. A quote that does
    not occur, or would reuse/overlap a span already taken, raises LocateError."""
    taken: list[tuple[int, int]] = []
    cursor = 0
    for q in quotes:
        if not q or q != q.strip():
            raise LocateError("quote is empty or has leading/trailing whitespace")
        span = None
        for start_at in (cursor, 0):
            pos = text.find(q, start_at)
            while pos != -1:
                cand = (pos, pos + len(q))
                if not any(cand[0] < e and s < cand[1] for s, e in taken):
                    span = cand
                    break
                pos = text.find(q, pos + 1)
            if span:
                break
        if span is None:
            raise LocateError(f"quote not found verbatim in ai_answer: {q[:80]!r}")
        taken.append(span)
        cursor = span[1]
    return taken
