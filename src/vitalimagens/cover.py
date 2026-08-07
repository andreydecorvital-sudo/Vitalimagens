from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFilter, ImageFont


CANVAS = 1600
SAFE = 72
NAVY = "#061D38"
NAVY_PANEL = "#0A2A4D"
GOLD = "#D9A73C"
PAPER = "#F7F3EC"
WHITE = "#FFFFFF"


def _font_path(bold: bool) -> str:
    candidates = (
        [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "C:/Windows/Fonts/arialbd.ttf",
        ]
        if bold
        else [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "C:/Windows/Fonts/arial.ttf",
        ]
    )
    for candidate in candidates:
        if Path(candidate).exists():
            return candidate
    return "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"


def _font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(_font_path(bold), size=size)


def _fit_font(draw: ImageDraw.ImageDraw, text: str, width: int, start: int, minimum: int) -> ImageFont.FreeTypeFont:
    for size in range(start, minimum - 1, -2):
        candidate = _font(size)
        box = draw.textbbox((0, 0), text, font=candidate)
        if box[2] - box[0] <= width:
            return candidate
    return _font(minimum)


def _center_text(draw: ImageDraw.ImageDraw, center_x: int, y: int, text: str, font: ImageFont.FreeTypeFont, fill: str) -> None:
    box = draw.textbbox((0, 0), text, font=font)
    draw.text((center_x - (box[2] - box[0]) / 2, y), text, font=font, fill=fill)


def _shadow(base: Image.Image, box: tuple[int, int, int, int], radius: int = 26) -> None:
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    x1, y1, x2, y2 = box
    draw.rounded_rectangle((x1, y1 + 12, x2, y2 + 12), radius=radius, fill=(0, 0, 0, 44))
    base.alpha_composite(layer.filter(ImageFilter.GaussianBlur(16)))


def _contain(source: Image.Image, size: tuple[int, int], background: str) -> Image.Image:
    """Fit without changing the product's aspect ratio."""
    target = Image.new("RGB", size, background)
    copy = source.copy().convert("RGB")
    copy.thumbnail(size, Image.Resampling.LANCZOS)
    x = (size[0] - copy.width) // 2
    y = (size[1] - copy.height) // 2
    target.paste(copy, (x, y))
    return target


@dataclass(frozen=True)
class CoverSpec:
    quantity: int
    area_m2: float
    brand: str
    product_name: str
    measure: str
    colors_label: str

    @property
    def area_label(self) -> str:
        return f"COBRE ATÉ {self.area_m2:.2f}".replace(".", ",") + " m²"


@dataclass(frozen=True)
class Preset:
    brand: str
    product_name: str
    measure: str
    colors_label: str
    unit_area_m2: float
    white_crop: tuple[int, int, int, int]
    black_crop: tuple[int, int, int, int]
    kits: tuple[int, ...]

    def specs(self) -> list[CoverSpec]:
        return [
            CoverSpec(
                quantity=quantity,
                area_m2=expected_area(quantity, self.unit_area_m2),
                brand=self.brand,
                product_name=self.product_name,
                measure=self.measure,
                colors_label=self.colors_label,
            )
            for quantity in self.kits
        ]


def load_preset(path: str | Path) -> Preset:
    data: dict[str, Any] = json.loads(Path(path).read_text(encoding="utf-8"))
    return Preset(
        brand=str(data["brand"]),
        product_name=str(data["product_name"]),
        measure=str(data["measure"]),
        colors_label=str(data["colors_label"]),
        unit_area_m2=float(data["unit_area_m2"]),
        white_crop=tuple(int(value) for value in data["white_crop"]),
        black_crop=tuple(int(value) for value in data["black_crop"]),
        kits=tuple(int(value) for value in data["kits"]),
    )


class CoverRenderer:
    def __init__(self, white_product: Image.Image, black_product: Image.Image):
        self.white_product = white_product.convert("RGB")
        self.black_product = black_product.convert("RGB")

    @classmethod
    def from_files(cls, white_path: str | Path, black_path: str | Path, preset: Preset) -> "CoverRenderer":
        with Image.open(white_path) as white_source, Image.open(black_path) as black_source:
            white = white_source.convert("RGB").crop(preset.white_crop)
            black = black_source.convert("RGB").crop(preset.black_crop)
        return cls(white, black)

    def render(self, spec: CoverSpec) -> Image.Image:
        image = Image.new("RGBA", (CANVAS, CANVAS), PAPER)
        draw = ImageDraw.Draw(image)

        # Three surfaces create hierarchy without generic decoration.
        draw.rectangle((0, 0, CANVAS, 286), fill=NAVY)
        draw.rectangle((0, 278, CANVAS, 286), fill=GOLD)
        draw.rectangle((0, 1220, CANVAS, CANVAS), fill=NAVY)
        draw.rectangle((0, 1212, CANVAS, 1222), fill=GOLD)

        # Brand is a signature, not the search headline.
        brand_font = _fit_font(draw, spec.brand, 420, 34, 24)
        draw.text((SAFE, 30), spec.brand, font=brand_font, fill=GOLD)

        title = f"KIT {spec.quantity} PLACAS"
        title_font = _fit_font(draw, title, 1450, 132, 92)
        _center_text(draw, 800, 82, title, title_font, WHITE)

        measure_box = (470, 305, 1130, 430)
        _shadow(image, measure_box)
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle(measure_box, radius=38, fill=NAVY_PANEL, outline=GOLD, width=5)
        measure_font = _fit_font(draw, spec.measure, 590, 64, 42)
        _center_text(draw, 800, 333, spec.measure, measure_font, WHITE)

        # Product remains the dominant focus and is never stretched.
        panel_size = (625, 630)
        white_panel = _contain(self.white_product, panel_size, WHITE)
        black_panel = _contain(self.black_product, panel_size, "#111111")
        white_box = (80, 470, 705, 1100)
        black_box = (895, 470, 1520, 1100)
        _shadow(image, white_box, radius=4)
        _shadow(image, black_box, radius=4)
        image.paste(white_panel, white_box[:2])
        image.paste(black_panel, black_box[:2])

        draw = ImageDraw.Draw(image)
        coverage_box = (380, 1082, 1220, 1194)
        draw.rounded_rectangle(coverage_box, radius=38, fill=NAVY_PANEL, outline=GOLD, width=5)
        coverage_font = _fit_font(draw, spec.area_label, 770, 58, 40)
        _center_text(draw, 800, 1104, spec.area_label, coverage_font, WHITE)

        product_font = _fit_font(draw, spec.product_name, 1380, 58, 38)
        _center_text(draw, 800, 1260, spec.product_name, product_font, WHITE)

        colors_box = (390, 1375, 1210, 1505)
        draw.rounded_rectangle(colors_box, radius=32, fill=NAVY_PANEL, outline=GOLD, width=5)
        colors_font = _fit_font(draw, spec.colors_label, 740, 60, 42)
        _center_text(draw, 800, 1403, spec.colors_label, colors_font, GOLD)

        return image.convert("RGB")


def expected_area(quantity: int, unit_area_m2: float) -> float:
    if quantity <= 0 or unit_area_m2 <= 0:
        raise ValueError("quantity and unit_area_m2 must be positive")
    return math.floor((quantity * unit_area_m2 + 0.005) * 100) / 100
