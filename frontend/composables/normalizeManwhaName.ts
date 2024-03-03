export default function (input: string): string {
    return input
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .replace(/[^\w\s]/gi, '')
        .replace(/\s+/g, '-')
        .toLowerCase()
}
