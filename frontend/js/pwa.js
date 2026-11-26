/**
 * Progressive Web App (PWA) Registration & Service Worker Management
 */

if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/service-worker.js')
      .then(reg => {
        console.log('ServiceWorker registered with scope:', reg.scope);
      })
      .catch(err => {
        console.warn('ServiceWorker registration failed:', err);
      });
  });
}

// Online / Offline State Detection
window.addEventListener('online', () => {
  const banner = document.getElementById('offline-banner');
  if (banner) banner.classList.add('hidden');
});

window.addEventListener('offline', () => {
  const banner = document.getElementById('offline-banner');
  if (banner) banner.classList.remove('hidden');
});
