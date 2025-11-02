// 전역 변수
let map;
let temperatureChart;
let markers = [];
let weatherData = [];
let currentCity = null;
let currentTempType = 'avg';

// 온도별 색상
function getColorByTemperature(temp) {
    if (temp < 0) return '#8b00ff';
    if (temp < 10) return '#0066ff';
    if (temp < 20) return '#00cc66';
    if (temp < 30) return '#ffaa00';
    return '#ff0000';
}

// 지도 초기화
function initMap() {
    map = L.map('map').setView([20, 0], 2);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap',
        maxZoom: 18
    }).addTo(map);
}

// 마커 추가
function addMarkers(cities) {
    markers.forEach(m => map.removeLayer(m));
    markers = [];
    
    cities.forEach(city => {
        const color = getColorByTemperature(city.temperature);
        const icon = L.divIcon({
            className: 'custom-marker',
            html: `<div style="background:${color};width:30px;height:30px;border-radius:50%;border:3px solid white;box-shadow:0 2px 10px rgba(0,0,0,0.3);display:flex;align-items:center;justify-content:center;color:white;font-weight:bold;font-size:12px;">${Math.round(city.temperature)}°</div>`,
            iconSize: [30, 30],
            iconAnchor: [15, 15]
        });
        
        const marker = L.marker([city.lat, city.lon], { icon }).addTo(map);
        marker.bindPopup(`<b>${city.name}</b><br>${city.temperature}°C<br>${city.weather}`);
        marker.on('click', () => {
            showCityInfo(city);
            updateChart(city);
        });
        markers.push(marker);
    });
}

// 도시 정보 표시
function showCityInfo(city) {
    currentCity = city;
    const html = `
        <div class="city-detail">
            <h3><i class="fas fa-map-marker-alt" style="color:${getColorByTemperature(city.temperature)}"></i> ${city.name}</h3>
            <div class="current-temp">${city.temperature}°C</div>
            <div class="weather-desc"><i class="fas ${city.weatherIcon}"></i> ${city.weather}</div>
            <div class="detail-row"><span class="detail-label"><i class="fas fa-globe"></i> 국가</span><span class="detail-value">${city.country}</span></div>
            <div class="detail-row"><span class="detail-label"><i class="fas fa-compass"></i> 위도</span><span class="detail-value">${city.lat.toFixed(4)}°</span></div>
            <div class="detail-row"><span class="detail-label"><i class="fas fa-compass"></i> 경도</span><span class="detail-value">${city.lon.toFixed(4)}°</span></div>
            <div class="detail-row"><span class="detail-label"><i class="fas fa-clock"></i> 시간대</span><span class="detail-value">${city.timezone}</span></div>
        </div>
    `;
    document.getElementById('cityInfo').innerHTML = html;
}

// 차트 초기화
function initChart() {
    const ctx = document.getElementById('temperatureChart').getContext('2d');
    temperatureChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['오늘', '1일 후', '2일 후', '3일 후', '4일 후'],
            datasets: [{
                label: '평균 온도',
                data: [],
                borderColor: '#667eea',
                backgroundColor: 'rgba(102,126,234,0.1)',
                borderWidth: 3,
                tension: 0.4,
                fill: true,
                pointRadius: 6,
                pointHoverRadius: 8,
                pointBackgroundColor: '#667eea',
                pointBorderColor: '#fff',
                pointBorderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                title: {
                    display: true,
                    text: '서울 - 평균 온도 추이 (5일)',
                    font: { size: 16, family: "'Noto Sans KR', sans-serif" }
                },
                tooltip: {
                    backgroundColor: 'rgba(0,0,0,0.8)',
                    padding: 12,
                    titleFont: { size: 14, family: "'Noto Sans KR', sans-serif" },
                    bodyFont: { size: 13, family: "'Noto Sans KR', sans-serif" },
                    callbacks: {
                        label: (ctx) => `온도: ${ctx.parsed.y.toFixed(1)}°C`
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    ticks: {
                        callback: (value) => value + '°C',
                        font: { family: "'Noto Sans KR', sans-serif" }
                    },
                    grid: { color: 'rgba(0,0,0,0.05)' }
                },
                x: {
                    ticks: { font: { family: "'Noto Sans KR', sans-serif" } },
                    grid: { color: 'rgba(0,0,0,0.05)' }
                }
            }
        }
    });
}

