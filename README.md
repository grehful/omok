# 오목 (Omok)

나무 바둑판 위에서 두는 오목. HTML5 캔버스로 만들고 [Capacitor](https://capacitorjs.com/)로
안드로이드 앱으로 포장했습니다. 웹과 앱이 **같은 소스 한 벌**을 씁니다.

## 기능

- **컴퓨터 대국** — 초급 / 중급 / 고급 3단계
  - 위협 패턴 평가 + 알파-베타 가지치기(고급: 4수 읽기, 시간 제한이 걸린 반복 심화)
  - 즉시 오목이 되는 자리와 상대의 오목 자리는 난이도와 무관하게 항상 처리
- **두 사람 대국** — 한 기기에서 번갈아 두기
- **두 번 눌러 착수** — 좁은 화면에서 잘못 놓는 것을 막습니다. 한 번 누르면 미리보기 돌과
  좌표(예: `H8`)가 뜨고, `착수`를 눌러야 확정됩니다. 마우스에서는 기본으로 꺼집니다.
- **무르기** — 컴퓨터 대국에서는 내 수와 컴퓨터 수를 함께 되돌립니다
- **수순 보기** — 돌 위에 착수 번호 표시
- **흑 3·3 금수** (선택) — 흑이 열린 삼을 동시에 두 개 만드는 자리를 금지하는 집 규칙
- 착수음, 전적 저장, 라이트/다크 테마 자동 전환

기본 규칙은 자유 오목입니다 — 가로·세로·대각선으로 다섯 점을 먼저 이으면 이기고,
여섯 점 이상(장목)도 승리로 봅니다.

## 웹에서 바로 하기

https://claude.ai/artifact/HAMfWTSzEJJSWHmewVQ7TA

## APK 받기

`main`에 푸시하면 GitHub Actions가 APK를 빌드합니다.
Actions 탭 → 해당 실행 → Artifacts 에서 `omok-debug-apk`를 내려받아 기기에 설치하세요.
(`omok-release-unsigned-apk`는 서명이 없어 그대로는 설치되지 않습니다. 배포용은 아래 참고.)

## 직접 빌드하기

Android SDK(빌드 도구 + 플랫폼 35)와 JDK 21이 필요합니다.

```bash
npm install
npm run apk          # dist 빌드 → cap sync → gradlew assembleDebug
# 결과물: android/app/build/outputs/apk/debug/app-debug.apk
```

`android/local.properties`에 SDK 경로가 필요할 수 있습니다:

```properties
sdk.dir=/path/to/Android/sdk
```

브라우저에서 확인만 하려면:

```bash
npm run serve        # http://localhost:8080
```

### 스토어 배포용 서명

```bash
keytool -genkey -v -keystore omok.keystore -alias omok \
        -keyalg RSA -keysize 2048 -validity 10000
```

`android/app/build.gradle`의 `android { }` 안에 `signingConfigs`를 추가하고
`buildTypes.release`에서 참조한 뒤 `./gradlew bundleRelease`로 AAB를 만듭니다.
키스토어와 비밀번호는 저장소에 넣지 말고 CI 시크릿이나 `~/.gradle/gradle.properties`에 두세요.

## 구조

```
www/index.html          게임 전체 (마크업·CSS·엔진). Artifact로 게시하는 원본이라
                        <html>/<head> 없이 조각으로 되어 있습니다.
tools/build-android.mjs  위 조각을 <!doctype>·뷰포트·리셋으로 감싸 dist/index.html 생성
tools/gen-icons.py       앱 아이콘과 스플래시 로고 PNG 생성 (의존성 없는 순수 파이썬)
dist/                    Capacitor의 webDir (생성물, 커밋하지 않음)
android/                 Capacitor가 만든 네이티브 프로젝트
```

`www/index.html`을 고쳤으면 `npm run sync`로 안드로이드 쪽에 반영하고,
아이콘 색이나 모양을 바꿨으면 `npm run icons`를 다시 돌리세요.

## 안드로이드 쪽 손본 것

- 세로 모드 고정 (`AndroidManifest.xml`)
- 시스템이 다크 모드면 WebView 안의 `prefers-color-scheme`도 dark가 되도록
  `MainActivity`에서 algorithmic darkening 허용
- 스플래시를 이미지 대신 `layer-list`로 교체 — 라이트/다크 각각 바탕색 사용
  (`res/values/colors.xml`, `res/values-night/colors.xml`)
- 적응형 아이콘 + 모노크롬 아이콘(테마 아이콘 대응)

## 글꼴에 대해

화면 글꼴은 Google Fonts(Gowun Batang, IBM Plex Sans KR)를 CDN에서 불러옵니다.
오프라인이면 안드로이드 기본 한글 글꼴(Noto Sans KR)로 대체되어 레이아웃은 그대로 유지됩니다.
완전한 오프라인 서체가 필요하면 woff2 파일을 `www/`에 받아 `@font-face`로 인라인하세요.
