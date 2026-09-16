/**
 * www/index.html (아티팩트용 조각) -> dist/index.html (안드로이드 WebView 용 완전한 문서)
 *
 * 아티팩트는 게시할 때 <!doctype>/<head>/뷰포트/리셋을 자동으로 씌워 주지만
 * WebView 는 그런 게 없으므로 같은 껍데기를 여기서 직접 붙인다.
 */
import { readFile, writeFile, mkdir } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const src = await readFile(resolve(root, "www/index.html"), "utf8");

// 첫 </style> 까지는 head, 나머지는 body
const cut = src.indexOf("</style>");
if (cut < 0) throw new Error("www/index.html 에서 </style> 를 찾지 못했습니다");
const head = src.slice(0, cut + 8).trim();
const body = src.slice(cut + 8).trim();

const html = `<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover">
<meta name="color-scheme" content="light dark">
<style>
  :root{
    color-scheme: light dark;
    padding-top: env(safe-area-inset-top, 0px);
    padding-bottom: env(safe-area-inset-bottom, 0px);
  }
  img{max-width:100%}
  [hidden]{display:none !important}
  /* 앱답게: 길게 눌러 텍스트 선택·확대 되는 것을 막는다 */
  body{ -webkit-user-select:none; user-select:none; -webkit-touch-callout:none;
        -webkit-tap-highlight-color:transparent; }
</style>
${head}
</head>
<body>
${body}
</body>
</html>
`;

await mkdir(resolve(root, "dist"), { recursive: true });
await writeFile(resolve(root, "dist/index.html"), html);
console.log(`dist/index.html  ${(Buffer.byteLength(html) / 1024).toFixed(1)} KB`);
