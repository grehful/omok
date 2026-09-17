# 오목 · 덕 헌팅

HTML5 캔버스로 만든 게임 두 개를 [Capacitor](https://capacitorjs.com/)로 안드로이드 앱으로
포장했습니다. 각 게임은 웹과 앱이 **같은 소스 한 벌**을 씁니다.

| | 게임 | 소스 | 앱 ID |
|---|---|---|---|
| 🪨 | **오목** — 나무 바둑판 위의 다섯 점 | `www/index.html` | `com.grehful.omok` |
| 🦆 | **덕 헌팅** — 늪지에서 하는 1인칭 오리 사냥 | `duck/www/index.html` | `com.grehful.duckhunt` |

---

## 🪨 오목

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

웹에서 바로 하기: https://claude.ai/artifact/HAMfWTSzEJJSWHmewVQ7TA

## 🦆 덕 헌팅

가로 화면으로 하는 **1인칭 오리 사냥**입니다. 늪지 한가운데 서서 사방을 둘러보며 쏩니다.

- **360도 시야** — 화면을 끌면 시선이 돌아갑니다. 오리는 어느 방향에서든 날아오르고,
  화면 밖에 있으면 가장자리 화살표가 방향을 알려 줍니다(끌 수 있음). 소리도 방향에 따라
  좌우로 갈라져 들립니다.
- **쏘기** — 화면을 툭 치거나 `발사` 버튼. 조준선이 노랗게 변하면 산탄이 닿는 거리입니다.
  탄창은 3발이고 다 쏘면 저절로 장전합니다.
- **라운드제** — 라운드마다 정해진 수만큼 잡아야 다음으로 넘어갑니다. 라운드가 오를수록
  오리가 빨라지고 동시에 더 많이 날아오릅니다.
- **오리 세 종류** — 청둥오리 · 흰뺨검둥오리 · 황금오리(귀하고 빠르고 점수가 큽니다).
  멀수록, 연달아 맞출수록 점수가 높고, 한 발에 두 마리면 보너스입니다.
- **시간대** — 아침 · 한낮 · 노을 · 달밤이 라운드마다 돌아갑니다. 산·나무·갈대·구름·물결까지
  같은 원근 투영으로 그려서 어느 쪽을 봐도 장면이 이어집니다.
- **사냥개** — 라운드가 끝나면 갈대밭에서 올라옵니다. 잡았으면 물고 오고, 못 잡았으면 웃습니다.
- 난이도 3단계, 조준 감도 · 소리 · 진동 설정, 최고 기록 저장

키보드로도 됩니다 — 방향키로 보고, `Space`로 쏘고, `R`로 장전, `Esc`로 멈춤.
마우스로는 화면을 누르면 포인터가 잠기고 그대로 조준할 수 있습니다.

---

## APK 받기

`main`에 푸시하면 GitHub Actions가 두 앱의 APK를 빌드해서 두 곳에 올려둡니다.

**Releases** — 폰에서 받을 때 편합니다. `https://github.com/<사용자명>/omok/releases/latest`
에 `omok-<번호>.apk`, `duckhunt-<번호>.apk`가 파일 그대로 붙어 있어서, 폰 브라우저에서 눌러
바로 설치할 수 있습니다.

**Actions → Artifacts** — `omok-debug-apk`, `duckhunt-debug-apk`. zip으로 내려오므로 압축을
풀어야 합니다. 90일 뒤 자동 삭제됩니다.

Release 단계가 건너뛰어졌다면 저장소 Settings → Actions → General → Workflow permissions 를
**Read and write permissions** 로 바꾸고 다시 빌드하세요. (이 단계가 실패해도 빌드는
성공 처리되므로 Artifacts 로는 항상 받을 수 있습니다.)

`*-release-unsigned-apk`는 서명이 없어 그대로는 설치되지 않습니다. 배포용은 아래 참고.

## 직접 빌드하기

Android SDK(빌드 도구 + 플랫폼 35)와 JDK 21이 필요합니다.

```bash
npm install
npm run apk          # 오목:     dist 빌드 → cap sync → gradlew assembleDebug
npm run apk:duck     # 덕 헌팅:  duck/dist 빌드 → cap sync → gradlew assembleDebug
# 결과물: android/app/build/outputs/apk/debug/app-debug.apk
#         duck/android/app/build/outputs/apk/debug/app-debug.apk
```

`android/local.properties`(와 `duck/android/local.properties`)에 SDK 경로가 필요할 수 있습니다:

```properties
sdk.dir=/path/to/Android/sdk
```

브라우저에서 확인만 하려면:

```bash
npm run serve        # 오목     http://localhost:8080
npm run serve:duck   # 덕 헌팅  http://localhost:8081
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
www/index.html            오목 전체 (마크업·CSS·엔진)
duck/www/index.html       덕 헌팅 전체 (마크업·CSS·엔진)
                          둘 다 Artifact로 게시하는 원본이라 <html>/<head> 없이 조각으로 되어 있습니다.

tools/build-android.mjs   위 조각을 <!doctype>·뷰포트·리셋으로 감싸 dist/index.html 생성
                          (앱 이름을 인자로 받습니다: `node tools/build-android.mjs duck`)
tools/gen-icons.py        오목 아이콘·스플래시 PNG 생성
tools/gen-duck-icons.py   덕 헌팅 아이콘·스플래시 PNG 생성
tools/pnglib.py           두 생성기가 함께 쓰는 PNG·거리장 도우미 (의존성 없는 순수 파이썬)
tools/check-xml.py        두 안드로이드 프로젝트의 XML 리소스 검사 (CI 앞단)

dist/, duck/dist/         Capacitor의 webDir (생성물, 커밋하지 않음)
android/, duck/android/   Capacitor가 만든 네이티브 프로젝트
```

`www/index.html`을 고쳤으면 `npm run sync`, `duck/www/index.html`을 고쳤으면
`npm run sync:duck`으로 안드로이드 쪽에 반영하고, 아이콘 색이나 모양을 바꿨으면
`npm run icons` / `npm run icons:duck`을 다시 돌리세요.

덕 헌팅은 `?test=1`을 붙여 열면 `window.__duck`으로 내부 상태가 열립니다. 자동 점검용입니다.

## 안드로이드 쪽 손본 것

**둘 다**

- 적응형 아이콘 + 모노크롬 아이콘(테마 아이콘 대응)
- 스플래시를 이미지 대신 `layer-list`로 교체 — 바탕색 + 가운데 로고

**오목**

- 세로 모드 고정 (`AndroidManifest.xml`)
- 시스템이 다크 모드면 WebView 안의 `prefers-color-scheme`도 dark가 되도록
  `MainActivity`에서 algorithmic darkening 허용
- 라이트/다크 각각 스플래시 바탕색 (`res/values/colors.xml`, `res/values-night/colors.xml`)

**덕 헌팅**

- 가로 모드 고정 (`sensorLandscape`) — 왼쪽으로 눕히든 오른쪽으로 눕히든 됩니다
- 몰입 모드 — 상태줄·내비게이션 바를 감추고, 사냥 중에는 화면이 꺼지지 않게 합니다
- 진동 권한 (`VIBRATE`) — 명중하면 짧게 울립니다
- 게임 화면이 늘 어두우므로 테마도 다크 고정

## 글꼴에 대해

화면 글꼴은 Google Fonts(Gowun Batang, IBM Plex Sans KR)를 CDN에서 불러옵니다.
오프라인이면 안드로이드 기본 한글 글꼴(Noto Sans KR)로 대체되어 레이아웃은 그대로 유지됩니다.
완전한 오프라인 서체가 필요하면 woff2 파일을 `www/`에 받아 `@font-face`로 인라인하세요.
