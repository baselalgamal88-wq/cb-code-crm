const C='cbcrm-v2';
self.addEventListener('install',e=>self.skipWaiting());
self.addEventListener('activate',e=>e.waitUntil(self.clients.claim()));
self.addEventListener('fetch',e=>{const u=new URL(e.request.url); if(e.request.method!=='GET'||u.origin!==location.origin) return;
  e.respondWith(fetch(e.request).then(r=>{const c=r.clone(); caches.open(C).then(x=>x.put(e.request,c)); return r;}).catch(()=>caches.match(e.request)));});
// phone notifications sent by the sheet's script through Firebase
self.addEventListener('push',e=>{let j={};try{j=e.data?e.data.json():{}}catch(x){j={body:e.data&&e.data.text()}}
  const d=Object.assign({},j.notification||{},j.data||{});
  e.waitUntil(self.registration.showNotification(d.title||'CB Code CRM',{body:d.body||'',icon:'icon-192.png',badge:'icon-192.png',tag:'cbcrm-'+Date.now(),data:{url:d.url||'./'}}));});
self.addEventListener('notificationclick',e=>{e.notification.close();const url=(e.notification.data&&e.notification.data.url)||'./';
  e.waitUntil(clients.matchAll({type:'window',includeUncontrolled:true}).then(ws=>{for(const w of ws){if('focus' in w){w.navigate&&w.navigate(url).catch(()=>{});return w.focus();}}return clients.openWindow(url);}));});
