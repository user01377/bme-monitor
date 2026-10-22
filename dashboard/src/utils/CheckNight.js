import * as SunCalc from 'suncalc';

const LAT = 43.084576;
const LON = -77.677079;

export function isNight() {
    const times = SunCalc.getTimes(new Date(), LAT, LON);
    const currentDate = new Date();

    return currentDate < times.sunrise || currentDate >= times.sunset;
}