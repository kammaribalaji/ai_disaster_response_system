/**
 * Telangana Disaster Response Map - Leaflet.js Integration
 * Coordinates: 17.3850° N, 78.4867° E
 * Provides real-time disaster mapping with rescue teams and relief centers
 */

// Telangana city coordinates
const TELANGANA_CITIES = {
    hyderabad: { lat: 17.3850, lng: 78.4867, name: 'Hyderabad' },
    secunderabad: { lat: 17.3620, lng: 78.5244, name: 'Secunderabad' },
    vijayawada: { lat: 16.5062, lng: 80.6480, name: 'Vijayawada' },
    warangal: { lat: 17.9689, lng: 79.5941, name: 'Warangal' },
    nizamabad: { lat: 19.2740, lng: 78.1198, name: 'Nizamabad' },
    karimnagar: { lat: 18.4393, lng: 79.1288, name: 'Karimnagar' },
    ramagundam: { lat: 18.7577, lng: 79.4453, name: 'Ramagundam' },
    medak: { lat: 17.0244, lng: 78.2444, name: 'Medak' },
    nalgonda: { lat: 17.0502, lng: 78.9556, name: 'Nalgonda' }
};

// Disaster types with colors and icons
const DISASTER_TYPES = {
    flood: { color: '#3b82f6', icon: '💧', label: 'Flood' },
    earthquake: { color: '#ef4444', icon: '🌍', label: 'Earthquake' },
    landslide: { color: '#f59e0b', icon: '⛰️', label: 'Landslide' },
    cyclone: { color: '#8b5cf6', icon: '🌪️', label: 'Cyclone' },
    drought: { color: '#f97316', icon: '☀️', label: 'Drought' }
};

// Sample disaster data for Telangana
const TELANGANA_DISASTERS = [
    {
        id: 'd1',
        type: 'flood',
        city: 'Hyderabad',
        lat: 17.4000,
        lng: 78.5000,
        severity: 'CRITICAL',
        affectedPeople: 15000,
        status: 'Active',
        date: '2026-03-22'
    },
    {
        id: 'd2',
        type: 'landslide',
        city: 'Warangal',
        lat: 17.9800,
        lng: 79.6100,
        severity: 'WARNING',
        affectedPeople: 3500,
        status: 'Monitoring',
        date: '2026-03-21'
    },
    {
        id: 'd3',
        type: 'earthquake',
        city: 'Karimnagar',
        lat: 18.4500,
        lng: 79.1400,
        severity: 'ALERT',
        affectedPeople: 8000,
        status: 'Response',
        date: '2026-03-20'
    },
    {
        id: 'd4',
        type: 'cyclone',
        city: 'Vijayawada',
        lat: 16.5200,
        lng: 80.6600,
        severity: 'WARNING',
        affectedPeople: 12000,
        status: 'Alert',
        date: '2026-03-22'
    },
    {
        id: 'd5',
        type: 'flood',
        city: 'Nizamabad',
        lat: 19.2900,
        lng: 78.1300,
        severity: 'MODERATE',
        affectedPeople: 5000,
        status: 'Response',
        date: '2026-03-21'
    }
];

// Rescue team locations
const RESCUE_TEAMS = [
    { id: 'r1', name: 'NDRF Unit 1', lat: 17.3850, lng: 78.4867, personnel: 45, status: 'Active' },
    { id: 'r2', name: 'Fire Brigade HQ', lat: 17.3920, lng: 78.4750, personnel: 120, status: 'Active' },
    { id: 'r3', name: 'Ambulance Service', lat: 17.3800, lng: 78.5100, personnel: 30, status: 'Active' },
    { id: 'r4', name: 'Police Response', lat: 17.3700, lng: 78.4900, personnel: 80, status: 'Active' },
    { id: 'r5', name: 'Warangal Emergency', lat: 17.9689, lng: 79.5941, personnel: 35, status: 'Active' },
    { id: 'r6', name: 'Karimnagar Medical', lat: 18.4393, lng: 79.1288, personnel: 25, status: 'Active' }
];

