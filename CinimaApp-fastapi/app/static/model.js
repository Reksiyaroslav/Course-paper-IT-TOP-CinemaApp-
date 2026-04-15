document.addEventListener('DOMContentLoaded', () => {
    // 🔹 1. СНАЧАЛА читаем ошибки из URL
    const params = new URLSearchParams(window.location.search);
    const errorLogin = params.get('error_login');
    const errorReg = params.get('error_reg');
    
    // 🔹 2. Если есть ошибки — работаем с ними
    if (errorLogin || errorReg) {
        // 🔥 Удаляем СТАРЫЕ ошибки из DOM
        document.querySelectorAll('.err').forEach(el => el.remove());
        
        // Показываем новую ошибку
        if (errorLogin) {
            showModalError('log_modal', errorLogin);
        }
        if (errorReg) {
            showModalError('reg_modal', errorReg);
        }
        
        // 🔹 3. ТОЛЬКО ПОСЛЕ показа — очищаем URL
        setTimeout(() => {
            window.history.replaceState({}, '', window.location.pathname);
        }, 100);
    }
});

function showModalError(modalId, errorMsg) {
    const modal = document.getElementById(modalId);
    if (!modal) return;
    
    // Открываем модалку
    window.location.hash = modalId;
    
    // Создаём блок ошибки
    const errDiv = document.createElement('div');
    errDiv.className = 'err';
    // 🔥 Декодируем и чистим сообщение
    let message = decodeURIComponent(errorMsg);
    message = message.split('?')[0].split('&')[0].trim();
    
    errDiv.textContent = message;
    
    const form = modal.querySelector('form');
    if (form) {
        form.insertBefore(errDiv, form.firstChild);
    }
}