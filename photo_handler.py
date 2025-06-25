import base64
from io import BytesIO
from typing import List
from PIL import Image


class ImageMerger:
    _BG = (255, 255, 255)

    @staticmethod
    def _b64_to_pil(uri: str) -> Image.Image:
        if "," in uri:                            # data:image/…;base64,
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

        canvas = Image.new("RGB", (w * cols, h * len(rows)), cls._BG)
        for r, row in enumerate(rows):
            for c, im in enumerate(row):
                canvas.paste(im, (c * w, r * h))

        buf = BytesIO()
        canvas.save(buf, format="PNG")
        canvas.show()
        merged_b64 = base64.b64encode(buf.getvalue()).decode()
        return f"data:image/png;base64,{merged_b64}"
