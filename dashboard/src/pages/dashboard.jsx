import React, { useEffect } from "react";
import { getTelemetry, getCurrentTelemetry, getNodes } from "../utils/telemetry"

const [telemetry, setTelemetry] = useState(null);
const [telemetryError, setTelemetryError] = useState(null);
const [telemetryLoading, setTelemetryLoading] = useState(true);

const [currentTelemetry, currentcurrentTelemetry] = useState(null);
const [currentLoading, setCurrentLoading] = useState(true);
const [currentError, setCurrentError] = useState(null);

const [nodes, setNodes] = useState(null);
const [nodesLoading, setNodesLoading] = useState(true);
const [nodesError, setNodesError] = useState(null);

// calls the getTelemetry helper to get data from /telemetry route
useEffect(() => {
    async function fetchTelemetry() {
        try {
            const data = await getTelemetry("esp32-01", "temp", 24);
            setTelemetry(data);
        } catch (error) {
            setError(error.message);
        } finally {
            setLoading(false);
        }
    }

    fetchTelemetry();
}, []);

export default function BMEDashboard() {
    return (
        <main id="bme-dashboard">
            <div id="dashboard-wrapper">

            </div>
        </main>
    )
}