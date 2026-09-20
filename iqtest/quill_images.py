"""Compress base64 images embedded in django-quill JSON payloads."""
from __future__ import annotations

import base64
import json
import re
from io import BytesIO
from typing import Any

from PIL import Image

DATA_URI_RE = re.compile(
    r"data:(image/[a-zA-Z0-9.+-]+);base64,([A-Za-z0-9+/=\s]+)",
    re.IGNORECASE,
)


def _compress_image_bytes(
    raw: bytes,
    *,
    max_side: int = 900,
    jpeg_quality: int = 72,
) -> tuple[bytes, str]:
    """Return (bytes, mime) for a resized/compressed image."""
    with Image.open(BytesIO(raw)) as img:
        img.load()
        has_alpha = img.mode in ("RGBA", "LA") or (
            img.mode == "P" and "transparency" in img.info
        )
        work = img.convert("RGBA") if has_alpha else img.convert("RGB")

        w, h = work.size
        longest = max(w, h)
        if longest > max_side:
            scale = max_side / float(longest)
            work = work.resize(
                (max(1, int(w * scale)), max(1, int(h * scale))),
                Image.Resampling.LANCZOS,
            )

        out = BytesIO()
        # Keep transparency as optimized PNG; otherwise JPEG is much smaller.
        if has_alpha:
            work.save(out, format="PNG", optimize=True)
            mime = "image/png"
        else:
            work.save(out, format="JPEG", quality=jpeg_quality, optimize=True)
            mime = "image/jpeg"
        compressed = out.getvalue()

        # Keep original when compression did not help.
        if len(compressed) >= len(raw) and longest <= max_side:
            return raw, ""
        return compressed, mime


def compress_data_uri(
    data_uri: str,
    *,
    max_side: int = 900,
    jpeg_quality: int = 72,
) -> str:
    match = DATA_URI_RE.fullmatch(data_uri.strip())
    if not match:
        return data_uri

    mime = match.group(1).lower()
    if mime in {"image/svg+xml", "image/gif"}:
        return data_uri

    try:
        raw = base64.b64decode(match.group(2), validate=False)
    except Exception:
        return data_uri

    try:
        compressed, new_mime = _compress_image_bytes(
            raw, max_side=max_side, jpeg_quality=jpeg_quality
        )
    except Exception:
        return data_uri

    if not new_mime:
        return data_uri

    encoded = base64.b64encode(compressed).decode("ascii")
    return f"data:{new_mime};base64,{encoded}"


def _walk_ops(ops: list[Any], **kwargs) -> bool:
    changed = False
    for op in ops:
        if not isinstance(op, dict):
            continue
        insert = op.get("insert")
        if isinstance(insert, dict) and "image" in insert:
            original = insert["image"]
            if isinstance(original, str) and original.startswith("data:image"):
                compressed = compress_data_uri(original, **kwargs)
                if compressed != original:
                    insert["image"] = compressed
                    changed = True
    return changed


def compress_quill_json(
    payload: str | dict,
    *,
    max_side: int = 900,
    jpeg_quality: int = 72,
) -> str:
    """
    Compress data-URI images inside a Quill field value (JSON string or dict).
    Returns a JSON string suitable for QuillField.
    """
    data = json.loads(payload) if isinstance(payload, str) else dict(payload)
    kwargs = {"max_side": max_side, "jpeg_quality": jpeg_quality}

    delta = data.get("delta")
    if isinstance(delta, str):
        try:
            delta_obj = json.loads(delta)
        except json.JSONDecodeError:
            delta_obj = None
    elif isinstance(delta, dict):
        delta_obj = delta
    else:
        delta_obj = None

    changed = False
    if isinstance(delta_obj, dict) and isinstance(delta_obj.get("ops"), list):
        changed = _walk_ops(delta_obj["ops"], **kwargs) or changed
        data["delta"] = json.dumps(delta_obj)

    html = data.get("html")
    if isinstance(html, str) and "data:image" in html:

        def _replace(match: re.Match[str]) -> str:
            nonlocal changed
            original = match.group(0)
            compressed = compress_data_uri(original, **kwargs)
            if compressed != original:
                changed = True
            return compressed

        data["html"] = DATA_URI_RE.sub(_replace, html)

    if not changed and isinstance(payload, str):
        return payload
    return json.dumps(data)


def lazy_load_images(html: str) -> str:
    """Add loading/decoding attributes to <img> tags that lack them."""
    if not html or "<img" not in html.lower():
        return html

    def _inject(match: re.Match[str]) -> str:
        tag = match.group(0)
        lower = tag.lower()
        extras = []
        if "loading=" not in lower:
            extras.append('loading="lazy"')
        if "decoding=" not in lower:
            extras.append('decoding="async"')
        if not extras:
            return tag
        return tag[:-1] + " " + " ".join(extras) + ">"

    return re.sub(r"<img\b[^>]*>", _inject, html, flags=re.IGNORECASE)
