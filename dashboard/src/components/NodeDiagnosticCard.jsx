import "../styles/NodeDiagnosticCard.css";
import { convertISO } from "../utils/convertISO";

function formatUptime(seconds) {
    const days = Math.floor(seconds / 86400);
    const hours = Math.floor((seconds % 86400) / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);

    return `${days}d ${hours}h ${minutes}m`;
}

export default function NodeDiagnosticCard({data}) {
    if (!data) {
        return <p>Loading...</p>
    }

    const OFFLINE_DECLARATION = 30; // 30 minute time delta for node to be declared offline

    const lastSeen = new Date(data.timestamp);

    // nodes are set to report every 10 minutes, 30m grace should ensure they are actually offline.
    const elapsed = Date.now() - lastSeen.getTime();
    const isOnline = elapsed >= 0 && elapsed < OFFLINE_DECLARATION * 60 * 1000;

    return (
        <article className="node-card">
            <header className="node-card__header">
                <h3>{data.device}</h3>

                <span className={`node-card__status ${isOnline ? "node-card__status--online" : "node-card__status--offline"}`}>
                    <span className="node-card__status-dot" />
                    {isOnline ? "Online" : "Offline"}
                </span>
            </header>

            <div className="node-card__metrics">
                <div className="node-card__metric">
                    <span>Signal Strength</span>
                    <div className="node-card__reading">
                        <strong>{data.rssi}</strong>
                        <small>dBm</small>
                    </div>
                </div>

                <div className="node-card__metric">
                    <span>Uptime</span>
                    <div className="node-card__reading">
                        <strong>{formatUptime(data.uptime)}</strong>
                    </div>
                </div>

                <div className="node-card__metric">
                    <span>Reset Reason</span>
                    <div className="node-card__reading">
                        <strong>{data.reset}</strong>
                    </div>
                </div>
            </div>

            <footer className="node-card__footer">
                Last seen: {convertISO(data.timestamp)}
            </footer>
        </article>
    );
}