import "../styles/DashboardPage.css";
import { useQuery } from "@tanstack/react-query";
import { useEffect } from "react";
import { getTelemetry, getCurrentTelemetry, getNodes, getCurrentTrends, getTelemetrySummary } from "../utils/telemetry"
import CurrentTelemetryCard from "../components/CurrentTelemetryCard";
import TelemetryGraph from "../components/TelemetryGraph";
import TelemetrySummary from "../components/TelemetrySummary";
import NodeDiagnosticCard from "../components/NodeDiagnosticCard";

// DASHBOARD CONSTANTS
const DEVICE_IDS = ["er-001", "jw-001", "vn-001"];
const METRICS = ["temp", "humidity", "pressure"];
const TELEMETRY_LEN = 24

const endTime = new Date();
const startTime = new Date(
    endTime.getTime() - TELEMETRY_LEN * 60 * 60 * 1000
);

const BUILD_VERSION = import.meta.env.VITE_BUILD_VERSION;
const VERSION_CHECK_INTERVAL = 300 * 1000; // first num is seconds

function formatDate(date) {
    return date.toLocaleDateString([], {
        timeZone: "America/New_York",
        month: "short",
        day: "numeric",
    });
}

export default function BMEDasdhboard() {

    // telemetry query
    const {
        data: telemetry,
        isPending: telemetryLoading,
        error: telemetryError,
    } = useQuery({
        queryKey: ["telemetry"],
        queryFn: () => 
            Promise.all(DEVICE_IDS.map(device => getTelemetry(device, "temp", TELEMETRY_LEN))),
        refetchInterval: 60_000
    });

    // currentTelemetry query
    const {
        data: currentTelemetry,
        isPending: currentLoading,
        error: currentError,
    } = useQuery({
        queryKey: ["currentTelemetry"],
        queryFn: () => 
            Promise.all(DEVICE_IDS.map(device => getCurrentTelemetry(device))),
        refetchInterval: 60_000
    });

    // telemetryTrends query
    const {
        data: telemetryTrends,
        isPending: telemetryTrendsLoading,
        error: telemetryTrendsError,
    } = useQuery({
        queryKey: ["telemetryTrends"],
        queryFn: () => 
            Promise.all(DEVICE_IDS.map(device => getCurrentTrends(device))),
        refetchInterval: 60_000
    });

    // telemetrySummary query
    const {
        data: telemetrySummary,
        isPending: telemetrySummaryLoading,
        error: telemetrySummaryError,
    } = useQuery({
        queryKey: ["telemetrySummary"],
        queryFn: getTelemetrySummary,
        refetchInterval: 60_000
    });

    // nodes query
    const {
        data: nodes,
        isPending: nodesLoading,
        error: nodesError,
    } = useQuery({
        queryKey: ["nodes"],
        queryFn: () => getNodes(),
        refetchInterval: 60_000
    });

    // hook to check if frontend version is stale, force refresh to get new code if stale
    useEffect(() => {
        async function checkVersion() {
            console.log("CHECKING VERSION...");

            try {
                const response = await fetch("/version.json", {cache: "no-store"});

                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }
              
                const { version } = await response.json();
                  
                if (version !== BUILD_VERSION) {
                    console.log(
                        `Version mismatch: ${BUILD_VERSION} -> ${version}`
                    );
                    
                    window.location.reload();
                }

            } catch (error) {
                console.error("Failed to check dashboard version:", error);
            }
        }

        checkVersion();

        const interval = setInterval(checkVersion, VERSION_CHECK_INTERVAL);

        return () => clearInterval(interval);
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
                            <p>Error: {(currentError || telemetryTrendsError).message}</p>
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
                                <p>Error: {(telemetryError).message}</p>
                        ) : (
                            <h2 style={{ textTransform: "capitalize" }}>{telemetry[0].metric === "temp" ? "Temperature" : telemetry[0].metric} Trends</h2>
                        )}

                        <p>Past {TELEMETRY_LEN} hours · {formatDate(startTime)}–{formatDate(endTime)}</p>
                    </header>

                    <div>
                       {(telemetryLoading) ? (
                            <p>Loading graph...</p>
                       ) : (telemetryError) ? (
                            <p>Error: {(telemetryError).message}</p>
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
                            <p>Error: {(telemetrySummaryError).message}</p>
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
                            <p>Error: {(nodesError).message}</p>
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