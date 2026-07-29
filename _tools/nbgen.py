"""
nbgen.py  —  chhota helper jo valid Jupyter (.ipynb v4) notebooks banata hai.
Koi external dependency nahi (nbformat ki zaroorat nahi), sirf stdlib json.

Use kaise karein:

    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "_tools"))
    from nbgen import md, code, save

    save("Python/Basics/01_intro.ipynb", [
        md("# Title\n\nExplanation..."),
        code("print('hello')"),
    ])
"""

from __future__ import annotations

import json
import os
import pathlib
import textwrap

# Repo root = _tools ka parent
ROOT = pathlib.Path(__file__).resolve().parents[1]


def _lines(src: str) -> list[str]:
    """String ko nbformat style list-of-lines me todta hai (har line par \n, aakhri par nahi)."""
    src = textwrap.dedent(src).strip("\n")
    parts = src.split("\n")
    return [p + "\n" for p in parts[:-1]] + [parts[-1]] if parts else []


def md(source: str) -> dict:
    """Markdown cell banata hai."""
    return {"cell_type": "markdown", "metadata": {}, "source": _lines(source)}


def code(source: str) -> dict:
    """Code cell banata hai (bina output, execution_count None)."""
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": _lines(source),
    }


def notebook(cells: list[dict]) -> dict:
    """Poora notebook dict (nbformat 4.5)."""
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "version": "3.11",
                "mimetype": "text/x-python",
                "file_extension": ".py",
                "pygments_lexer": "ipython3",
                "nbconvert_exporter": "python",
                "codemirror_mode": {"name": "ipython", "version": 3},
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def save(rel_path: str, cells: list[dict], root: pathlib.Path | None = None) -> pathlib.Path:
    """Notebook ko disk par likhta hai. rel_path repo root ke relative hona chahiye."""
    base = pathlib.Path(root) if root else ROOT
    out = base / rel_path
    out.parent.mkdir(parents=True, exist_ok=True)
    nb = notebook(cells)
    text = json.dumps(nb, indent=1, ensure_ascii=False)
    out.write_text(text + "\n", encoding="utf-8")
    # sanity: dobara parse karke tasdeeq
    json.loads(out.read_text(encoding="utf-8"))
    print(f"[ok] {os.path.relpath(out, base)}  ({len(cells)} cells)")
    return out
