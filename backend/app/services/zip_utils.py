import io, zipfile
from typing import Iterable, Tuple


def unzip_all(buf: bytes) -> list[Tuple[str, bytes]]:
    out = []
    with zipfile.ZipFile(io.BytesIO(buf)) as z:
        for info in z.infolist():
            if info.is_dir():
                continue
            with z.open(info) as f:
                out.append((info.filename, f.read()))
    return out


def zip_pairs(pairs: Iterable[Tuple[str, bytes]]) -> bytes:
    mem = io.BytesIO()
    with zipfile.ZipFile(mem, mode='w', compression=zipfile.ZIP_DEFLATED) as z:
        for name, data in pairs:
            z.writestr(name, data)
    return mem.getvalue()