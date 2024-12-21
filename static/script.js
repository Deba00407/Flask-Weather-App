document.addEventListener('DOMContentLoaded', () => {
    let p = document.getElementById('time-of-day');
    
    if (p.innerHTML == 'Day') {
        document.body.style.backgroundColor = '#FAF7F0';
        document.body.style.color = '#181C14';
    } else if (p.innerHTML == 'Night') {
        document.body.style.backgroundColor = '#181C14';
        document.body.style.color = '#FAF7F0';
    }
});