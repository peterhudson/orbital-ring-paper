#!/usr/bin/env node
const fs = require('node:fs/promises');
const path = require('node:path');
const os = require('node:os');
const { execFile } = require('node:child_process');
const { promisify } = require('node:util');

const execFileAsync = promisify(execFile);

function buildHtml(markdown, title) {
  return `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>${title}</title>
  <script>
    window.MathJax = {
      tex: {
        inlineMath: [['\\(', '\\)']],
        displayMath: [['\\[', '\\]'], ['$$', '$$']]
      },
      chtml: { scale: 0.96 },
      startup: { typeset: false }
    };
  </script>
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
  <style>
    @page {
      size: 210mm 297mm;
      margin: 16mm 16mm 18mm 16mm;
    }
    :root {
      color-scheme: light;
      --text: #111827;
      --muted: #4b5563;
      --rule: #d1d5db;
      --bg: #ffffff;
      --quote: #f9fafb;
      --code: #f3f4f6;
      --link: #1d4ed8;
    }
    html, body {
      margin: 0;
      padding: 0;
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Inter, Roboto, Helvetica, Arial, sans-serif;
      font-size: 14px;
      line-height: 1.4;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }
    main {
      width: 100%;
      box-sizing: border-box;
    }
    h1, h2, h3, h4 {
      line-height: 1.15;
      margin: 1.1em 0 0.45em;
      page-break-after: avoid;
      break-after: avoid-page;
    }
    h1 {
      font-size: 1.85rem;
      margin-top: 0;
    }
    h2 {
      font-size: 1.32rem;
      padding-top: 0.15rem;
    }
    h3 {
      font-size: 1.08rem;
    }
    p, ul, ol, blockquote, table {
      margin: 0 0 0.82em;
    }
    ul, ol {
      padding-left: 1.2em;
    }
    li + li {
      margin-top: 0.18em;
    }
    hr {
      border: 0;
      border-top: 1px solid var(--rule);
      margin: 1.2em 0;
    }
    blockquote {
      margin-left: 0;
      padding: 0.7em 0.9em;
      border-left: 3px solid var(--rule);
      background: var(--quote);
      color: var(--muted);
    }
    code {
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 0.9em;
      background: var(--code);
      padding: 0.1em 0.28em;
      border-radius: 0.25em;
    }
    pre {
      background: var(--code);
      border-radius: 0.45em;
      padding: 0.8em;
      overflow: auto;
      white-space: pre-wrap;
      word-break: break-word;
    }
    pre code {
      background: transparent;
      padding: 0;
    }
    a {
      color: var(--link);
      text-decoration: none;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.9rem;
    }
    th, td {
      border-bottom: 1px solid var(--rule);
      padding: 0.34em 0.42em;
      text-align: left;
      vertical-align: top;
    }
    thead th {
      font-weight: 700;
      border-bottom: 1.5px solid #9ca3af;
    }
    img {
      max-width: 100%;
    }
    .title {
      margin-bottom: 0.8rem;
    }
    .title p {
      margin: 0.15rem 0 0;
      color: var(--muted);
      font-size: 0.95rem;
    }
    mjx-container[display="true"] {
      margin: 0.7em 0 !important;
      overflow-x: auto;
      overflow-y: hidden;
    }
  </style>
</head>
<body>
  <main id="content" aria-busy="true"></main>
  <script>
    const raw = ${JSON.stringify(markdown)};
    const title = ${JSON.stringify(title)};
    marked.setOptions({ gfm: true, breaks: false, headerIds: false, mangle: false });
    const content = document.getElementById('content');
    content.innerHTML = marked.parse(raw);
    document.title = title;

    const run = async () => {
      if (window.MathJax && window.MathJax.typesetPromise) {
        await window.MathJax.typesetPromise([content]);
      }
      content.setAttribute('aria-busy', 'false');
      document.body.setAttribute('data-rendered', 'true');
    };

    if (document.readyState === 'complete') {
      run();
    } else {
      window.addEventListener('load', () => { run(); });
    }
  </script>
</body>
</html>`;
}

async function renderWithPlaywright(html, outputPath) {
  const { chromium } = require('playwright');
  const browser = await chromium.launch({ executablePath: '/usr/bin/chromium', headless: true, args: ['--no-sandbox'] });
  try {
    const page = await browser.newPage({ viewport: { width: 1240, height: 1754 }, deviceScaleFactor: 1.5 });
    await page.setContent(html, { waitUntil: 'networkidle' });
    await page.waitForFunction(() => document.body.dataset.rendered === 'true', { timeout: 30000 });
    await page.emulateMedia({ media: 'print' });
    await page.pdf({
      path: outputPath,
      printBackground: true,
      preferCSSPageSize: true,
      displayHeaderFooter: true,
      headerTemplate: '<div></div>',
      footerTemplate: '<div style="width:100%; font-size:9px; color:#6b7280; text-align:center; margin:0 auto;"><span class="pageNumber"></span></div>',
      margin: { top: '16mm', right: '16mm', bottom: '18mm', left: '16mm' }
    });
  } finally {
    await browser.close();
  }
}

async function renderWithChromiumCli(html, outputPath) {
  const tempDir = await fs.mkdtemp(path.join(os.tmpdir(), 'openclaw-pdf-'));
  const tempHtmlPath = path.join(tempDir, 'render.html');
  try {
    await fs.writeFile(tempHtmlPath, html, 'utf8');
    await execFileAsync('/usr/bin/chromium', [
      '--headless=new',
      '--disable-gpu',
      '--no-sandbox',
      '--allow-file-access-from-files',
      '--run-all-compositor-stages-before-draw',
      '--virtual-time-budget=30000',
      '--no-pdf-header-footer',
      '--print-to-pdf-no-header',
      `--print-to-pdf=${outputPath}`,
      tempHtmlPath.startsWith('/') ? `file://${tempHtmlPath}` : tempHtmlPath
    ], { maxBuffer: 10 * 1024 * 1024 });
  } finally {
    await fs.rm(tempDir, { recursive: true, force: true });
  }
}

async function main() {
  const [inputArg, outputArg, titleArg] = process.argv.slice(2);
  if (!inputArg || !outputArg) {
    console.error('Usage: node render_mobile_markdown_pdf.cjs <input.md> <output.pdf> [title]');
    process.exit(1);
  }

  const inputPath = path.resolve(inputArg);
  const outputPath = path.resolve(outputArg);
  const title = titleArg || path.basename(inputPath, path.extname(inputPath));
  const markdown = await fs.readFile(inputPath, 'utf8');
  const html = buildHtml(markdown, title);

  await fs.mkdir(path.dirname(outputPath), { recursive: true });

  try {
    await renderWithPlaywright(html, outputPath);
  } catch (error) {
    if (error && error.code !== 'MODULE_NOT_FOUND') {
      console.warn(`Playwright render failed, falling back to Chromium CLI: ${error.message}`);
    }
    await renderWithChromiumCli(html, outputPath);
  }

  console.log(outputPath);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
