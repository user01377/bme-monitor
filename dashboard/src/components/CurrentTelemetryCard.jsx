
export default function CurrentTelemetryCard({room, data}) {
    if (!data) {
        return <p>Loading...</p>
    }

    return (
        <div>
            <h2>{room}</h2>
            <p>Temperature: {data.temperature}°F</p>
            <p>Humidity: {data.humidity}%</p>
            <p>Pressure: {data.pressure} hPa</p>
        </div>
    );
}