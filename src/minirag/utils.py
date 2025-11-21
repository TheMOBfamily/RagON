from __future__ import annotations
import time
from contextlib import contextmanager
from typing import Iterator
from rich.console import Console

console = Console()


@contextmanager
def timed(message: str) -> Iterator[None]:
    start = time.time()
    try:
        yield
    finally:
        dur = time.time() - start
        console.print(f"[bold cyan]{message}[/]: [green]{dur:.2f}s")