// 차트 업데이트
function updateChart(city, tempType = currentTempType) {
    currentCity = city;
    currentTempType = tempType;
    
    if (!city.fourDayData || city.fourDayData.length === 0) {
        console.warn('예보 데이터 없음:', city.name);
        return;
    }
    
    const labels = city.fourDayData.map((d, i) => i === 0 ? '오늘' : `${i}일 후`);
    let data, label, color, bg;
    
    if (tempType === 'avg') {
        data = city.fourDayData.map(d => parseFloat(d.Avg_Temp.toFixed(1)));
        label = '평균 온도';
        color = '#667eea';
        bg = 'rgba(102,126,234,0.1)';
    } else if (tempType === 'max') {
        data = city.fourDayData.map(d => parseFloat(d.Max_Temp.toFixed(1)));
        label = '최고 온도';
        color = '#ff5252';
        bg = 'rgba(255,82,82,0.1)';
    } else {
        data = city.fourDayData.map(d => parseFloat(d.Min_Temp.toFixed(1)));
        label = '최저 온도';
        color = '#2196f3';
        bg = 'rgba(33,150,243,0.1)';
    }
    
    temperatureChart.data.labels = labels;
    temperatureChart.data.datasets[0].data = data;
    temperatureChart.data.datasets[0].label = label;
    temperatureChart.data.datasets[0].borderColor = color;
    temperatureChart.data.datasets[0].backgroundColor = bg;
    temperatureChart.data.datasets[0].pointBackgroundColor = color;
    temperatureChart.options.plugins.title.text = `${city.name} - ${label} 추이 (5일)`;
    temperatureChart.update();
}

// 통계 업데이트
function updateStatistics(cities) {
    const temps = cities.map(c => c.temperature);
    const hottestTemp = Math.max(...temps);
    const coldestTemp = Math.min(...temps);
    const avgTemp = (temps.reduce((a, b) => a + b, 0) / temps.length).toFixed(1);
    
    const hottest = cities.find(c => c.temperature === hottestTemp);
    const coldest = cities.find(c => c.temperature === coldestTemp);
    
    document.getElementById('hottestCity').textContent = hottest.name;
    document.getElementById('hottestTemp').textContent = `${hottestTemp}°C`;
    document.getElementById('coldestCity').textContent = coldest.name;
    document.getElementById('coldestTemp').textContent = `${coldestTemp}°C`;
    document.getElementById('avgTemp').textContent = `${avgTemp}°C`;
    document.getElementById('cityCount').textContent = `${cities.length}개`;
}

// 버튼 이벤트
function setupButtons() {
    document.querySelectorAll('.period-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.period-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            const type = this.dataset.type;
            if (currentCity) updateChart(currentCity, type);
        });
    });
}

// 초기화
async function init() {
    initMap();
    initChart();
    setupButtons();
    
    const data = await fetchWeatherData();
    weatherData = data.cities;
    
    if (weatherData.length > 0) {
        addMarkers(weatherData);
        updateStatistics(weatherData);
        
        // 서울 기본 선택
        const seoul = weatherData.find(c => c.name === 'Seoul');
        if (seoul) {
            showCityInfo(seoul);
            updateChart(seoul);
        }
        
        console.log('✅ 초기화 완료:', weatherData.length, '개 도시');
    } else {
        console.error('❌ 데이터 없음');
    }
}

document.addEventListener('DOMContentLoaded', init);
