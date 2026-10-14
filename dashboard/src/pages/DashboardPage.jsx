import "../styles/DashboardPage.css";
import { useEffect, useState } from "react";
import { getTelemetry, getCurrentTelemetry, getNodes, getCurrentTrends } from "../utils/telemetry"
import CurrentTelemetryCard from "../components/CurrentTelemetryCard";

export default function BMEDashboard() {
    const [telemetry, setTelemetry] = useState(null);
    const [telemetryLoading, setTelemetryLoading] = useState(true);
    const [telemetryError, setTelemetryError] = useState(null);

    const [currentTelemetry, setCurrentTelemetry] = useState(null);
    const [currentLoading, setCurrentLoading] = useState(true);
    const [currentError, setCurrentError] = useState(null);

    const [telemetryTrends, setTelemetryTrends] = useState(null);
    const [telemetryTrendsLoading, setTelemetryTrendsLoading] = useState(true);
    const [telemetryTrendsError, setTelemetryTrendsError] = useState(null);

    const [nodes, setNodes] = useState(null);
    const [nodesLoading, setNodesLoading] = useState(true);
    const [nodesError, setNodesError] = useState(null);

    const DEVICE_IDS = ["vn-001", "er-001", "jw-001"]

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
                // temporary hard coded query params
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

    return (
        <main id="bme-dashboard">
            <div id="dashboard-wrapper">
                
                <header className="dashboard-header">
                    <div className="dashboard-header-info">
                        <h1>BME Dashboard</h1>
                        <p>Environmental Monitoring System</p>
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
                                <CurrentTelemetryCard device={device} data={currentTelemetry[index]} trend={telemetryTrends[index]}/>
                            ))
                        )}
                    </div>
                </section>
                        
            </div>
        </main>
    );
}