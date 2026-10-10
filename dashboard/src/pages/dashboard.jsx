import React, { useEffect } from "react";
import { getTelemetry, getCurrentTelemetry, getNodes } from "../utils/telemetry"

const [telemetry, setTelemetry] = useState(null);
const [error, setError] = useState(null);
const [loading, setLoading] = useState(true);

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