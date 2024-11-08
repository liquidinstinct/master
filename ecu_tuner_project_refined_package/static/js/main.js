
const API_BASE_URL = "/api/tune";

async function sendVoiceCommand() {
    try {
        const response = await fetch(`${API_BASE_URL}/voice_command`, { method: 'POST' });
        const data = await response.json();
        alert(data.message);
    } catch (error) {
        console.error("Error sending voice command:", error);
    }
}

async function checkConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/connection_status`);
        const data = await response.json();
        document.getElementById('connectionStatus').textContent = data.connected ? "Connected" : "Disconnected";
    } catch (error) {
        console.error("Error checking connection status:", error);
    }
}

async function fetchVehicleData() {
    try {
        const response = await fetch(`${API_BASE_URL}/vehicle_data`);
        const data = await response.json();
        document.getElementById('rpmData').textContent = data.rpm || "-";
        document.getElementById('speedData').textContent = data.speed || "-";
    } catch (error) {
        console.error("Error fetching vehicle data:", error);
    }
}

// Fetch data periodically
setInterval(fetchVehicleData, 1000);
