#!/usr/bin/env python3
"""오목 앱 아이콘 · 스플래시 로고 생성기 (외부 의존성 없음).

나무판 위의 흑돌·백돌을 거리장(SDF)으로 그려 PNG로 내보낸다.
res/ 아래 mipmap-*, drawable-* 디렉터리를 직접 채운다.
"""
import os

from pnglib import write_png, grad, cov, over, sd_circle, sd_round_rect
import math

RES = os.path.join(os.path.dirname(__file__), "..", "android", "app", "src", "main", "res")

WOOD_A, WOOD_B = (229, 187, 130), (198, 145, 63)
GRID = (74, 52, 24)
BLACK_STOPS = [(0.0, (120, 120, 134)), (0.42, (43, 43, 51)), (1.0, (8, 8, 12))]
WHITE_STOPS = [(0.0, (255, 255, 255)), (0.5, (244, 240, 228)), (1.0, (196, 188, 170))]


def render(size, shape, inset=0.0):
    """shape: 'squircle' | 'circle' | 'none'(투명 배경) — inset은 여백 비율."""
    S = float(size)
    u = lambda v: v * S                       # 단위 좌표 -> 픽셀
    lo, hi = inset, 1.0 - inset
    span = hi - lo
    c = 0.5
    r_stone = span * 0.185
    sep = span * 0.092
    b_cx, b_cy = c - sep, c - sep
    w_cx, w_cy = c + sep, c + sep
    lw = span * 0.020
    reach = span * (0.30 if shape == "none" else 0.75)   # 판 밖으로 나가는 선은 바탕 알파에 클리핑된다

    px = bytearray(size * size * 4)
    for iy in range(size):
        y = (iy + 0.5) / S
        for ix in range(size):
            x = (ix + 0.5) / S
            col, alpha = (0.0, 0.0, 0.0), 0.0

            # 1. 나무판 바탕
            if shape != "none":
                d = (sd_round_rect(u(x), u(y), u(c), u(c), u(span / 2), u(span / 2), u(span * 0.22))
                     if shape == "squircle" else sd_circle(u(x), u(y), u(c), u(c), u(span / 2)))
                a = cov(d)
                if a > 0:
                    t = ((x - lo) + (y - lo)) / (2 * span)
                    wood = grad([(0.0, WOOD_A), (0.5, WOOD_B), (1.0, WOOD_A)], t)
                    vig = 1.0 - 0.16 * min(1.0, math.hypot(x - c, y - c) / (span * 0.62)) ** 2
                    col, alpha = tuple(v * vig for v in wood), a

            # 2. 격자 (돌 뒤)
            for gx in (b_cx, w_cx):
                d = max(abs(u(x) - u(gx)) - u(lw) / 2, abs(u(y) - u(c)) - u(reach))
                a = cov(d) * 0.52 * (alpha if shape != "none" else 1.0)
                if a > 0:
                    col, alpha = over(col, GRID, a), max(alpha, a)
            for gy in (b_cy, w_cy):
                d = max(abs(u(y) - u(gy)) - u(lw) / 2, abs(u(x) - u(c)) - u(reach))
                a = cov(d) * 0.52 * (alpha if shape != "none" else 1.0)
                if a > 0:
                    col, alpha = over(col, GRID, a), max(alpha, a)

            # 3. 돌 그림자 + 돌
            for (scx, scy, stops) in ((b_cx, b_cy, BLACK_STOPS), (w_cx, w_cy, WHITE_STOPS)):
                ds = sd_circle(u(x), u(y), u(scx), u(scy) + u(span * 0.012), u(r_stone) + u(span * 0.012))
                a = cov(ds) * 0.30
                if a > 0 and (alpha > 0 or shape == "none"):
                    col, alpha = over(col, (58, 38, 14), a), max(alpha, a * 0.9)
                d = sd_circle(u(x), u(y), u(scx), u(scy), u(r_stone))
                a = cov(d)
                if a > 0:
                    dx = (x - scx) / r_stone + 0.34
                    dy = (y - scy) / r_stone + 0.40
                    col = over(col, grad(stops, min(1.0, math.hypot(dx, dy) / 1.08)), a)
                    alpha = max(alpha, a)

            o = (iy * size + ix) * 4
            px[o] = int(max(0, min(255, col[0])) + 0.5)
            px[o + 1] = int(max(0, min(255, col[1])) + 0.5)
            px[o + 2] = int(max(0, min(255, col[2])) + 0.5)
            px[o + 3] = int(max(0, min(255, alpha * 255)) + 0.5)
    return px


JOBS = [
    # (하위경로, 파일명, 크기, 모양, 여백)
    ("mipmap-%s", "ic_launcher.png",            {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}, "squircle", 0.02),
    ("mipmap-%s", "ic_launcher_round.png",      {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}, "circle", 0.0),
    ("mipmap-%s", "ic_launcher_foreground.png", {"mdpi": 108, "hdpi": 162, "xhdpi": 216, "xxhdpi": 324, "xxxhdpi": 432}, "none", 0.255),
    ("drawable-%s", "splash_logo.png",          {"mdpi": 96, "hdpi": 144, "xhdpi": 192, "xxhdpi": 288, "xxxhdpi": 384}, "squircle", 0.04),
]

if __name__ == "__main__":
    for tmpl, name, sizes, shape, inset in JOBS:
        for dens, size in sizes.items():
            out = os.path.join(RES, tmpl % dens, name)
            write_png(out, size, size, render(size, shape, inset))
            print(f"  {out.split('/res/')[1]:46s} {size}px")
    print("done")
