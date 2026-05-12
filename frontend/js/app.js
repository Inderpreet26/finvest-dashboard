// ===== CONFIG =====
const API = {
    auth: 'http://127.0.0.1:8001',
    portfolio: 'http://127.0.0.1:8002',
    market: 'http://127.0.0.1:8003',
    news: 'http://127.0.0.1:8004',
    analytics: 'http://127.0.0.1:8005',
    watchlist: 'http://127.0.0.1:8006',
    notification: 'http://127.0.0.1:8007',
};

// ===== AUTH =====
const getUsername = () => localStorage.getItem('username') || 'user1';

const setUsername = (username) => localStorage.setItem('username', username);

const logout = () => {
    localStorage.removeItem('username');
    window.location.href = '../index.html';
};

const checkLogin = () => {
    const username = localStorage.getItem('username');
    if (!username) window.location.href = '../index.html';
    const el = document.getElementById('username-display');
    if (el) el.textContent = username;
};

// ===== API CALLS =====
const fetchData = async (url) => {
    try {
        const res = await fetch(url);
        return await res.json();
    } catch (err) {
        console.error('API Error:', url, err);
        return null;
    }
};

const postData = async (url, body) => {
    try {
        const res = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });
        return await res.json();
    } catch (err) {
        console.error('API Error:', url, err);
        return null;
    }
};

const deleteData = async (url) => {
    try {
        const res = await fetch(url, { method: 'DELETE' });
        return await res.json();
    } catch (err) {
        console.error('API Error:', url, err);
        return null;
    }
};

// ===== UI HELPERS =====
const formatMoney = (amount) => `$${parseFloat(amount).toLocaleString()}`;

const getPLClass = (value) => value >= 0 ? 'positive' : 'negative';

const getChangeText = (change) => `${change >= 0 ? '+' : ''}${change}%`;

const showMessage = (elementId, message, success) => {
    const el = document.getElementById(elementId);
    if (el) {
        el.textContent = message;
        el.style.color = success ? '#00d09c' : '#ff4d4d';
    }
};