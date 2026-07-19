"""PT-BR: Confere os hashes SHA-256 sem abrir os arquivos pickle.

EN-US: Verify result-file SHA-256 hashes without opening the pickle files.
"""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
MANIFEST = DATA_DIR / "SHA256SUMS"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    failures = 0
    for raw_line in MANIFEST.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        expected, filename = line.split(maxsplit=1)
        path = DATA_DIR / filename.strip()
        if not path.is_file():
            print(f"AUSENTE  {filename}")
            failures += 1
            continue
        actual = sha256(path)
        if actual == expected:
            print(f"OK      {filename}")
        else:
            print(f"FALHA   {filename}\n  esperado: {expected}\n  obtido:   {actual}")
            failures += 1
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
