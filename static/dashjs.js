window.onload = function () {
    if (!window.chartsData) return;

    window.chartsData.forEach(chart => {
        if (chart.error) return;  // skip charts with error

        const ctx = document.getElementById(chart.id)?.getContext('2d');
        if (ctx && chart.config) {
            new Chart(ctx, chart.config);  // ✅ THIS LINE IS THE KEY
        }
    });
};
