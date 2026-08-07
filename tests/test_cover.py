from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from PIL import Image

from vitalimagens.cover import CoverRenderer, CoverSpec, expected_area, load_preset
from vitalimagens.qa import audit_outputs, file_hash


class CoverTests(unittest.TestCase):
    def test_expected_area(self) -> None:
        self.assertEqual(expected_area(20, 0.539), 10.78)
        self.assertEqual(expected_area(50, 0.539), 26.95)
        with self.assertRaises(ValueError):
            expected_area(0, 0.539)

    def test_preset_has_all_fifteen_kits(self) -> None:
        preset = load_preset(Path(__file__).parents[1] / "presets" / "tijolinho-70x77.json")
        self.assertEqual(preset.kits, (2, 3, 4, 5, 6, 8, 10, 12, 15, 18, 20, 25, 30, 40, 50))
        self.assertEqual(len(preset.specs()), 15)
        self.assertEqual(preset.specs()[-1].area_m2, 26.95)

    def test_render_is_square_and_does_not_touch_sources(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            tmp_path = Path(directory)
            white_path = tmp_path / "white.png"
            black_path = tmp_path / "black.png"
            Image.new("RGB", (500, 520), "#f4f4f2").save(white_path)
            Image.new("RGB", (700, 730), "#161616").save(black_path)
            before = {"white": file_hash(white_path), "black": file_hash(black_path)}

            with Image.open(white_path) as white, Image.open(black_path) as black:
                renderer = CoverRenderer(white, black)
            spec = CoverSpec(20, 10.78, "VITAL DECOR", "TIJOLINHO 3D AUTOADESIVO", "70 × 77 CM CADA", "BRANCO OU PRETO")
            output = tmp_path / "cover.png"
            renderer.render(spec).save(output)

            with Image.open(output) as image:
                self.assertEqual(image.size, (1600, 1600))
            self.assertEqual(file_hash(white_path), before["white"])
            self.assertEqual(file_hash(black_path), before["black"])
            audit = audit_outputs([output], before)
            self.assertEqual(audit["alerts"], [])


if __name__ == "__main__":
    unittest.main()
