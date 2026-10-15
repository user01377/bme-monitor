import "../styles/CurrentTelemetryCard.css";

function mapTrend(trend) {
    // helper function to convert string to unicode arrows, will use svgs in future
    if (trend === "up") {
        return "↗";
    } else if (trend === "down") {
        return "↘";
    } else {
        return "→";
    }
}

function convertISO(ISO) {
    const date = new Date(ISO);
    const converted = date.toLocaleString();

    return converted;
}

export default function CurrentTelemetryCard({device, data, trend}) {
    if (!data || !trend) {
        return <p>Loading...</p>
    }

    const trendData = trend.data[0];

    const tempTrend = trendData?.temp ?? null;
    const humidityTrend = trendData?.humidity ?? null;
    const pressureTrend = trendData?.pressure ?? null;

    return (
        <article className="telemetry-card">

          <header className="telemetry-card__header">
            <h2>{device}</h2>
          </header>
      
          <div className="telemetry-card__metric">
            <span>Temperature</span>

            <div className="telemetry-card__reading">

              <strong>{data.temperature}<small> °F</small></strong>
              <span className="telemetry-card__trend">{tempTrend !== null && mapTrend(tempTrend)}</span>

            </div>
          </div>
      
          <div className="telemetry-card__metric">
            <span>Humidity</span>

            <div className="telemetry-card__reading">

              <strong>{data.humidity}<small> %</small></strong>
              <span className="telemetry-card__trend">{humidityTrend !== null && mapTrend(humidityTrend)}</span>

            </div>
          </div>
      
          <div className="telemetry-card__metric">
            <span>Pressure</span>

            <div className="telemetry-card__reading">

              <strong>{data.pressure}<small> hPa</small></strong>
              <span className="telemetry-card__trend">{pressureTrend !== null && mapTrend(pressureTrend)}</span>

            </div>
          </div>
      
          <footer className="telemetry-card__footer">
            Latest: <time dateTime={data.timestamp}>{convertISO(data.timestamp)}</time>
          </footer>
        </article>
    );
}