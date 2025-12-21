const form = document.getElementById("aqiForm");
const resultSection = document.getElementById("resultSection");
let chart;

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
        pm25: pm25.value,
        pm10: pm10.value,
        no2: no2.value,
        so2: so2.value,
        co: co.value
    };

    const response = await fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    const result = await response.json();

    resultSection.classList.remove("d-none");

    document.getElementById("aqiValue").innerText = result.aqi;
    document.getElementById("healthText").innerText = result.health;

    const badge = document.getElementById("aqiCategory");
    badge.innerText = result.category;

    let color = "#2ecc71";
    if (result.aqi > 100) color = "#f1c40f";
    if (result.aqi > 200) color = "#e67e22";
    if (result.aqi > 300) color = "#e74c3c";

    document.getElementById("aqiValue").style.background = color;
    badge.className = "badge bg-dark";

    // Chart
    const ctx = document.getElementById("aqiChart");
    if (chart) chart.destroy();

    chart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: ["PM2.5", "PM10", "NO2", "SO2", "CO"],
            datasets: [{
                label: "Pollutant Levels",
                data: Object.values(data),
                backgroundColor: "#667eea"
            }]
        }
    });
});
