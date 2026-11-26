const CACHE_NAME = 'sahayak-v1';
const STATIC_ASSETS = [
  '/',
  '/manifest.json',
  '/static/css/style.css',
  '/static/css/admin.css',
  '/static/js/i18n.js',
  '/static/js/voice.js',
  '/static/js/pwa.js',
  '/pages/offline.html',
  '/pages/about.html',
  '/pages/how_it_works.html'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(STATIC_ASSETS);
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((k) => {
          if (k !== CACHE_NAME) {
            return caches.delete(k);
          }
        })
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', (e) => {
  // Pass through non-GET and API requests directly to network
  if (e.request.method !== 'GET' || e.request.url.includes('/api/')) {
    return;
  }

  e.respondWith(
    caches.match(e.request).then((cached) => {
      if (cached) {
        // Return cache and update in background
        fetch(e.request).then((networkRes) => {
          if (networkRes && networkRes.status === 200) {
            caches.open(CACHE_NAME).then((cache) => cache.put(e.request, networkRes));
          }
        }).catch(() => {});
        return cached;
      }

      return fetch(e.request).catch(() => {
        // Return offline page for HTML navigation requests
        if (e.request.headers.get('accept').includes('text/html')) {
          return caches.match('/pages/offline.html');
        }
      });
    })
  );
});
