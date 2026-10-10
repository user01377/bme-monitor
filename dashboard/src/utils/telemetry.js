const API_URL = import.meta.env.VITE_API_URL;

export async function getTelemetry(device_id, metric, range = 24) {
    const params = new URLSearchParams({
        device_id: device_id,
        metric: metric,
        range: String(range)
    });

    const response = await fetch(`${API_URL}/api/telemetry?${params}`)

    if (!response.ok) {
        throw new Error(`Failed to fetch telemetry: ${response.status}`);
    }

    return response.json();
}

export async function getCurrentTelemetry() {
    
}

export async function getNodes() {
    
} 