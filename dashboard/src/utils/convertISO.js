export function convertISO(ISO) {
    const date = new Date(ISO);
    const converted = date.toLocaleString();

    return converted;
}