// Relief centers
const RELIEF_CENTERS = [
    { id: 'rc1', name: 'Relief Camp - Stadium', lat: 17.3810, lng: 78.5050, capacity: 5000, occupancy: 3200 },
    { id: 'rc2', name: 'Medical Center - GMC', lat: 17.3950, lng: 78.4900, capacity: 500, occupancy: 380 },
    { id: 'rc3', name: 'Food Distribution - Park', lat: 17.3700, lng: 78.5200, capacity: 1000, occupancy: 650 },
    { id: 'rc4', name: 'Shelter - School Complex', lat: 17.3880, lng: 78.4750, capacity: 2000, occupancy: 1200 },
    { id: 'rc5', name: 'Warangal Relief Camp', lat: 17.9650, lng: 79.5900, capacity: 3000, occupancy: 1800 },
    { id: 'rc6', name: 'Vijayawada Medical', lat: 16.5100, lng: 80.6500, capacity: 400, occupancy: 220 }
];

/**
 * Initialize Telangana map with all disaster, rescue, and relief data
 * @param {string} mapElementId - HTML element ID where map should be rendered
 * @param {string} userRole - User role to determine what features are visible
 */
function initializeTelanganaMap(mapElementId, userRole = 'admin') {
    // Create map centered on Telangana
    const map = L.map(mapElementId).setView([17.3850, 78.4867], 8);

    // Add tile layer (OpenStreetMap)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors | Telangana Disaster Response',
        maxZoom: 19
    }).addTo(map);

    // Add disasters to map
    addDisastersToMap(map, userRole);

    // Add rescue teams (if admin or rescue role)
    if (userRole === 'admin' || userRole === 'rescue') {
        addRescueTeamsToMap(map);
    }

    // Add relief centers (all roles)
    addReliefCentersToMap(map, userRole);

    return map;
}

/**
 * Add disaster markers to the map
 */
function addDisastersToMap(map, userRole) {
    TELANGANA_DISASTERS.forEach(disaster => {
        const disasterInfo = DISASTER_TYPES[disaster.type];
        const severityColor = getSeverityColor(disaster.severity);

        // Create custom HTML icon
        const iconHtml = `
            <div style="
                background: ${severityColor};
                width: 40px;
                height: 40px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 20px;
                border: 3px solid white;
                box-shadow: 0 2px 8px rgba(0,0,0,0.3);
                animation: pulse 2s infinite;
            ">
                ${disasterInfo.icon}
            </div>
        `;

        const customIcon = L.divIcon({
            html: iconHtml,
            iconSize: [40, 40],
            className: 'disaster-marker'
        });

        const marker = L.marker([disaster.lat, disaster.lng], { icon: customIcon })
            .bindPopup(`
                <div style="font-family: 'Poppins', sans-serif; width: 250px;">
                    <h4 style="margin: 0 0 8px 0; color: ${severityColor};">
                        ${disasterInfo.icon} ${disasterInfo.label}
                    </h4>
                    <p style="margin: 4px 0; font-size: 12px;">
                        <strong>Location:</strong> ${disaster.city}
                    </p>
                    <p style="margin: 4px 0; font-size: 12px;">
                        <strong>Severity:</strong> <span style="color: ${severityColor}; font-weight: bold;">${disaster.severity}</span>
                    </p>
                    <p style="margin: 4px 0; font-size: 12px;">
                        <strong>Affected:</strong> ${disaster.affectedPeople.toLocaleString()} people
                    </p>
                    <p style="margin: 4px 0; font-size: 12px;">
                        <strong>Status:</strong> ${disaster.status}
                    </p>
                </div>
            `)
            .addTo(map);
    });
}

/**
 * Add rescue team markers to the map
 */
function addRescueTeamsToMap(map) {
    RESCUE_TEAMS.forEach(team => {
        const iconHtml = `
            <div style="
                background: linear-gradient(135deg, #3b82f6, #1d4ed8);
                width: 38px;
                height: 38px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 18px;
                border: 3px solid white;
                box-shadow: 0 2px 8px rgba(59,130,246,0.4);
            ">
                🚑
            </div>
        `;

        const customIcon = L.divIcon({
            html: iconHtml,
            iconSize: [38, 38],
            className: 'rescue-marker'
        });

        L.marker([team.lat, team.lng], { icon: customIcon })
            .bindPopup(`
                <div style="font-family: 'Poppins', sans-serif; width: 200px;">
                    <h4 style="margin: 0 0 8px 0; color: #3b82f6;">🚑 ${team.name}</h4>
                    <p style="margin: 4px 0; font-size: 12px;">
                        <strong>Personnel:</strong> ${team.personnel}
                    </p>
                    <p style="margin: 4px 0; font-size: 12px;">
                        <strong>Status:</strong> <span style="color: #10b981; font-weight: bold;">● ${team.status}</span>
                    </p>
                </div>
            `)
            .addTo(map);
    });
}

