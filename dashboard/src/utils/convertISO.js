export function convertISO(ISO, timezone = "America/New_York") {
    const date = new Date(ISO);

    const converted = date.toLocaleString("en-US", {
        timeZone: timezone
    });

    return converted;
}