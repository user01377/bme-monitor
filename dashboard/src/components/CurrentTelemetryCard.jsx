import "../styles/CurrentTelemetryCard.css";

function mapTrendString(trend) {
    // helper function to convert string to unicode arrows, will use svgs in future
    if (trend === "up") {
        return "↑";
    } else if (trend === "down") {
        return "↓";
    } else {
        return "→";
    }
}
export default function CurrentTelemetryCard({device, data, trend}) {
    if (!data || !trend) {
        return <p>Loading...</p>
    }

    const trendData = trend.data[0];

    return (
        <div>
            <h2>{device}</h2>
            <p>Temperature: {data.temperature}°F {mapTrend(trendData.temp)}</p>
            <p>Humidity: {data.humidity}% {mapTrend(trendData.humidity)}</p>
            <p>Pressure: {data.pressure} hPa {mapTrend(trendData.pressure)}</p>
            <p>Latest: {data.timestamp}</p>
        </div>
    );
}