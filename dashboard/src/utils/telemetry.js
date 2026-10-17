export async function getTelemetry(device_id, metric, range = 24) {
    const params = new URLSearchParams({
        device_id: device_id,
        metric: metric,
        range: String(range)
    });

    const response = await fetch(`/api/telemetry?${params}`);

    if (!response.ok) {
        throw new Error(`Failed to fetch telemetry: ${response.status}`);
    }

    return response.json();
}

export async function getCurrentTelemetry(device_id) {
    const params = new URLSearchParams({
        device_id: device_id
    });

    const response = await fetch(`/api/telemetry/current?${params}`);

    if (!response.ok) {
        throw new Error(`Failed to fetch telemetry current: ${response.status}`);
    }

    return response.json();
}

export async function getNodes(device_id) {
    let url = `/api/nodes`;

    if (device_id) {
        const params = new URLSearchParams({ device_id });
        
        url += `?${params}`;
    }

    const response = await fetch(url);

    if (!response.ok) {
        throw new Error(`Failed to fetch nodes: ${response.status}`);
    }

    return response.json();
}

export async function getCurrentTrends(device_id) {
    let url = `/api/telemetry/trend`;

    if (device_id) {
        const params = new URLSearchParams({ device_id });
        
        url += `?${params}`;
    }

    const response = await fetch(url);

    if (!response.ok) {
        throw new Error(`Failed to fetch telemetry trends: ${response.status}`);
    }
    
    return response.json();
}

export async function getTelemetrySummary() {
    const response = await fetch(`/api/telemetry/summary`);

    if (!response.ok) {
        throw new Error(`Failed to fetch telemetry summary: ${response.status}`);
    }

    return response.json();
}