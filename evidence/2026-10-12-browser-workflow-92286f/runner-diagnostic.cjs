'use strict';
// Run unchanged, pinned upstream browser modules; this runner is not RoadOS code.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const crypto = require('node:crypto');
const { test } = require('node:test');

const source = path.resolve(process.argv[2] || '.');
const captures = path.resolve(process.env.ROAD_BROWSER_CAPTURE_DIR || './browser-captures');
const manifest = JSON.parse(fs.readFileSync(path.join(source, 'SOURCE_MANIFEST.json'), 'utf8'));
const playwrightPath = process.env.ROAD_PLAYWRIGHT_MODULE || 'playwright';
const { chromium } = require(playwrightPath);
const playwrightVersion = require(path.join(path.dirname(require.resolve(playwrightPath)), 'package.json')).version;
const executable = process.env.ROAD_CHROMIUM_EXECUTABLE;
const modules = ['startup-navigation-browser.cjs', 'startup-input-browser.cjs', 'document-lifecycle-browser.cjs', 'local-computers-browser.cjs'];
const mime = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.css': 'text/css', '.jpeg': 'image/jpeg', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml' };
const errors = [], blocked = [], requests = [], results = [];
const report = { schema: 'blackroad-browser-workflow/1', source_commit: manifest.source_commit, playwright_version: playwrightVersion, browser_executable: executable || null, viewport: { width: 1536, height: 1024 }, modules: results, production_source_modified: false, upstream_assertions_modified: false, network_policy: 'Only the ephemeral loopback static server is permitted. No Host, provider, device or cloud service is started.', started_at_utc: new Date().toISOString() };
let browser, server, activeModule = 'base desktop';

async function main() {
  fs.mkdirSync(captures, { recursive: true });
  // The original modules use relative screenshot names. Keep output outside source.
  process.chdir(captures);
  try {
    server = http.createServer((req, res) => {
      let relative;
      try { relative = decodeURIComponent(new URL(req.url, 'http://localhost').pathname).replace(/^\/+/, ''); }
      catch { res.writeHead(400).end(); return; }
      if (!relative || relative.endsWith('/')) relative += 'index.html';
      if (relative === 'favicon.ico') { res.writeHead(204).end(); return; }
      const file = path.resolve(source, relative);
      if (!file.startsWith(source + path.sep) || !manifest.files[relative]) {
        requests.push({ method: req.method, path: relative, status: 404 });
        res.writeHead(404).end('Outside the pinned export'); return;
      }
      try {
        const body = fs.readFileSync(file);
        requests.push({ method: req.method, path: relative, status: 200 });
        res.writeHead(200, { 'Content-Type': mime[path.extname(file)] || 'application/octet-stream', 'Cache-Control': 'no-store' }).end(body);
      } catch (error) { requests.push({ method: req.method, path: relative, status: 500 }); res.writeHead(500).end(String(error)); }
    });
    await new Promise((resolve, reject) => { server.once('error', reject); server.listen(0, '127.0.0.1', resolve); });
    const origin = 'http://127.0.0.1:' + server.address().port;
    browser = await chromium.launch(executable ? { executablePath: executable } : {});
    report.browser_version = browser.version();
    if (executable) report.browser_executable_sha256 = crypto.createHash('sha256').update(fs.readFileSync(executable)).digest('hex');
    // Observe each original module's fresh context, without replacing its DOM/storage.
    const newContext = browser.newContext.bind(browser);
    browser.newContext = async options => {
      const context = await newContext(options);
      await context.route('**/*', route => {
        const url = new URL(route.request().url());
        if (url.origin === origin) return route.continue();
        blocked.push({ method: route.request().method(), url: url.href });
        return route.abort('blockedbyclient');
      });
      context.on('page', page => page.on('pageerror', error => errors.push({ message: String(error), stack: error.stack, page_url: page.url(), module: activeModule })));
      return context;
    };
    const context = await browser.newContext({ viewport: report.viewport, deviceScaleFactor: 1 });
    const page = await context.newPage();
    await page.goto(origin + '/desktop/');
    for (const name of modules) {
      activeModule = name;
      const started = performance.now(), item = { module: 'workspace/tests/' + name, status: 'RUNNING' };
      results.push(item);
      await test(name, { timeout: 90000 }, async () => {
        try {
          await require(path.join(source, item.module))(page);
          item.status = 'PASS';
        } catch (error) { item.status = 'FAIL'; item.error = String(error.stack || error); throw error; }
        finally { item.elapsed_ms = Math.round(performance.now() - started); }
      });
    }
    await test('independent resource and network observation', () => {
      assert.deepEqual(errors, [], 'JavaScript errors across all created pages');
      assert.deepEqual(blocked, [], 'Unexpected non-local browser requests');
      assert.deepEqual(requests.filter(r => r.status >= 400), [], 'Every requested export resource must exist');
      assert.ok(requests.some(r => r.path === 'desktop/assets/forest-road.jpeg'), 'Original forest wallpaper must be requested');
      assert.equal(results.length, modules.length);
      assert.ok(results.every(r => r.status === 'PASS'));
    });
  } finally {
    if (browser) await browser.close();
    if (server) await new Promise(resolve => server.close(resolve));
    report.finished_at_utc = new Date().toISOString();
    report.javascript_errors = errors;
    report.blocked_network_requests = blocked;
    report.http_requests = requests;
    report.screenshots = Object.fromEntries(fs.readdirSync(captures).filter(n => n.endsWith('-preview.jpg')).sort().map(name => { const data = fs.readFileSync(path.join(captures, name)); return [name, { bytes: data.length, sha256: crypto.createHash('sha256').update(data).digest('hex') }]; }));
    fs.writeFileSync(path.join(captures, 'browser-report.json'), JSON.stringify(report, null, 2) + '\n');
  }
}

main().catch(error => { console.error(error); process.exitCode = 1; });
