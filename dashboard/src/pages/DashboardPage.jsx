import { useEffect, useState } from "react";
import { getTelemetry, getCurrentTelemetry, getNodes } from "../utils/telemetry"

const [telemetry, setTelemetry] = useState(null);
const [telemetryLoading, setTelemetryLoading] = useState(true);
const [telemetryError, setTelemetryError] = useState(null);

const [currentTelemetry, setCurrentTelemetry] = useState(null);
const [currentLoading, setCurrentLoading] = useState(true);
const [currentError, setCurrentError] = useState(null);

const [nodes, setNodes] = useState(null);
const [nodesLoading, setNodesLoading] = useState(true);
const [nodesError, setNodesError] = useState(null);

// calls the getTelemetry helper to get data from /telemetry route
useEffect(() => {
    async function fetchTelemetry() {
        try {
            // temporary hard coded query params
            const data = await getTelemetry("esp32-01", "temp", 24);
            setTelemetry(data);
        } catch (error) {
            setTelemetryError(error.message);
        } finally {
            setTelemetryLoading(false);
        }
    }

    fetchTelemetry();
}, []);

useEffect(() => {
    async function fetchCurrentTelemetry() {
        try {
            // temporary hard coded query params
            const data = await getCurrentTelemetry("esp32-01");
            setCurrentTelemetry(data);
        } catch (error) {
            setCurrentError(error.message);
        } finally {
            setCurrentLoading(false);
        }
    }

    fetchCurrentTelemetry();
}, []);

useEffect(() => {
    async function fetchNodes() {
        try {
            // temporary hard coded query params
            const data = await getNodes();
            setNodes(data);
        } catch (error) {
            setNodesError(error.message);
        } finally {
            setNodesLoading(false);
        }
    }

    fetchNodes();
}, []);

export default function BMEDashboard() {
    return (
        <main id="bme-dashboard">
            <div id="dashboard-wrapper">

            </div>
        </main>
    )
}