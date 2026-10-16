const API_URL = import.meta.env.VITE_API_URL;
const API_KEY = import.meta.env.VITE_API_KEY;

export async function getTelemetry(device_id, metric, range = 24) {
    const params = new URLSearchParams({
        device_id: device_id,
        metric: metric,
        range: String(range)
    });

    const response = await fetch(`${API_URL}/api/telemetry?${params}`, {
        method: "GET",
        headers: {
            "X-API-Key": API_KEY
        }
    });

    if (!response.ok) {
        throw new Error(`Failed to fetch telemetry: ${response.status}`);
    }

    return response.json();
}

export async function getCurrentTelemetry(device_id) {
    const params = new URLSearchParams({
        device_id: device_id
    });

    const response = await fetch(`${API_URL}/api/telemetry/current?${params}`, {
        method: "GET",
        headers: {
            "X-API-Key": API_KEY
        }
    });

    if (!response.ok) {
        throw new Error(`Failed to fetch telemetry current: ${response.status}`);
    }

    return response.json();
}

export async function getNodes(device_id) {
    let url = `${API_URL}/api/nodes`;

    if (device_id) {
        const params = new URLSearchParams({ device_id });
        
        url += `?${params}`;
      }
    
      const response = await fetch(url, {
            method: "GET",
            headers: {
                "X-API-Key": API_KEY
            }
       });
    
      if (!response.ok) {
        throw new Error(`Failed to fetch nodes: ${response.status}`);
      }
    
      return response.json();
}

export async function getCurrentTrends(device_id) {
    let url = `${API_URL}/api/telemetry/trend`;

    if (device_id) {
        const params = new URLSearchParams({ device_id });
        
        url += `?${params}`;
    }

    const response = await fetch(url, {
        method: "GET",
        headers: {
            "X-API-Key": API_KEY
        }
    });

    if (!response.ok) {
        throw new Error(`Failed to fetch telemetry trends: ${response.status}`);
    }
    
    return response.json();
}

export async function getTelemetrySummary() {
    const response = await fetch(`${API_URL}/api/telemetry/summary`, {
        method: "GET",
        headers: {
            "X-API-Key": API_KEY
        }
    });

    if (!response.ok) {
        throw new Error(`Failed to fetch telemetry summary: ${response.status}`);
    }

    return response.json();
}