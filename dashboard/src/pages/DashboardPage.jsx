import "../styles/DashboardPage.css";
import { useEffect, useState } from "react";
import { getTelemetry, getCurrentTelemetry, getNodes, getCurrentTrends, getTelemetrySummary } from "../utils/telemetry"
import CurrentTelemetryCard from "../components/CurrentTelemetryCard";
import TelemetryGraph from "../components/TelemetryGraph";
import TelemetrySummary from "../components/TelemetrySummary";
import NodeDiagnosticCard from "../components/NodeDiagnosticCard";

function formatDate(date) {
    return date.toLocaleDateString([], {
        month: "short",
        day: "numeric",
    });
}

export default function BMEDashboard() {

    // USE STATE HOOKS
    const [telemetry, setTelemetry] = useState(null);
    const [telemetryLoading, setTelemetryLoading] = useState(true);
    const [telemetryError, setTelemetryError] = useState(null);

    const [currentTelemetry, setCurrentTelemetry] = useState(null);
    const [currentLoading, setCurrentLoading] = useState(true);
    const [currentError, setCurrentError] = useState(null);

    const [telemetryTrends, setTelemetryTrends] = useState(null);
    const [telemetryTrendsLoading, setTelemetryTrendsLoading] = useState(true);
    const [telemetryTrendsError, setTelemetryTrendsError] = useState(null);

    const [telemetrySummary, setTelemetrySummary] = useState(null);
    const [telemetrySummaryLoading, setTelemetrySummaryLoading] = useState(true);
    const [telemetrySummaryError, setTelemetrySummaryError] = useState(null);

    const [nodes, setNodes] = useState(null);
    const [nodesLoading, setNodesLoading] = useState(true);
    const [nodesError, setNodesError] = useState(null);

    // DASHBOARD CONSTANTS
    const DEVICE_IDS = ["er-001", "jw-001", "vn-001"];
    const METRICS = ["temp", "humidity", "pressure"];
    const TELEMETRY_LEN = 24

    const endTime = new Date();
    const startTime = new Date(
        endTime.getTime() - TELEMETRY_LEN * 60 * 60 * 1000
    );

    // calls the getTelemetry helper to get data from /telemetry route
    useEffect(() => {
        async function fetchTelemetry() {
            try {
                // eventually make the metric variable, fetch every xyz refreshes and use different 
                const data = await Promise.all(
                    DEVICE_IDS.map(device => getTelemetry(device, "temp", TELEMETRY_LEN))
                );

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
                const data = await Promise.all(
                    DEVICE_IDS.map(device => getCurrentTelemetry(device))
                );

                setCurrentTelemetry(data);
            } catch (error) {
                setCurrentError(error.message);
            } finally {
                setCurrentLoading(false);
            }
        }

        async function fetchCurrentTelemetryTrends() {
            try {
                const data = await Promise.all(
                    DEVICE_IDS.map(device => getCurrentTrends(device))
                );

                setTelemetryTrends(data);
            } catch (error) {
                setTelemetryTrendsError(error.message);
            } finally {
                setTelemetryTrendsLoading(false);
            }
        }
        
        fetchCurrentTelemetry();
        fetchCurrentTelemetryTrends();
    }, []);

    useEffect(() => {
        async function fetchTelemetrySummary() {
            try {
                const data = await getTelemetrySummary();

                setTelemetrySummary(data);
            } catch (error) {
                setTelemetrySummaryError(error.message);
            } finally {
                setTelemetrySummaryLoading(false);
            }
        }

        fetchTelemetrySummary();
    }, []);

    useEffect(() => {
        async function fetchNodes() {
            try {
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

    return (
        <main id="bme-dashboard">
            <div id="dashboard-wrapper">
                
                <header className="dashboard-header">
                    <div className="dashboard-header__info">
                        <h1>Telemetry Dashboard</h1>
                        <p>Displaying room conditions and sensor diagnostics</p>
                    </div>
                </header>

                <section className="dashboard-section glass-panel">
                    <header className="section-header">
                        <h2>Current Telemetry</h2>
                        <p>Latest environmental readings from each sensor</p>
                    </header>

                    <div className="telemetry-cards">
                        {/* if loading, display loading */}
                        {(currentLoading || telemetryTrendsLoading) ? (
                            <p>Loading telemetry...</p>

                        // if not loading, check for error. if error, display error message. if no error, display cards.
                        ) : (currentError || telemetryTrendsError) ? (
                            <p>Error: {currentError || telemetryTrendsError}</p>
                        ) : (
                            DEVICE_IDS.map((device, index) => (
                                <CurrentTelemetryCard key={device} device={device} data={currentTelemetry[index]} trend={telemetryTrends[index]}/>
                            ))
                        )}
                    </div>
                </section>

                <section className="dashboard-section glass-panel">
                    <header className="section-header">
                        {(telemetryLoading) ? (
                                <p>Loading Title...</p>
                        ) : (telemetryError) ? (
                                <p>Error: {telemetryError}</p>
                        ) : (
                            <h2 style={{ textTransform: "capitalize" }}>{telemetry[0].metric === "temp" ? "Temperature" : telemetry[0].metric} Trends</h2>
                        )}

                        <p>Past {TELEMETRY_LEN} hours · {formatDate(startTime)}–{formatDate(endTime)}</p>
                    </header>

                    <div>
                       {(telemetryLoading) ? (
                            <p>Loading graph...</p>
                       ) : (telemetryError) ? (
                            <p>Error: {telemetryError}</p>
                       ) : (
                            <TelemetryGraph dataList={telemetry} range={TELEMETRY_LEN} />
                       )}
                    </div>
                </section>

                <section className="dashboard-section glass-panel">
                    <header className="section-header">
                       <h2>Today's Summary · All Rooms</h2>
                    </header>

                    <div>
                       {(telemetrySummaryLoading) ? (
                            <p>Loading summary...</p>
                       ) : (telemetrySummaryError) ? (
                            <p>Error: {telemetrySummaryError}</p>
                       ) : (
                            <TelemetrySummary data={telemetrySummary} />
                       )}
                    </div>
                </section>

                <section className="dashboard-section glass-panel">
                    <header className="section-header">
                       <h2>Node Diagnostics</h2>
                    </header>
                    
                    <div className="node-cards">
                       {(nodesLoading) ? (
                            <p>Loading summary...</p>
                       ) : (nodesError) ? (
                            <p>Error: {nodesError}</p>
                       ) : (
                            nodes.data.map(node => (
                                <NodeDiagnosticCard key={node.device} data={node} />
                            ))
                       )}
                    </div>
                </section>
            </div>
        </main>
    );
}