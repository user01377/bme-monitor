import "../styles/TelemetrySummary.css";

export default function TelemetrySummary({data}) {
    if (!data) {
        return <p>Loading...</p>
    }

    const [dataAvg, dataHigh, dataLow] = data.data;


    const summaries = [
        { label: "Average", data: dataAvg },
        { label: "High", data: dataHigh },
        { label: "Low", data: dataLow }
    ];
    
    return (
        <section className="telemetry-summary">
            {summaries.map(({ label, data }) => (
                <div className="telemetry-summary__metric" key={label}>
                    <h3 className="telemetry-summary__title">{label}</h3>
    
                    <div className="telemetry-summary__values">

                        <div className="telemetry-summary__reading">
                            <span className="telemetry-summary__label">Temperature</span>
                            <span className="telemetry-summary__value">{data.temp.toFixed(0)}<small>°F</small></span>
                        </div>
    
                        <div className="telemetry-summary__reading">
                            <span className="telemetry-summary__label">Humidity</span>
                            <span className="telemetry-summary__value">{data.humidity.toFixed(0)}<small> %</small></span>
                        </div>
    
                        <div className="telemetry-summary__reading">
                            <span className="telemetry-summary__label">Pressure</span>
                            <span className="telemetry-summary__value">{data.pressure.toFixed(0)}<small> hPa</small></span>
                        </div>

                    </div>
                </div>
            ))}
        </section>
    );    
}