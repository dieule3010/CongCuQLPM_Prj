// =========================
// UTILS
// =========================
function $(selector) {
    return document.querySelector(selector);
}

function formatCurrency(v) {
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(v);
}

function notify(msg) {
    alert(msg); // có thể đổi sang toast đẹp
}


// =========================
// DASHBOARD SUMMARY + CHART
// =========================
function loadRevenueSummary() {
    const todayEl = $("#todayRevenue");
    const weekEl = $("#weekRevenue");
    const monthEl = $("#monthRevenue");
    const avgEl = $("#avgOrder");

    if (!todayEl || !weekEl || !monthEl || !avgEl) return;

    fetch("/api/revenue")
        .then(r => r.json())
        .then(data => {
            todayEl.textContent = formatCurrency(data.totals.today);
            weekEl.textContent = formatCurrency(data.totals.week);
            monthEl.textContent = formatCurrency(data.totals.month);
            avgEl.textContent = formatCurrency(data.totals.avg_order);

            renderRevenueChart(data.daily);
        });
}

let revenueChart = null;
function renderRevenueChart(dailyData) {
    const ctx = $("#chartCanvas");
    if (!ctx) return;

    if (revenueChart) revenueChart.destroy();

    revenueChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dailyData.map(d => d.date),
            datasets: [{
                label: 'Revenue',
                data: dailyData.map(d => d.revenue),
                tension: 0.4,
                fill: true
            }]
        },
        options: { responsive: true }
    });
}


// =========================
// MENU MODULE
// =========================
function loadMenu() {
    const container = $("#menuList");
    if (!container) return;

    fetch("/api/menu-items")
        .then(r => r.json())
        .then(data => {
            container.innerHTML = data.items.map(i => `
                <div class="card menu-card">
                    <img src="${i.image}">
                    <h3>${i.name}</h3>
                    <div>${formatCurrency(i.price)}</div>
                    <button class="delete-menu" data-id="${i.id}">Delete</button>
                </div>
            `).join("");

            bindMenuDelete();
        });
}

function bindMenuDelete() {
    const buttons = document.querySelectorAll(".delete-menu");
    buttons.forEach(btn => {
        btn.addEventListener("click", () => {
            const id = btn.dataset.id;
            fetch("/menu-delete/", {
                method: "POST",
                headers: { "X-CSRFToken": getCSRFToken() },
                body: JSON.stringify({ id })
            })
                .then(r => r.json())
                .then(res => {
                    notify("Deleted!");
                    loadMenu();
                });
        });
    });
}


// =========================
// STAFF MODULE
// =========================
function loadStaff() {
    const container = $("#staffList");
    if (!container) return;

    fetch("/api/staff")
        .then(r => r.json())
        .then(data => {
            container.innerHTML = data.staff.map(s => `
                <div class="card staff-card">
                    <b>${s.name}</b>
                    <div>${s.role}</div>
                    <button class="delete-staff" data-id="${s.email}">Delete</button>
                </div>
            `).join("");

            bindStaffDelete();
        });
}

function bindStaffDelete() {
    const buttons = document.querySelectorAll(".delete-staff");
    buttons.forEach(btn => {
        btn.addEventListener("click", () => {
            fetch("/staff-delete/", {
                method: "POST",
                headers: { "X-CSRFToken": getCSRFToken() },
                body: JSON.stringify({ email: btn.dataset.id })
            })
                .then(r => r.json())
                .then(res => {
                    notify("Deleted!");
                    loadStaff();
                });
        });
    });
}


// =========================
// FEEDBACK MODULE
// =========================
function loadFeedback() {
    const container = $("#feedbackList");
    if (!container) return;

    fetch("/api/feedback")
        .then(r => r.json())
        .then(data => {
            container.innerHTML = data.feedback.map(f => `
                <div class="card fb-card">
                    <b>${f.customer}</b>
                    <p>${f.comment}</p>
                    <button class="reply-feedback" data-id="${f.id}">Reply</button>
                    <button class="delete-feedback" data-id="${f.id}">Delete</button>
                </div>
            `).join("");

            bindFeedbackActions();
        });
}

function bindFeedbackActions() {
    document.querySelectorAll(".reply-feedback").forEach(btn => {
        btn.addEventListener("click", () => {
            const reply = prompt("Nhập phản hồi:");
            if (!reply) return;

            fetch("/feedback_reply/", {
                method: "POST",
                headers: { "X-CSRFToken": getCSRFToken() },
                body: JSON.stringify({ id: btn.dataset.id, reply })
            })
                .then(r => r.json())
                .then(res => notify("Đã phản hồi!"));
        });
    });

    document.querySelectorAll(".delete-feedback").forEach(btn => {
        btn.addEventListener("click", () => {
            fetch("/feedback_delete/", {
                method: "POST",
                headers: { "X-CSRFToken": getCSRFToken() },
                body: JSON.stringify({ id: btn.dataset.id })
            })
                .then(r => r.json())
                .then(res => {
                    notify("Đã xoá!");
                    loadFeedback();
                });
        });
    });
}


// =========================
// INVENTORY
// =========================
function loadInventory() {
    const container = $("#inventoryMgmtList");
    if (!container) return;

    fetch("/api/inventory")
        .then(r => r.json())
        .then(data => {
            container.innerHTML = data.items.map(i => `
                <div class="card inventory-card">
                    ${i.name} - ${i.quantity} ${i.unit}
                </div>
            `).join("");
        });
}


// =========================
// PROMOTIONS
// =========================
function loadPromotions() {
    const container = $("#promotionsList");
    if (!container) return;

    fetch("/api/promotions")
        .then(r => r.json())
        .then(data => {
            container.innerHTML = data.promotions.map(p => `
                <div class="card promotion-card">
                    <b>${p.name}</b> - ${p.discount}%
                </div>
            `).join("");
        });
}


// =========================
// POPULAR ITEMS
// =========================
function loadPopularItems() {
    const container = $("#popularItemsList");
    if (!container) return;

    fetch("/api/popular-items")
        .then(r => r.json())
        .then(data => {
            container.innerHTML = data.items.map((item, i) => `
                <div class="card popular-card">
                    #${i + 1} ${item.name} – ${item.totalSold} sold
                </div>
            `).join("");
        });
}


// =========================
// CSRF HELPER
// =========================
function getCSRFToken() {
    const cookie = document.cookie.split("; ").find(row => row.startsWith("csrftoken="));
    return cookie ? cookie.split("=")[1] : "";
}


// =========================
// INIT (Tự nhận biết page đang dùng phần nào)
// =========================
document.addEventListener("DOMContentLoaded", () => {
    loadRevenueSummary();
    loadMenu();
    loadStaff();
    loadFeedback();
    loadInventory();
    loadPromotions();
    loadPopularItems();
});
