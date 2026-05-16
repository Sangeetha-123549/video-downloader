const CACHE_NAME = "video-downloader-cache-v1";

const urlsToCache = [
    "/",
    "/static/style.css",
    "/static/script.js",
    "/static/manifest.json"
];

// INSTALL EVENT
self.addEventListener("install", event => {
    console.log("Service Worker Installing...");

    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                return cache.addAll(urlsToCache);
            })
    );
});

// ACTIVATE EVENT
self.addEventListener("activate", event => {
    console.log("Service Worker Activated");

    event.waitUntil(
        caches.keys().then(keys => {
            return Promise.all(
                keys.map(key => {
                    if (key !== CACHE_NAME) {
                        return caches.delete(key);
                    }
                })
            );
        })
    );
});

// FETCH EVENT (Offline support)
self.addEventListener("fetch", event => {
    event.respondWith(
        fetch(event.request)
            .then(response => {
                return response;
            })
            .catch(() => {
                return caches.match(event.request);
            })
    );
});