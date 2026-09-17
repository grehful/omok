#!/usr/bin/env python3
"""android/ 아래 XML 리소스가 잘 만들어졌는지 검사한다.

Gradle 의 mergeResources 는 빌드 한참 뒤에야 이런 오류를 알려주므로
(주석 안의 '--' 처럼) 흔한 실수를 CI 앞단에서 몇 초 만에 잡는다.
저장소의 모든 안드로이드 프로젝트(오목, 덕 헌팅)를 한 번에 본다.
"""
import pathlib, sys
from xml.etree import ElementTree as ET

base = pathlib.Path(__file__).resolve().parent.parent
roots = [base / "android"] + sorted(
    d / "android" for d in base.iterdir()
    if d.is_dir() and d.name not in ("node_modules", "android") and not d.name.startswith(".")
)
roots = [r for r in roots if r.is_dir()]

files, bad = [], []
for root in roots:
    files += [p for p in root.rglob("*.xml") if "/build/" not in str(p)]

for p in files:
    try:
        ET.parse(p)
    except ET.ParseError as e:
        bad.append((p.relative_to(base), e))

for path, err in bad:
    print(f"  ✗ {path}: {err}", file=sys.stderr)

names = ", ".join(str(r.relative_to(base)) for r in roots)
print(f"XML 리소스 {len(files)}개 검사({names}), 오류 {len(bad)}건")
sys.exit(1 if bad else 0)
