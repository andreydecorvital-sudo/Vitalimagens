from __future__ import annotations

import argparse
from pathlib import Path

from vitalimagens.cover import CoverRenderer, load_preset
from vitalimagens.qa import audit_outputs, contact_sheet, file_hash, save_audit


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Gera capas VITAL DECOR sem alterar o produto")
    parser.add_argument("--preset", required=True, type=Path)
    parser.add_argument("--white", required=True, type=Path)
    parser.add_argument("--black", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    preset = load_preset(args.preset)
    source_hashes = {"white": file_hash(args.white), "black": file_hash(args.black)}
    renderer = CoverRenderer.from_files(args.white, args.black, preset)

    files: list[Path] = []
    for spec in preset.specs():
        path = args.output / f"tijolinho_70x77_kit_{spec.quantity:02d}_capa.png"
        renderer.render(spec).save(path, optimize=True)
        files.append(path)

    contact_sheet(files, args.output / "PREVIA.png")
    audit = audit_outputs(files, source_hashes)
    save_audit(args.output / "audit.json", audit)
    if audit["alerts"]:
        for alert in audit["alerts"]:
            print(f"ALERTA: {alert}")
        return 1
    print(f"{len(files)} capas geradas em {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

