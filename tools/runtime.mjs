import {createRequire} from 'node:module';import path from 'node:path';
export const req=createRequire(path.resolve(process.env.LINIA_TOOLS||'.','package.json'));
export async function browser(){return req('puppeteer-core').launch({executablePath:process.env.CHROME_PATH||'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true})}
