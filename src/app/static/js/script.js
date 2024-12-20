async function sendClick() {
    try {
        const response = await fetch('/records', { method: 'POST' });
        const data = await response.json();
        console.log('Response:', data);
    } catch (error) {
        console.error('Error:', error);
    }
}
