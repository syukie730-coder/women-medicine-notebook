const CACHE='women-medicine-notebook-v4';
const FILES=['./','index.html','style.css','app.js','assets/app-icon.webp','assets/woman-notebook.webp','apple-touch-icon.png?v=3','apple-touch-icon.png','assets/icon-192.png','assets/icon-512.png','manifest.webmanifest'];
self.addEventListener('install',event=>{event.waitUntil(caches.open(CACHE).then(c=>c.addAll(FILES)))});
self.addEventListener('activate',event=>{event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k.startsWith('women-medicine-notebook-')&&k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',event=>{if(event.request.method!=='GET'||new URL(event.request.url).origin!==self.location.origin)return;event.respondWith(caches.open(CACHE).then(cache=>cache.match(event.request)).then(cached=>cached||fetch(event.request)))});
