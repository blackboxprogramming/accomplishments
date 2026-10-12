'use strict';
// Qualification infrastructure only. Upstream RoadWork sources/tests are unchanged.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const crypto = require('node:crypto');
const { test } = require('node:test');
const source = path.resolve(process.argv[2] || '.');
const captures = path.resolve(process.env.ROAD_PROJECTS_CAPTURE_DIR || './projects-captures');
const manifest = JSON.parse(fs.readFileSync(path.join(source, 'SOURCE_MANIFEST.json')));
const playwrightPath = process.env.ROAD_PLAYWRIGHT_MODULE || 'playwright';
const { chromium } = require(playwrightPath);
const executable = process.env.ROAD_CHROMIUM_EXECUTABLE;
const digest = data => crypto.createHash('sha256').update(data).digest('hex');
const report = {
  schema: 'blackroad-projects-workflow/1', source_commit: manifest.source_commit,
  runner_sha256: digest(fs.readFileSync(__filename)),
  playwright_version: require(path.join(path.dirname(require.resolve(playwrightPath)), 'package.json')).version,
  browser_executable: executable || null, viewport: { width: 1536, height: 1024 },
  production_source_modified: false, upstream_assertions_modified: false,
  storage: 'Native Chromium IndexedDB on a fresh loopback origin, not an in-memory database replacement.',
  network_policy: 'Only the ephemeral static export server is allowed. No system Host, inference provider, device or deployment is started.',
  modules: [], javascript_errors: [], blocked_requests: [], http_requests: [], downloads: [],
  started_at_utc: new Date().toISOString()
};
const modules = ['roadwork-browser.cjs', 'roadwork-storage-browser.cjs'];
const mime = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.jpeg': 'image/jpeg', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml' };
let browser, server, activeModule = 'initial desktop', downloadNumber = 0;

