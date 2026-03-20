/* =================================================================
   AI Disaster Response — Premium App JS v2.0
   Skeleton loaders · Bell shake · Auto-refresh · Smooth UI
================================================================= */

/* ── Fetch Helper ─────────────────────────────────────────────── */
async function fetchJSON(url, options = {}) {
    try {
        const res = await fetch(url, options);
        return await res.json();
    } catch (err) {
        console.warn(`fetch ${url}:`, err.message);
        return null;
    }
}

/* ── Color Tokens ─────────────────────────────────────────────── */
const C = {
    primary: '#3b82f6',
    danger:  '#ef4444',
    warning: '#f59e0b',
    success: '#10b981',
    info:    '#06b6d4',
};

const formatNum = n => Number(n).toLocaleString();

/* ── Skeleton Loader Helpers ─────────────────────────────────── */
function showSkeleton(id, rows = 3) {
    const el = document.getElementById(id);
    if (!el) return;
    el.innerHTML = Array.from({length: rows}, () =>
        `<div class="skeleton skeleton-text mb-2" style="width:${70+Math.random()*25|0}%"></div>`
    ).join('');
}

function showSkeletonStat(id) {
    const el = document.getElementById(id);
    if (el) el.innerHTML = '<div class="skeleton skeleton-stat"></div>';
}

/* ── Bell Shake on new alert ─────────────────────────────────── */
let bellShaking = false;
function shakeBell() {
    if (bellShaking) return;
    const bell = document.querySelector('[data-bs-toggle="dropdown"] .bi-bell');
    if (!bell) return;
    bellShaking = true;
    bell.parentElement.classList.add('bell-shake');
    setTimeout(() => { bell?.parentElement?.classList?.remove('bell-shake'); bellShaking = false; }, 900);
}

/* ── Animate Number Counter ──────────────────────────────────── */
function animateCount(el, targetVal, duration = 800) {
    if (!el) return;
    const start = parseInt(el.textContent) || 0;
    const target = parseInt(targetVal) || 0;
    const startTime = performance.now();
    const update = now => {
        const progress = Math.min((now - startTime) / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3); // ease-out-cubic
        el.textContent = formatNum(Math.round(start + (target - start) * eased));
        if (progress < 1) requestAnimationFrame(update);
    };
    requestAnimationFrame(update);
}

/* ── Dashboard Init ──────────────────────────────────────────── */
const statIds = ['zonesCount','alertsCount','rescueOpsCount','reliefCount','evacuatedCount','efficiencyCount'];
statIds.forEach(id => showSkeleton(id, 1));

async function initDashboard() {
    const data = await fetchJSON('/api/dashboard');
    if (!data) return;

    const updates = [
        ['zonesCount',      data.monitored_zones   || 9],
        ['alertsCount',     data.high_risk_alerts   || 6],
        ['rescueOpsCount',  data.active_rescue_ops  || 12],
        ['reliefCount',     data.relief_delivered   || 3400],
        ['evacuatedCount',  data.total_evacuated    || 8200],
        ['efficiencyCount', data.team_efficiency    || 87],
    ];

    updates.forEach(([id, val]) => {
        const el = document.getElementById(id);
        if (el) { el.textContent = '0'; animateCount(el, val, 900); }
    });

    // Chart font defaults
    if (typeof Chart !== 'undefined') {
        const isDark = document.body.classList.contains('dark-mode');
        Chart.defaults.color = isDark ? '#64748b' : '#6b7280';
        Chart.defaults.font.family = "'Inter', sans-serif";
    }

    initCharts(data);
}

/* ── Charts ──────────────────────────────────────────────────── */
let chartInstances = {};

