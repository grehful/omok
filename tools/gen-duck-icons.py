#!/usr/bin/env python3
"""덕 헌팅 앱 아이콘 · 스플래시 로고 생성기 (외부 의존성 없음).

해질녘 하늘을 나는 오리 실루엣을 거리장(SDF)으로 그려 PNG로 내보낸다.
duck/android/.../res 아래 mipmap-*, drawable-* 디렉터리를 직접 채운다.
"""
import math, os

from pnglib import write_png, grad, cov, over, sd_circle, sd_round_rect, sd_ellipse, px_write

RES = os.path.join(os.path.dirname(__file__), "..", "duck", "android", "app", "src", "main", "res")

SKY = [(0.0, (46, 64, 92)), (0.38, (120, 96, 110)), (0.72, (226, 148, 88)), (1.0, (244, 200, 122))]
SUN = (255, 232, 176)
DUCK = (28, 24, 28)          # 하늘 배경 위의 실루엣
DUCK_FG = (232, 196, 96)     # 적응형 아이콘 전경 (어두운 바탕 위)
REED = (32, 34, 30)


def sd_duck(x, y):
    """단위 사각형(0..1) 안을 나는 오리. 부리는 +x 쪽."""
    d = sd_ellipse(x, y, .455, .560, .205, .118, -0.14)          # 몸통
    d = min(d, sd_ellipse(x, y, .620, .478, .080, .048, -0.72))  # 목
    d = min(d, sd_ellipse(x, y, .690, .418, .086, .076, 0.0))    # 머리
    d = min(d, sd_ellipse(x, y, .796, .398, .058, .023, -0.10))  # 부리
    d = min(d, sd_ellipse(x, y, .248, .512, .085, .040, 0.42))   # 꼬리
    d = min(d, sd_ellipse(x, y, .372, .418, .062, .140, 0.52))   # 먼 쪽 날개
    d = min(d, sd_ellipse(x, y, .462, .372, .076, .158, 0.34))   # 가까운 쪽 날개
    return d


def sd_reeds(x, y):
    """아래쪽 갈대 몇 대."""
    d = 9.9
    for cx, h, tilt in ((.17, .16, -0.10), (.30, .11, 0.08), (.82, .14, 0.12), (.70, .09, -0.06)):
        d = min(d, sd_ellipse(x, y, cx, 1.0 - h * .5, .012, h * .5, tilt))
    return d


def render(size, shape, inset=0.0, fg=False):
    """shape: 'squircle' | 'circle' | 'none'(전경 전용, 투명 배경)."""
    S = float(size)
    u = lambda v: v * S
    lo, hi = inset, 1.0 - inset
    span = hi - lo
    c = 0.5
    # 오리를 그릴 지역 좌표로 옮기는 변환
    # 전경 레이어는 오리만 있으므로 실루엣의 외곽 상자를 아이콘 한가운데에 맞춘다
    if shape == "none":
        dscale = span * 1.72
        dx0, dy0 = c - 0.507 * dscale, c - 0.44 * dscale
    else:
        dscale = span * 0.86
        dx0, dy0 = c - dscale * 0.5, c - dscale * 0.52

    px = bytearray(size * size * 4)
    for iy in range(size):
        y = (iy + 0.5) / S
        for ix in range(size):
            x = (ix + 0.5) / S
            col, alpha = (0.0, 0.0, 0.0), 0.0

            if shape != "none":                                   # 하늘 바탕
                d = (sd_round_rect(u(x), u(y), u(c), u(c), u(span / 2), u(span / 2), u(span * 0.22))
                     if shape == "squircle" else sd_circle(u(x), u(y), u(c), u(c), u(span / 2)))
                a = cov(d)
                if a > 0:
                    col, alpha = grad(SKY, (y - lo) / span), a
                    ds = sd_circle(u(x), u(y), u(c - span * .24), u(c - span * .17), u(span * .115))
                    sa = cov(ds) * alpha
                    if sa > 0:
                        col = over(col, SUN, sa)
                    dr = sd_reeds((x - lo) / span, (y - lo) / span) * u(span)
                    ra = cov(dr) * alpha
                    if ra > 0:
                        col = over(col, REED, ra)

            dd = sd_duck((x - dx0) / dscale, (y - dy0) / dscale) * u(dscale)
            a = cov(dd)
            if a > 0:
                if shape == "none":
                    col, alpha = DUCK_FG, max(alpha, a)
                else:
                    col, alpha = over(col, DUCK, a * alpha), alpha

            px_write(px, (iy * size + ix) * 4, col, alpha)
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