/**
 * Add relief center markers to the map
 */
function addReliefCentersToMap(map, userRole) {
    RELIEF_CENTERS.forEach(center => {
        const occupancyPercent = Math.round((center.occupancy / center.capacity) * 100);
        const capacityColor = occupancyPercent > 80 ? '#ef4444' : occupancyPercent > 50 ? '#f59e0b' : '#10b981';

        const iconHtml = `
            <div style="
                background: linear-gradient(135deg, ${capacityColor}, ${capacityColor}dd);
                width: 38px;
                height: 38px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 18px;
                border: 3px solid white;
                box-shadow: 0 2px 8px rgba(16,185,129,0.4);
            ">
                🏥
            </div>
        `;

        const customIcon = L.divIcon({
            html: iconHtml,
            iconSize: [38, 38],
            className: 'relief-marker'
        });

        L.marker([center.lat, center.lng], { icon: customIcon })
            .bindPopup(`
                <div style="font-family: 'Poppins', sans-serif; width: 220px;">
                    <h4 style="margin: 0 0 8px 0; color: ${capacityColor};">🏥 ${center.name}</h4>
                    <p style="margin: 4px 0; font-size: 12px;">
                        <strong>Capacity:</strong> ${center.capacity}
                    </p>
                    <p style="margin: 4px 0; font-size: 12px;">
                        <strong>Occupancy:</strong> ${center.occupancy} (${occupancyPercent}%)
                    </p>
                    <div style="
                        background: #f3f4f6;
                        border-radius: 4px;
                        height: 6px;
                        margin: 8px 0;
                        overflow: hidden;
                    ">
                        <div style="
                            background: ${capacityColor};
                            height: 100%;
                            width: ${occupancyPercent}%;
                        "></div>
                    </div>
                    <p style="margin: 4px 0; font-size: 12px; color: ${capacityColor};">
                        ${capacityColor === '#10b981' ? '✓ Availability OK' : capacityColor === '#f59e0b' ? '⚠️ Nearing Capacity' : '❌ At Capacity'}
                    </p>
                </div>
            `)
            .addTo(map);
    });
}

/**
 * Get color based on severity level
 */
function getSeverityColor(severity) {
    const colors = {
        'CRITICAL': '#ef4444',
        'WARNING': '#f59e0b',
        'ALERT': '#f97316',
        'MODERATE': '#3b82f6',
        'LOW': '#10b981'
    };
    return colors[severity] || '#6b7280';
}

/**
 * Get disaster statistics for a given area
 */
function getTelanganaDisasterStats() {
    return {
        totalDisasters: TELANGANA_DISASTERS.length,
        criticalCount: TELANGANA_DISASTERS.filter(d => d.severity === 'CRITICAL').length,
        warningCount: TELANGANA_DISASTERS.filter(d => d.severity === 'WARNING').length,
        totalAffected: TELANGANA_DISASTERS.reduce((sum, d) => sum + d.affectedPeople, 0),
        activeRescueTeams: RESCUE_TEAMS.filter(t => t.status === 'Active').length,
        totalRescuePersonnel: RESCUE_TEAMS.reduce((sum, t) => sum + t.personnel, 0),
        reliefCentersTotal: RELIEF_CENTERS.length,
        reliefCapacityUsed: Math.round((RELIEF_CENTERS.reduce((sum, c) => sum + c.occupancy, 0) / 
                                        RELIEF_CENTERS.reduce((sum, c) => sum + c.capacity, 0)) * 100)
    };
}

/**
 * Update map with real-time data (simulated)
 */
function updateMapWithRealtimeData(map) {
    // This function can be called periodically to update disaster/relief data
    // For now, it's a placeholder for future WebSocket integration
    console.log('Map data updated with latest information');
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.1); opacity: 0.9; }
    }
    
    .disaster-marker {
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
    }
    
    .rescue-marker {
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
    }
    
    .relief-marker {
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
    }
    
    .leaflet-popup-content {
        font-family: 'Poppins', sans-serif !important;
    }
`;
document.head.appendChild(style);
