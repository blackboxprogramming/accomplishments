import { join } from 'node:path';
import { pathToFileURL } from 'node:url';

const root = process.argv[2];
if (!root) throw new Error('an explicitly selected trusted export is required');
const module = await import(pathToFileURL(join(root, 'impl/dist/products/wire.js')).href);
if (typeof module.verifyBundle !== 'function') throw new Error('verifyBundle export is absent');
console.log(JSON.stringify({ status: 'PASS', export: 'verifyBundle', type: typeof module.verifyBundle }));
