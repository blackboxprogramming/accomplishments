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
const report = { schema: 'blackroad-browser-workflow/1', source_commit: manifest.source_commit, runner_sha256: crypto.createHash('sha256').update(fs.readFileSync(__filename)).digest('hex'), playwright_version: playwrightVersion, browser_executable: executable || null, viewport: { width: 1536, height: 1024 }, modules: results, production_source_modified: false, upstream_assertions_modified: false, network_policy: 'Only the ephemeral loopback static server is permitted. No Host, provider, device or cloud service is started.', started_at_utc: new Date().toISOString() };
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
    await test('negative control: fixture storage read on a blank document', { timeout: 10000 }, async () => {
      // The same first storage access as the upstream startup fixture, but no
      // RoadOS document, script or server resource is loaded in this context.
      const probe = await newContext();
      try {
        await probe.addInitScript(() => { if (localStorage.getItem('startup-test-released')) return; });
        let resolveError;
        const observed = new Promise(resolve => { resolveError = resolve; });
        probe.on('page', p => p.on('pageerror', error => resolveError({ message: String(error), page_url: p.url() })));
        await probe.newPage();
        report.blank_fixture_control = await observed;
        assert.equal(report.blank_fixture_control.page_url, 'about:blank');
        assert.match(report.blank_fixture_control.message, /^SecurityError:.*localStorage.*Access is denied/);
      } finally { await probe.close(); }
    });
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
    activeModule = 'layout observation';
    await test('independent GOAL-aligned desktop geometry', { timeout: 15000 }, async () => {
      const layoutContext = await browser.newContext({ viewport: report.viewport, deviceScaleFactor: 1 });
      try {
        const p = await layoutContext.newPage();
        await p.goto(origin + '/workspace/');
        const computer = p.frameLocator('#computer');
        await computer.locator('[data-computer]').first().waitFor();
        await computer.locator('body').evaluate(() => document.fonts.ready);
        const rect = locator => locator.evaluate(n => { const r = n.getBoundingClientRect(); return { x: r.x, y: r.y, width: r.width, height: r.height, right: r.right, bottom: r.bottom }; });
        const panes = await p.locator('.split-workspace > section').evaluateAll(nodes => nodes.map(n => { const r = n.getBoundingClientRect(); return { x: r.x, y: r.y, width: r.width, height: r.height, right: r.right, bottom: r.bottom }; }));
        const tiles = await computer.locator('.mini-computer').evaluateAll(nodes => nodes.map(n => { const r = n.getBoundingClientRect(); return { x: r.x, y: r.y, width: r.width, height: r.height, right: r.right, bottom: r.bottom }; }));
        const grid = await rect(computer.locator('.computer-grid'));
        const progress = await rect(p.locator('.overall-progress'));
        const audio = await rect(p.locator('.audio-bar'));
        const dock = await rect(p.locator('#workspace-dock'));
        const backgrounds = await computer.locator('.mini-screen').evaluateAll(nodes => nodes.map(n => ({ background: getComputedStyle(n).backgroundImage })));
        const wallpaperLoaded = await computer.locator('body').evaluate(async () => { const img = new Image(); img.src = 'assets/forest-road.jpeg'; await img.decode(); return { width: img.naturalWidth, height: img.naturalHeight }; });
        assert.equal(panes.length, 2); assert.ok(Math.abs(panes[0].width - panes[1].width) < 1);
        assert.equal(tiles.length, 4);
        assert.ok(tiles.every(r => Math.abs(r.width - tiles[0].width) < 1 && Math.abs(r.height - tiles[0].height) < 1));
        assert.ok(Math.abs(tiles[0].y - tiles[1].y) < 1 && Math.abs(tiles[2].y - tiles[3].y) < 1);
        assert.ok(Math.abs(tiles[0].x - tiles[2].x) < 1 && Math.abs(tiles[1].x - tiles[3].x) < 1);
        assert.ok(tiles[1].x > tiles[0].right && tiles[2].y > tiles[0].bottom);
        assert.ok(tiles.every(r => r.x >= grid.x && r.y >= grid.y && r.right <= grid.right + 1 && r.bottom <= grid.bottom + 1));
        assert.ok(backgrounds.every(b => b.background.includes('/desktop/assets/forest-road.jpeg')));
        assert.ok(wallpaperLoaded.width > 0 && wallpaperLoaded.height > 0);
        assert.ok(Math.abs(progress.x - panes[0].x) < 1 && Math.abs(progress.right - panes[1].right) < 1 && progress.bottom < panes[0].y);
        assert.ok(Math.abs(audio.x - panes[0].x) < 1 && Math.abs(audio.right - panes[1].right) < 1 && audio.y > panes[0].bottom && audio.bottom < dock.y);
        report.layout = { panes, tiles, grid, progress, audio, dock, backgrounds, wallpaper: wallpaperLoaded, tolerance_css_px: 1, scope: 'One 1536x1024 Chromium viewport; geometry and loaded asset only, not full visual/accessibility conformance.' };
        await p.mouse.move(10, 40);
        await p.screenshot({ path: 'goal-layout-preview.jpg', type: 'jpeg', quality: 80 });
        await computer.locator('[data-computer]').first().click();
        await computer.locator('#dock').getByRole('button', { name: 'Code', exact: true }).click();
        await computer.locator('[data-roadcode-view="Files"]').click();
        const text = '  Browser evidence 💚\n<script>neverExecute()</script>  ';
        await computer.locator('#code').fill(text);
        await p.locator('#pin').click();
        await p.locator('[data-context="Gaia introduction"]').click();
        assert.equal(await computer.locator('#code').inputValue(), text);
        assert.equal(await p.locator('#pin').getAttribute('aria-pressed'), 'true');
        assert.equal(await p.locator('#context-title').textContent(), 'Gaia introduction');
        await p.screenshot({ path: 'pinned-draft-preview.jpg', type: 'jpeg', quality: 80 });
      } finally { await layoutContext.close(); }
    });
    await test('independent resource and network observation', () => {
      // Do not hide the four existing fixture errors: require their exact known
      // blank-document origin and module count, and reject any other exception.
      const setup = errors.filter(e => e.page_url === 'about:blank' && /^SecurityError:.*localStorage.*Access is denied/.test(e.message) && ['startup-navigation-browser.cjs', 'local-computers-browser.cjs'].includes(e.module));
      report.test_setup_opaque_origin_errors = setup;
      report.application_javascript_errors = errors.filter(e => !setup.includes(e));
      assert.equal(setup.filter(e => e.module === 'startup-navigation-browser.cjs').length, 3);
      assert.equal(setup.filter(e => e.module === 'local-computers-browser.cjs').length, 1);
      assert.deepEqual(report.application_javascript_errors, [], 'JavaScript errors outside the reproduced blank-document fixture case');
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
