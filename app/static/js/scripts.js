// app/static/js/scripts.js
document.getElementById('barChart').style.width = "150px";
document.getElementById('barChart').style.height = "100px";
document.getElementById('pieChart').style.width = "150px";
document.getElementById('pieChart').style.height = "100px";
document.getElementById('lineChart').style.width = "150px";
document.getElementById('lineChart').style.height = "100px";


// Bar Chart
var ctxBar = document.getElementById('barChart').getContext('2d');
new Chart(ctxBar, {
    type: 'bar',
    data: barData,
    options: {
        responsive: true,
        plugins: {
            legend: { display: false }
        }
    }
});

// Pie Chart
var ctxPie = document.getElementById('pieChart').getContext('2d');
new Chart(ctxPie, {
    type: 'pie',
    data: pieData,
    options: {
        responsive: true
    }
});

// Line Chart
var ctxLine = document.getElementById('lineChart').getContext('2d');
new Chart(ctxLine, {
    type: 'line',
    data: lineData,
    options: {
        responsive: true,
        plugins: {
            legend: { display: true }
        }
    }
});
