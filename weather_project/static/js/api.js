// API 호출 및 데이터 통합
async function fetchWeatherData() {
    try {
        // API 1: 현재 날씨
        const currentResponse = await fetch('/api/current');
        if (!currentResponse.ok) {
            throw new Error(`현재 날씨 API 실패: ${currentResponse.status}`);
        }
        const currentData = await currentResponse.json();
        
        // API 2: 예보 데이터
        const forecastResponse = await fetch('/api/forecast');
        if (!forecastResponse.ok) {
            throw new Error(`예보 API 실패: ${forecastResponse.status}`);
        }
        const forecastData = await forecastResponse.json();
        
        console.log('✅ 현재 날씨 타입:', typeof currentData, Array.isArray(currentData));
        console.log('✅ 현재 날씨 데이터:', currentData);
        console.log('✅ 예보 타입:', typeof forecastData, Array.isArray(forecastData));
        console.log('✅ 예보 데이터:', forecastData);
        
        // 배열 체크
        if (!Array.isArray(currentData)) {
            throw new Error('현재 날씨 데이터가 배열이 아님');
        }
        if (!Array.isArray(forecastData)) {
            throw new Error('예보 데이터가 배열이 아님');
        }
        
        // 예보 데이터를 도시별로 그룹화
        const forecastMap = new Map();
        forecastData.forEach(item => {
            if (!forecastMap.has(item.City)) {
                forecastMap.set(item.City, []);
            }
            forecastMap.get(item.City).push(item);
        });
        
        // 통합
        const cities = [];
        currentData.forEach(current => {
            const forecasts = forecastMap.get(current.City) || [];
            forecasts.sort((a, b) => a.Date.localeCompare(b.Date));
            
            cities.push({
                name: current.City,
                nameEn: current.City,
                lat: current.Latitude,
                lon: current.longitude,
                temperature: current.Temperature,
                weather: current.Weather.trim(),
                weatherIcon: getWeatherIcon(current.Weather),
                country: getCityCountry(current.City),
                timezone: getCityTimezone(current.City),
                fourDayData: forecasts.slice(0, 5)
            });
        });
        
        console.log('✅ 통합 완료:', cities.length, '개 도시');
        return { cities };
        
    } catch (error) {
        console.error('❌ API 에러:', error);
        alert('API 서버 에러: ' + error.message + '\n\nFlask 서버가 실행 중인지 확인하세요.');
        return { cities: [] };
    }
}

function getWeatherIcon(weather) {
    const w = weather.toLowerCase();
    if (w.includes('clear')) return 'fa-sun';
    if (w.includes('rain')) return 'fa-cloud-rain';
    if (w.includes('cloud')) return 'fa-cloud';
    if (w.includes('snow')) return 'fa-snowflake';
    if (w.includes('mist') || w.includes('haze')) return 'fa-smog';
    return 'fa-cloud-sun';
}

function getCityCountry(city) {
    const map = {
        'Bangkok': '태국', 'Beijing': '중국', 'Berlin': '독일',
        'Buenos Aires': '아르헨티나', 'Cairo': '이집트', 'Dubai': 'UAE',
        'Lagos': '나이지리아', 'London': '영국', 'Madrid': '스페인',
        'Mexico City': '멕시코', 'Mumbai': '인도', 'New York': '미국',
        'Paris': '프랑스', 'Rome': '이탈리아', 'Sao Paulo': '브라질',
        'Seoul': '대한민국', 'Singapore': '싱가포르', 'Sydney': '호주',
        'Tokyo': '일본', 'Toronto': '캐나다'
    };
    return map[city] || '알 수 없음';
}

function getCityTimezone(city) {
    const map = {
        'Bangkok': 'Asia/Bangkok', 'Beijing': 'Asia/Shanghai', 'Berlin': 'Europe/Berlin',
        'Buenos Aires': 'America/Argentina/Buenos_Aires', 'Cairo': 'Africa/Cairo', 'Dubai': 'Asia/Dubai',
        'Lagos': 'Africa/Lagos', 'London': 'Europe/London', 'Madrid': 'Europe/Madrid',
        'Mexico City': 'America/Mexico_City', 'Mumbai': 'Asia/Kolkata', 'New York': 'America/New_York',
        'Paris': 'Europe/Paris', 'Rome': 'Europe/Rome', 'Sao Paulo': 'America/Sao_Paulo',
        'Seoul': 'Asia/Seoul', 'Singapore': 'Asia/Singapore', 'Sydney': 'Australia/Sydney',
        'Tokyo': 'Asia/Tokyo', 'Toronto': 'America/Toronto'
    };
    return map[city] || 'UTC';
}
