import base64
from io import BytesIO
from typing import List
from PIL import Image


class ImageMerger:
    _BG = (255, 255, 255)
    _SEP_COLOR = (0, 0, 0)
    _SEP_WIDTH = 5

    @staticmethod
    def _b64_to_pil(uri: str) -> Image.Image:
        if "," in uri:  # data:image/…;base64,
            uri = uri.split(",", 1)[1]
        return Image.open(BytesIO(base64.b64decode(uri)))

    @classmethod
    def merge_rows(cls, *rows_b64: List[str]) -> str:
        rows = [[cls._b64_to_pil(b) for b in row] for row in rows_b64 if row]
        if not rows:
            raise ValueError("Brak obrazów do scalenia")

        w, h = rows[0][0].size
        rows = [[im.resize((w, h)) for im in r] for r in rows]
        cols = max(len(r) for r in rows)

        canvas_width = cols * w + (cols - 1) * cls._SEP_WIDTH
        canvas_height = len(rows) * h + (len(rows) - 1) * cls._SEP_WIDTH

        canvas = Image.new("RGB", (canvas_width, canvas_height), cls._BG)

        for r, row in enumerate(rows):
            y_offset = r * h + r * cls._SEP_WIDTH
            for c, im in enumerate(row):
                x_offset = c * w + c * cls._SEP_WIDTH
                canvas.paste(im, (x_offset, y_offset))

        for r, row in enumerate(rows):
            y_offset = r * h + r * cls._SEP_WIDTH
            for c in range(1, len(row)):
                x_line = c * w + (c - 1) * cls._SEP_WIDTH
                canvas.paste(Image.new("RGB", (cls._SEP_WIDTH, h), cls._SEP_COLOR), (x_line, y_offset))

        for r in range(1, len(rows)):
            y_line = r * h + (r - 1) * cls._SEP_WIDTH
            canvas.paste(Image.new("RGB", (canvas_width, cls._SEP_WIDTH), cls._SEP_COLOR), (0, y_line))

        buf = BytesIO()
        canvas.save(buf, format="PNG")
        canvas.show()
        merged_b64 = base64.b64encode(buf.getvalue()).decode()
        return f"data:image/png;base64,{merged_b64}"