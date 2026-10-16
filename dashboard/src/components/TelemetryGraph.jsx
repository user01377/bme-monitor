import "../styles/TelemetryGraph.css";
import { Line } from "react-chartjs-2";
import  "chart.js/auto";

const DEVICE_IDS = ["vn-001", "er-001", "jw-001"];
const COLORS = ["#C2B280", "#A95C68", "#a78bfa"];

const METRICS = {
    temp: {label: "Temperature", unit: "°F", smoothing: 5,},
    humidity: {label: "Humidity", unit: "%", smoothing: 4,},
    pressure: {label: "Pressure", unit: "hPa", smoothing: 1},
};

function movingAverage(data, windowSize = 3) {
    return data.map((point, index) => {
        const start = Math.max(0, index - windowSize + 1);
        const window = data.slice(start, index + 1);

        const average = window.reduce(
            (sum, p) => sum + p.y, 0
        ) / window.length;

        return {
            ...point,
            y: average,
        };
    });
}

export default function TelemetryGraph({dataList, range}) {
    if (!dataList) {
        return <p>Loading...</p>
    }

    const metric = METRICS[dataList[0].metric];

    const chartData = {
        datasets: dataList.map((response, index) => {
            const rawData = response.data
                .map(point => ({
                    x: new Date(point.timestamp).getTime(),
                    y: point.value,
                }))
                .sort((a, b) => a.x - b.x);
    
            return {
                label: DEVICE_IDS[index],
                data: movingAverage(rawData, metric.smoothing),
                borderColor: COLORS[index],
                backgroundColor: COLORS[index],
                borderWidth: 2,
                pointRadius: 0,
                pointHoverRadius: 4,
                cubicInterpolationMode: "monotone",
            };
        }),
    };

    const endTime = Date.now();
    const startTime = endTime - range * 60 * 60 * 1000;

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
            mode: "nearest",
            axis: "x",
            intersect: false,
        },
        scales: {
            x: {
                type: "linear",
                min: startTime,
                max: endTime,
                title: {
                    display: true,
                    text: "Time",
                    color: "#ffffff"
                },
                ticks: {
                    stepSize: 3 * 60 * 60 * 1000,
                    autoSkip: false,
                    color: "rgba(255, 255, 255, 0.8)",
                    font: {
                        size: 13,
                    },
                    padding: 10,
                    callback: value =>
                        new Date(value).toLocaleTimeString([], {
                            hour: "numeric",
                            hour12: true,
                        }),
                },
                title: {
                    display: false,
                },
            },
            y: {
                title: {
                    display: true,
                    text: `${metric.label} (${metric.unit})`,
                    color: "#ffffff",
                    font: {
                        size: 11
                    }
                },
                ticks: {
                    font: {
                        size: 13
                    },
                    color: "rgba(255, 255, 255, 0.8)"
                }
            },
        },
        plugins: {
            legend: {
                position: "bottom",
                labels: {
                    color: "rgba(255, 255, 255, 0.8)",
                    usePointStyle: true,
                    pointStyle: "circle",
                    boxWidth: 8,
                    boxHeight: 8,
                    padding: 20,
                    font: {
                        size: 13,
                    },
                },
            },
            tooltip: {
                callbacks: {
                    title: items =>
                        new Date(items[0].parsed.x).toLocaleString(),
                    label: context =>
                        `${context.dataset.label}: ${context.parsed.y} ${metric.unit}`,
                },
            },
        },
    };

    return (
        <section className="telemetry-graph">
            <div className="telemetry-graph__chart">
                <Line data={chartData} options={options} />
            </div>
        </section>
    )
}