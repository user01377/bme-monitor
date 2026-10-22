import "../styles/DayTexture.css";

export default function DayTexture() {
    return (
        <div className="day-texture" aria-hidden="true">
            <div className="day-texture__gradient" />
            <div className="day-texture__sun" />

            <div className="day-texture__cloud day-texture__cloud--one" />
            <div className="day-texture__cloud day-texture__cloud--two" />
            <div className="day-texture__cloud day-texture__cloud--three" />

            <div className="day-texture__glow day-texture__glow--one" />
            <div className="day-texture__glow day-texture__glow--two" />
        </div>
    );
}