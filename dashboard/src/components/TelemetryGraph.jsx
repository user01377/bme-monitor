import "../styles/TelemetryGraph.css";
import { Line } from "react-chartjs-2";
import  "chart.js/auto";
import { useState, useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import { getTelemetry } from "../utils/telemetry";

const DEVICE_IDS = ["er-001", "jw-001", "vn-001"];
const COLORS = ["#FFE08A", "#FFA2B7", "#C4F59D"];

const METRICS = {
    temp: {label: "Temperature", unit: "°F", smoothing: 5,},
    humidity: {label: "Humidity", unit: "%", smoothing: 4,},
    pressure: {label: "Pressure", unit: "hPa", smoothing: 1},
};

const TELEMETRY_LEN = 24;
const ROTATION_INTERVAL = 30_000; // every 30 seconds rotate graph displayed
const REFRESH_INTERVAL = 300_000; // every 5 mins refresh data

const METRIC_KEYS = Object.keys(METRICS);

function formatDate(timestamp) {
    return new Date(timestamp).toLocaleDateString([], {
        timeZone: "America/New_York",
        month: "short",
        day: "numeric",
    });
}

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

export default function TelemetryGraph() {
    const [metricIndex, setMetricIndex] = useState(0);

    const currentMetric = METRIC_KEYS[metricIndex];
    const metric = METRICS[currentMetric];

    // rotate graph every 15 seconds
    useEffect(() => {
        const interval = setInterval(() => {
            setMetricIndex(prev => (prev + 1) % METRIC_KEYS.length);
        }, ROTATION_INTERVAL);

        return () => clearInterval(interval);
    }, []);

    // Fetch telemetry for the current metric
    const {
        data: dataList,
        isPending: telemetryLoading,
        error: telemetryError,
        dataUpdatedAt,
    } = useQuery({
        queryKey: ["telemetry", currentMetric, TELEMETRY_LEN, DEVICE_IDS],
        queryFn: () =>
            Promise.all(
                DEVICE_IDS.map(device =>
                    getTelemetry(device, currentMetric, TELEMETRY_LEN)
                )
            ),
        refetchInterval: REFRESH_INTERVAL,
        staleTime: REFRESH_INTERVAL,
    });

    const chartData = {
        datasets: (dataList ?? []).map((response, index) => {
            const rawData = (response.data ?? [])
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
                borderWidth: 3,
                pointRadius: 0,
                pointHoverRadius: 4,
                cubicInterpolationMode: "monotone",
            };
        }),
    };

    const endTime = dataUpdatedAt || Date.now();
    const startTime = endTime - TELEMETRY_LEN * 60 * 60 * 1000;

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
                            timeZone: "America/New_York",
                            hour: "numeric",
                            hour12: true,
                        }),
                },
                title: {
                    display: false,
                },
                grid: {
                    color: "rgba(255, 255, 255, 0.15)",
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
                },
                grid: {
                    color: "rgba(255, 255, 255, 0.15)",
                },
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
        <>
            <header className="section-header">
                <h2>{metric.label} Trends</h2>
    
                <p>
                    Past {TELEMETRY_LEN} hours ·{" "}
                    {formatDate(startTime)}–{formatDate(endTime)}
                </p>
            </header>
    
            <section className="telemetry-graph">
                <div className="telemetry-graph__chart">
                    {telemetryLoading ? (
                        <p className="telemetry-graph__loading">
                            Loading graph...
                        </p>
                    ) : telemetryError && !dataList ? (
                        <p className="telemetry-graph__loading">
                            Error: {telemetryError.message}
                        </p>
                    ) : !dataList?.length ? (
                        <p className="telemetry-graph__loading">
                            No telemetry available.
                        </p>
                    ) : (
                        <Line
                            data={chartData}
                            options={options}
                            updateMode="none"
                        />
                    )}
                </div>
            </section>
        </>
    );
}