// Observe the documented storage contract directly, bypassing RoadWorkStore.
async function readRaw(frame) {
  return frame.locator('body').evaluate(async () => {
    const db = await new Promise((resolve, reject) => {
      const request = indexedDB.open('roados-desktop-v1', 1);
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
    try {
      return await new Promise((resolve, reject) => {
        const tx = db.transaction('workspace', 'readonly');
        const request = tx.objectStore('workspace').get('current');
        tx.oncomplete = () => resolve(request.result);
        tx.onabort = tx.onerror = () => reject(tx.error);
      });
    } finally { db.close(); }
  });
}

async function main() {
  fs.mkdirSync(path.join(captures, 'downloads'), { recursive: true });
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
        report.http_requests.push({ method: req.method, path: relative, status: 404 });
        res.writeHead(404).end('Outside the pinned export'); return;
      }
      try {
        const body = fs.readFileSync(file);
        report.http_requests.push({ method: req.method, path: relative, status: 200 });
        res.writeHead(200, { 'Content-Type': mime[path.extname(file)] || 'application/octet-stream', 'Cache-Control': 'no-store' }).end(body);
      } catch (error) { report.http_requests.push({ method: req.method, path: relative, status: 500 }); res.writeHead(500).end(String(error)); }
    });
    await new Promise((resolve, reject) => { server.once('error', reject); server.listen(0, '127.0.0.1', resolve); });
    const origin = 'http://127.0.0.1:' + server.address().port;
    browser = await chromium.launch(executable ? { executablePath: executable } : {});
    report.browser_version = browser.version();
    if (executable) report.browser_executable_sha256 = digest(fs.readFileSync(executable));
    const createContext = browser.newContext.bind(browser);
    browser.newContext = async options => {
      const context = await createContext(options), pending = [];
      await context.route('**/*', route => {
        const url = new URL(route.request().url());
        if (url.origin === origin) return route.continue();
        report.blocked_requests.push({ method: route.request().method(), url: url.href });
        return route.abort('blockedbyclient');
      });
      context.on('page', page => {
        page.on('pageerror', error => report.javascript_errors.push({ message: String(error), stack: error.stack, page_url: page.url(), module: activeModule }));
        page.on('download', download => {
          const name = 'downloads/' + String(++downloadNumber).padStart(3, '0') + '-workspace.json';
          const item = { path: name, module: activeModule, suggested_filename: download.suggestedFilename(), status: 'PENDING' };
          report.downloads.push(item);
          pending.push((async () => {
            try {
              await download.saveAs(path.join(captures, name));
              const data = fs.readFileSync(path.join(captures, name));
              const snapshot = JSON.parse(data);
              item.status = 'SAVED'; item.sha256 = digest(data); item.bytes = data.length;
              item.workspace_revision = snapshot.revision;
              item.record_counts = { files: snapshot.files.length, tasks: snapshot.tasks.length, local_activity: snapshot.receipts.length };
            } catch (error) { item.status = 'FAIL'; item.error = String(error); }
          })());
        });
      });
      const close = context.close.bind(context);
      context.close = async () => { await Promise.all(pending); await close(); };
      return context;
    };
    const baseContext = await browser.newContext({ viewport: report.viewport, deviceScaleFactor: 1 });
    const basePage = await baseContext.newPage();
    await basePage.goto(origin + '/desktop/');
    for (const name of modules) {
      activeModule = name;
      const item = { module: 'desktop/apps/tests/' + name, status: 'RUNNING' }, started = performance.now();
      report.modules.push(item);
      await test(name, { timeout: 90000 }, async () => {
        try { await require(path.join(source, item.module))(basePage); item.status = 'PASS'; }
        catch (error) { item.status = 'FAIL'; item.error = String(error.stack || error); throw error; }
        finally { item.elapsed_ms = Math.round(performance.now() - started); }
      });
    }
    activeModule = 'independent nested-project observation';
    await test('nested Projects: raw IndexedDB, reload and committed backup', { timeout: 45000 }, async () => {
      const context = await browser.newContext({ viewport: report.viewport, deviceScaleFactor: 1, acceptDownloads: true });
      try {
        const page = await context.newPage();
        await page.goto(origin + '/workspace/');
        await page.locator('#workspace-dock').getByRole('button', { name: 'Projects', exact: true }).click();
        const work = page.frameLocator('#computer').frameLocator('#surface iframe');
        await work.getByRole('heading', { name: 'RoadWork', exact: true }).waitFor();
        await work.getByRole('button', { name: 'Projects', exact: true }).click();
        const title = 'Verified native Project', brief = 'Keep actual tasks and committed notes inside the right Computer.';
        const notes = 'Retained project decision 💚\n<script>neverExecute()</script>';
        await work.getByLabel('Project name').fill(title);
        await work.getByLabel('Project brief').fill(brief);
        await work.getByRole('button', { name: 'Create project', exact: true }).click();
        await work.getByRole('heading', { name: title, exact: true }).waitFor();
        await work.getByLabel('Project notes and decisions').fill(notes);
        await work.getByRole('checkbox', { name: 'Define the smallest useful result', exact: true }).check();
        await work.getByText('1 / 4 tasks complete', { exact: true }).waitFor();
        assert.equal(await work.getByLabel('Project notes and decisions').inputValue(), notes);
        await work.getByRole('button', { name: 'Save project notes', exact: true }).click();
        await work.getByText('Saved in browser workspace', { exact: false }).waitFor();
        const taskTitle = 'Inspect the committed backup';
        await work.getByLabel('Next task', { exact: true }).fill(taskTitle);
        await work.getByRole('button', { name: 'Add task', exact: true }).click();
        await work.getByRole('checkbox', { name: taskTitle, exact: true }).waitFor();
        const before = await readRaw(work);
        const projects = before.files.filter(file => file.mime === 'application/vnd.blackroad.project+json');
        assert.equal(projects.length, 1);
        const record = JSON.parse(projects[0].content);
        assert.equal(record.title, title); assert.equal(record.brief, brief); assert.equal(record.context, notes);
        assert.equal(record.taskIds.length, 5); assert.equal(new Set(record.taskIds).size, 5);
        assert.equal(before.tasks.length, 5); assert.equal(before.tasks.filter(task => task.done).length, 1);
        assert.ok(before.tasks.some(task => task.title === taskTitle && !task.done));
        assert.ok(record.taskIds.every(id => before.tasks.some(task => task.id === id)));
        assert.equal(before.revision, 4); assert.equal(projects[0].revision, 3);
        assert.deepEqual(before.receipts.map(item => item.operation), ['project-create', 'project-task-toggle', 'project-context', 'project-task-add']);
        assert.equal(await work.locator('#rw-runtime-root').getAttribute('data-phase'), 'disconnected');
        await page.waitForFunction(() => JSON.parse(localStorage.getItem('road-workspace-navigation') || 'null')?.product === 'Projects');
        await page.locator('#pin').click();
        await page.locator('[data-context="Gaia introduction"]').click();
        assert.equal(await work.getByLabel('Project notes and decisions').inputValue(), notes);
        await page.reload();
        await work.getByRole('heading', { name: 'RoadWork', exact: true }).waitFor();
        await work.getByRole('button', { name: 'Projects', exact: true }).click();
        await work.getByRole('button', { name: title, exact: false }).click();
        assert.equal(await work.getByLabel('Project notes and decisions').inputValue(), notes);
        assert.equal(await work.getByRole('checkbox', { name: 'Define the smallest useful result', exact: true }).isChecked(), true);
        assert.deepEqual(await readRaw(work), before, 'Reload must preserve the actual saved workspace exactly');
        assert.equal(await page.locator('#context-title').textContent(), 'Gaia introduction');
        assert.equal(await page.locator('#pin').getAttribute('aria-pressed'), 'true');
        await page.mouse.move(10, 40);
        await page.screenshot({ path: 'nested-project-preview.jpg', type: 'jpeg', quality: 80 });
        const unsaved = notes + '\nUnsaved proposal excluded from backup';
        await work.getByLabel('Project notes and decisions').fill(unsaved);
        const downloadEvent = page.waitForEvent('download');
        await work.getByRole('button', { name: 'Export workspace', exact: true }).click();
        const download = await downloadEvent, stream = await download.createReadStream();
        let text = ''; for await (const chunk of stream) text += chunk.toString('utf8');
        const backup = JSON.parse(text);
        assert.deepEqual(backup, before, 'Download must equal raw committed IndexedDB, not the unsaved editor');
        assert.equal(await work.getByLabel('Project notes and decisions').inputValue(), unsaved);
        assert.match(await work.locator('#rw-status').textContent(), /Unsaved drafts are not included/);
        assert.deepEqual(await readRaw(work), before, 'Export must be read-only');
        await page.screenshot({ path: 'committed-backup-preview.jpg', type: 'jpeg', quality: 80 });
        fs.writeFileSync(path.join(captures, 'raw-committed-workspace.json'), JSON.stringify(before, null, 2) + '\n');
        report.independent_project = { title, project_file_id: projects[0].id, workspace_revision: before.revision, project_revision: projects[0].revision, task_count: before.tasks.length, completed_tasks: 1, activity_operations: before.receipts.map(item => item.operation), reload_raw_state_equal: true, backup_equals_raw_committed_state: true, export_left_raw_state_unchanged: true, unsaved_editor_retained: true, pin_and_left_context_retained: true, canonical_system_connection: 'disconnected' };
      } finally { await context.close(); }
    });
    await test('resource, download and network observations', () => {
      assert.deepEqual(report.javascript_errors, []);
      assert.deepEqual(report.blocked_requests, []);
      assert.deepEqual(report.http_requests.filter(item => item.status >= 400), []);
      assert.ok(report.http_requests.some(item => item.path === 'desktop/apps/roadwork.html'));
      assert.equal(report.modules.length, 2); assert.ok(report.modules.every(item => item.status === 'PASS'));
      assert.equal(report.downloads.length, 3); assert.ok(report.downloads.every(item => item.status === 'SAVED'));
      assert.deepEqual(report.downloads.map(item => item.module), ['roadwork-storage-browser.cjs', 'roadwork-storage-browser.cjs', 'independent nested-project observation']);
      assert.ok(report.independent_project?.backup_equals_raw_committed_state);
    });
  } finally {
    if (browser) await browser.close();
    if (server) await new Promise(resolve => server.close(resolve));
    report.finished_at_utc = new Date().toISOString();
    report.screenshots = Object.fromEntries(fs.readdirSync(captures).filter(name => name.endsWith('-preview.jpg')).sort().map(name => { const data = fs.readFileSync(path.join(captures, name)); return [name, { bytes: data.length, sha256: digest(data) }]; }));
    fs.writeFileSync(path.join(captures, 'browser-report.json'), JSON.stringify(report, null, 2) + '\n');
  }
}
main().catch(error => { console.error(error); process.exitCode = 1; });
