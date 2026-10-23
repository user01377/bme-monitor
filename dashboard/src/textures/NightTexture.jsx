export default function NightTexture({
  dotCount = 200,
  minDotSize = 1.5,
  maxDotSize = 5,
  twinkleCount = 50,
}) {
  const stars = Array.from({ length: dotCount }).map(() => ({
    cx: Math.random() * 100,
    cy: Math.random() * 100,
    r: minDotSize + Math.random() * (maxDotSize - minDotSize),
    opacity: 0.1 + Math.random() * 0.9,
  }));

  const twinkles = Array.from({ length: twinkleCount }).map(() => ({
    cx: Math.random() * 100,
    cy: Math.random() * 100,
    r: 1.5 + Math.random() * 2,
    opacity: 0.7 + Math.random() * 0.3,
  }));

  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        pointerEvents: "none",
        overflow: "hidden",
        zIndex: 0
      }}
    >
      <svg width="100%" height="100%" style={{ position: "absolute", top: 0, left: 0 }}>
        {stars.map((star, i) => (
          <circle
            key={i}
            cx={`${star.cx}%`}
            cy={`${star.cy}%`}
            r={star.r}
            fill={`rgba(255,255,255,${star.opacity})`}
          />
        ))}
        {twinkles.map((twinkle, i) => (
          <circle
            key={`twinkle-${i}`}
            cx={`${twinkle.cx}%`}
            cy={`${twinkle.cy}%`}
            r={twinkle.r}
            fill={`rgba(255,255,255,${twinkle.opacity})`}
          />
        ))}
      </svg>
    </div>
  );
}
