"""아이콘 생성기가 함께 쓰는 것들 — PNG 쓰기, 색 보간, 간단한 거리장(SDF).

외부 의존성 없이 순수 파이썬으로 32비트 RGBA PNG 를 쓴다.
"""
import math, os, struct, zlib


def write_png(path, w, h, px):
    raw = b"".join(b"\x00" + bytes(px[y * w * 4:(y + 1) * w * 4]) for y in range(h))
    def chunk(tag, data):
        body = tag + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xffffffff)
    ihdr = struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
                + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def lerp(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))


def grad(stops, t):
    t = max(0.0, min(1.0, t))
    for i in range(len(stops) - 1):
        (p0, c0), (p1, c1) = stops[i], stops[i + 1]
        if t <= p1:
            return lerp(c0, c1, (t - p0) / (p1 - p0) if p1 > p0 else 0)
    return stops[-1][1]


def cov(d):
    """부호거리 -> 알파 (1px 안티에일리어싱)."""
    return max(0.0, min(1.0, 0.5 - d))


def over(dst, src, a):
    return tuple(src[i] * a + dst[i] * (1 - a) for i in range(3))


def sd_circle(x, y, cx, cy, r):
    return math.hypot(x - cx, y - cy) - r


def sd_round_rect(x, y, cx, cy, hw, hh, rad):
    qx, qy = abs(x - cx) - (hw - rad), abs(y - cy) - (hh - rad)
    return math.hypot(max(qx, 0), max(qy, 0)) + min(max(qx, qy), 0) - rad


def sd_ellipse(x, y, cx, cy, a, b, rot=0.0):
    """회전한 타원의 근사 거리 — 1px 안티에일리어싱에는 충분하다."""
    dx, dy = x - cx, y - cy
    if rot:
        c, s = math.cos(-rot), math.sin(-rot)
        dx, dy = dx * c - dy * s, dx * s + dy * c
    k = math.hypot(dx / a, dy / b)
    return (k - 1.0) * min(a, b)


def sd_union(*ds):
    return min(ds)


def px_write(px, i, col, alpha):
    px[i] = int(max(0, min(255, col[0])) + 0.5)
    px[i + 1] = int(max(0, min(255, col[1])) + 0.5)
    px[i + 2] = int(max(0, min(255, col[2])) + 0.5)
    px[i + 3] = int(max(0, min(255, alpha * 255)) + 0.5)
