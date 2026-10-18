import './App.css';
import { useState, useEffect } from 'react';
import BMEDashboard from './pages/DashboardPage';
import NightTexture from './textures/NightTexture';
import { isNight } from './utils/CheckNight';

const CHECK_NIGHT_INTERVAL = 60_000; // time is seconds * 1000, so 1 minute

function App() {
    const [night, setNight] = useState(() => isNight());

    useEffect(() => {
        const interval = setInterval(() => {
            setNight(isNight());
        }, CHECK_NIGHT_INTERVAL);

        return () => clearInterval(interval);
    }, []);

    return (
        <div className={night ? "theme-night" : "theme-day"}>
            {night && <NightTexture />}
            <BMEDashboard />
        </div>
    );
}

export default App;