function initCharts(data) {
    const isDark = document.body.classList.contains('dark-mode');
    const gridColor = isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.05)';

    const tooltipDefaults = {
        backgroundColor: isDark ? '#1a2235' : '#fff',
        titleColor: isDark ? '#f1f5f9' : '#0f172a',
        bodyColor: isDark ? '#94a3b8' : '#64748b',
        borderColor: isDark ? 'rgba(255,255,255,0.1)' : '#e2e8f0',
        borderWidth: 1,
        padding: 12, cornerRadius: 10,
        titleFont: { family:"'Inter'", size:13, weight:'700' },
        bodyFont: { family:"'Inter'", size:12 },
    };

    // Main disaster timeline chart
    const ctx1 = document.getElementById('disasterChart');
    if (ctx1 && data.timeline) {
        if (chartInstances.disaster) chartInstances.disaster.destroy();
        chartInstances.disaster = new Chart(ctx1, {
            type: 'line',
            data: {
                labels: data.timeline.labels,
                datasets: [{
                    label: 'Alerts',
                    data: data.timeline.data,
                    borderColor: C.primary,
                    backgroundColor: 'rgba(59,130,246,0.08)',
                    borderWidth: 2.5,
                    pointBackgroundColor: C.primary,
                    pointBorderColor: isDark ? '#0b0f1a' : '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 4, pointHoverRadius: 6,
                    tension: 0.4, fill: true,
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: { legend: { display: false }, tooltip: tooltipDefaults },
                scales: {
                    y: { beginAtZero: true, grid: { color: gridColor, drawBorder: false }, border: { display: false }, ticks: { padding: 8, font: { size: 11 } } },
                    x: { grid: { display: false, drawBorder: false }, border: { display: false }, ticks: { padding: 8, font: { size: 11 } } }
                },
                animation: { duration: 800, easing: 'easeOutQuart' }
            }
        });
    }

    // Predictive risk chart (if present)
    const ctx2 = document.getElementById('predictiveChart');
    if (ctx2) {
        if (chartInstances.predictive) chartInstances.predictive.destroy();
        chartInstances.predictive = new Chart(ctx2, {
            type: 'line',
            data: {
                labels: ['Now','2h','4h','6h','8h','12h','18h','24h'],
                datasets: [
                    { label: 'Zone G', data: [90,88,92,95,94,89,85,82], borderColor: C.danger,  backgroundColor: 'rgba(239,68,68,0.07)',  borderWidth: 2, pointRadius: 3, tension: 0.4, fill: true },
                    { label: 'Zone D', data: [80,82,85,83,79,75,72,68], borderColor: C.warning, backgroundColor: 'rgba(245,158,11,0.07)', borderWidth: 2, pointRadius: 3, tension: 0.4, fill: true },
                    { label: 'Zone B', data: [50,52,54,51,48,45,42,40], borderColor: C.info,    backgroundColor: 'rgba(6,182,212,0.06)',   borderWidth: 2, pointRadius: 3, tension: 0.4, fill: true },
                ]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: { legend: { labels: { font: { size: 11, family:"'Inter'" }, usePointStyle: true, pointStyleWidth: 8 } }, tooltip: tooltipDefaults },
                scales: {
                    y: { beginAtZero: false, min: 30, max: 100, grid: { color: gridColor }, border: { display: false }, ticks: { callback: v => v+'%', font: { size: 11 } } },
                    x: { grid: { display: false }, border: { display: false }, ticks: { font: { size: 11 } } }
                },
                animation: { duration: 1000, easing: 'easeOutQuart' }
            }
        });
    }

    // Performance / radar chart (if present)
    const ctx3 = document.getElementById('performanceChart');
    if (ctx3) {
        if (chartInstances.performance) chartInstances.performance.destroy();
        chartInstances.performance = new Chart(ctx3, {
            type: 'radar',
            data: {
                labels: ['Response Time','Rescue Rate','Relief Coverage','Team Efficiency','Alert Speed','Evacuation'],
                datasets: [{
                    label: 'Performance', data: [82, 91, 78, 87, 94, 83],
                    borderColor: C.primary, backgroundColor: 'rgba(59,130,246,0.12)',
                    borderWidth: 2, pointBackgroundColor: C.primary, pointRadius: 4,
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: { legend: { display: false }, tooltip: tooltipDefaults },
                scales: { r: { min: 0, max: 100, grid: { color: gridColor }, angleLines: { color: gridColor }, ticks: { display: false } } },
                animation: { duration: 900, easing: 'easeOutQuart' }
            }
        });
    }

    // Weekly alerts bar chart
    const ctx4 = document.getElementById('weeklyChart');
    if (ctx4) {
        if (chartInstances.weekly) chartInstances.weekly.destroy();
        chartInstances.weekly = new Chart(ctx4, {
            type: 'bar',
            data: {
                labels: ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],
                datasets: [{
                    label: 'Alerts', data: [18, 23, 31, 27, 42, 38, 19],
                    backgroundColor: 'rgba(59,130,246,0.6)', borderRadius: 6,
                    hoverBackgroundColor: C.primary,
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: { legend: { display: false }, tooltip: tooltipDefaults },
                scales: {
                    y: { beginAtZero: true, grid: { color: gridColor }, border: { display: false }, ticks: { font: { size: 11 } } },
                    x: { grid: { display: false }, border: { display: false }, ticks: { font: { size: 11 } } }
                },
                animation: { duration: 700, easing: 'easeOutQuart' }
            }
        });
    }
}

/* ── Auto-Refresh Dashboard (every 30s) ──────────────────────── */
let refreshCount = 0;
function autoRefreshDashboard() {
    setInterval(async () => {
        const data = await fetchJSON('/api/dashboard');
        if (!data) return;
        refreshCount++;
        // Shake bell every 3rd refresh (simulate new alert)
        if (refreshCount % 3 === 0) shakeBell();
        const updates = [
            ['zonesCount',     data.monitored_zones   || 9],
            ['alertsCount',    data.high_risk_alerts   || 6],
            ['rescueOpsCount', data.active_rescue_ops  || 12],
            ['reliefCount',    data.relief_delivered   || 3400],
        ];
        updates.forEach(([id, val]) => {
            const el = document.getElementById(id);
            if (el) animateCount(el, val, 600);
        });
    }, 30000);
}

/* ── Leaflet Map Init ────────────────────────────────────────── */
let map = null;

async function initMap() {
    const mapElement = document.getElementById('riskMap');
    if (!mapElement || map) return;

    const isDark = document.body.classList.contains('dark-mode');
    const tileUrl = isDark
        ? 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png'
        : 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png';

    map = L.map('riskMap', { zoomControl: false }).setView([12.97, 77.6], 10);
    L.control.zoom({ position: 'bottomright' }).addTo(map);
    L.tileLayer(tileUrl, { attribution: '&copy; CARTO', subdomains: 'abcd', maxZoom: 20 }).addTo(map);

    const data = await fetchJSON('/api/risk-map');
    const groups = { heat: L.layerGroup(), markers: L.layerGroup(), shelters: L.layerGroup(), teams: L.layerGroup() };

    if (data?.zones) {
        data.zones.forEach(zone => {
            const color = zone.base_risk > 70 ? C.danger : zone.base_risk > 40 ? C.warning : C.success;
            const r = Math.max(10, zone.base_risk / 5);
            const m = L.circleMarker([zone.lat, zone.lng], {
                radius: r, fillColor: color, color: color,
                weight: 2, opacity: 1, fillOpacity: 0.4
            });
            m.bindPopup(`<div style="font-family:'Inter'; font-weight:700; color:${color}; font-size:1rem;">${zone.name}</div>
                <div style="font-size:0.82rem; color:#64748b; margin-top:4px;">Risk: <b style="color:${color}">${zone.base_risk}%</b><br>Population: ${zone.population?.toLocaleString() || 'N/A'}</div>`,
                { closeButton: false, className: 'clean-popup' });
            m.addTo(groups.markers);
        });
    }

    if (data?.shelters) {
        data.shelters.forEach(s => {
            const icon = L.divIcon({
                html: `<div style="background:#10b981;border-radius:50%;width:26px;height:26px;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 8px rgba(16,185,129,0.5);border:2px solid white;"><i class="bi bi-house-heart-fill" style="color:white;font-size:0.75rem;"></i></div>`,
                className: '', iconSize: [26,26], iconAnchor: [13,13]
            });
            L.marker([s.lat, s.lng], {icon}).bindPopup(`<b>${s.name}</b><br><span style="font-size:0.82rem;color:#10b981">${s.occupancy}/${s.capacity}</span>`).addTo(groups.shelters);
        });
    }

    if (data?.rescue_teams) {
        data.rescue_teams.forEach(t => {
            const icon = L.divIcon({
                html: `<div class="pulse-anim" style="background:#3b82f6;border-radius:50%;width:28px;height:28px;display:flex;align-items:center;justify-content:center;border:2px solid white;"><i class="bi bi-truck" style="color:white;font-size:0.75rem;"></i></div>`,
                className: '', iconSize: [28,28], iconAnchor: [14,14]
            });
            L.marker([t.lat, t.lng], {icon}).bindPopup(`<b>${t.id}</b><br><small>${t.status}</small>`).addTo(groups.teams);
        });
    }

    Object.values(groups).forEach(g => g.addTo(map));

    L.control.layers(null, { "🔴 Risk Rings": groups.markers, "🏠 Shelters": groups.shelters, "🚑 Teams": groups.teams }, { collapsed: false, position: 'topright' }).addTo(map);

    // Style leaflet control
    setTimeout(() => {
        const lc = document.querySelector('.leaflet-control-layers');
        if (lc) Object.assign(lc.style, { borderRadius: '10px', fontFamily:"'Inter'", fontSize:'0.85rem', fontWeight:'600', border:'1px solid rgba(0,0,0,0.07)', boxShadow:'0 4px 16px rgba(0,0,0,0.1)' });
    }, 200);
}

/* ── Leaflet popup + map pins CSS ────────────────────────────── */
const mapStyle = document.createElement('style');
mapStyle.innerHTML = `
    .leaflet-popup-content-wrapper { border-radius: 12px !important; padding: 6px 8px !important; box-shadow: 0 12px 40px rgba(0,0,0,0.15) !important; font-family: 'Inter', sans-serif !important; }
    .leaflet-popup-tip { box-shadow: none !important; }
    .leaflet-control-layers { border-radius: 10px !important; }
    .pulse-anim { animation: pinPulse 2s infinite; }
    @keyframes pinPulse {
        0%   { box-shadow: 0 0 0 0 rgba(59,130,246,0.7); }
        70%  { box-shadow: 0 0 0 10px rgba(59,130,246,0); }
        100% { box-shadow: 0 0 0 0 rgba(59,130,246,0); }
    }
`;
document.head.appendChild(mapStyle);

/* ── Dark mode: re-render charts ─────────────────────────────── */
document.addEventListener('darkModeChange', () => {
    const data = {};
    initCharts(data);
});

/* ── Auto-init ───────────────────────────────────────────────── */
if (document.getElementById('riskMap'))       initMap();
if (document.getElementById('disasterChart')) { initDashboard(); autoRefreshDashboard(); }
if (document.getElementById('zonesCount'))    initDashboard();
