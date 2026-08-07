from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


def file_hash(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def audit_outputs(files: list[Path], source_hashes: dict[str, str]) -> dict[str, object]:
    items: list[dict[str, object]] = []
    alerts: list[str] = []
    for path in files:
        with Image.open(path) as image:
            item = {
                "file": path.name,
                "width": image.width,
                "height": image.height,
                "mode": image.mode,
                "bytes": path.stat().st_size,
            }
            if image.size != (1600, 1600):
                alerts.append(f"{path.name}: dimensão diferente de 1600x1600")
            if image.mode != "RGB":
                alerts.append(f"{path.name}: modo esperado RGB, recebido {image.mode}")
            items.append(item)
    return {"outputs": items, "source_hashes": source_hashes, "alerts": alerts}


def save_audit(path: str | Path, audit: dict[str, object]) -> None:
    Path(path).write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")


def contact_sheet(files: list[Path], output: str | Path, columns: int = 5) -> None:
    thumb = 300
    rows = (len(files) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * thumb, rows * thumb), "#DED9D0")
    for index, path in enumerate(files):
        with Image.open(path) as image:
            item = image.convert("RGB").resize((thumb, thumb), Image.Resampling.LANCZOS)
        sheet.paste(item, ((index % columns) * thumb, (index // columns) * thumb))
    sheet.save(output, quality=94)

