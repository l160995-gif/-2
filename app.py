from flask import Flask, render_template_string, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# Словник для перекладу днів тижня
DAYS_UA = {
    0: 'понеділок',
    1: 'вівторок',
    2: 'середа',
    3: 'четвер',
    4: 'п\'ятниця',
    5: 'субота',
    6: 'неділя'
}

def get_correct_day_form(days):
    """Повертає правильну форму слова 'день' залежно від числа"""
    if days % 10 == 1 and days % 100 != 11:
        return 'день'
    elif days % 10 in [2, 3, 4] and days % 100 not in [12, 13, 14]:
        return 'дні'
    else:
        return 'днів'

def calculate_days_to_saturday():
    """Обчислює кількість днів до наступної суботи"""
    now = datetime.now()
    current_day = now.weekday()  # 0 = понеділок, 5 = субота, 6 = неділя
    
    # Обчислюємо різницю днів до суботи
    if current_day == 5:  # Якщо сьогодні субота
        days_until_saturday = 7
    else:
        days_until_saturday = (5 - current_day) % 7
    
    # Дата наступної суботи
    next_saturday = now + timedelta(days=days_until_saturday)
    
    return {
        'days': days_until_saturday,
        'current_date': now,
        'next_saturday': next_saturday,
        'current_day_name': DAYS_UA[current_day]
    }

# HTML шаблон
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Зворотній відлік до суботи</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            border: 1px solid rgba(255, 255, 255, 0.18);
            max-width: 500px;
            width: 100%;
            text-align: center;
        }
        
        h1 {
            color: white;
            font-size: 2.5em;
            margin-bottom: 30px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        }
        
        .countdown {
            background: rgba(255, 255, 255, 0.25);
            border-radius: 15px;
            padding: 30px;
            margin: 20px 0;
        }
        
        .days-number {
            font-size: 5em;
            font-weight: bold;
            color: #fff;
            text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.3);
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% {
                transform: scale(1);
            }
            50% {
                transform: scale(1.05);
            }
        }
        
        .days-text {
            font-size: 1.5em;
            color: white;
            margin-top: 10px;
            font-weight: 500;
        }
        
        .info-block {
            background: rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
            color: white;
        }
        
        .info-row {
            display: flex;
            justify-content: space-between;
            margin: 10px 0;
            font-size: 1.1em;
        }
        
        .label {
            font-weight: 600;
        }
        
        .emoji {
            font-size: 1.5em;
            margin-right: 10px;
        }
        
        @media (max-width: 600px) {
            h1 {
                font-size: 1.8em;
            }
            
            .days-number {
                font-size: 3.5em;
            }
            
            .container {
                padding: 25px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1><span class="emoji">📅</span>Зворотній відлік до суботи</h1>
        
        <div class="countdown">
            <div class="days-number">{{ data.days }}</div>
            <div class="days-text">{{ day_form }}</div>
        </div>
        
        <div class="info-block">
            <div class="info-row">
                <span class="label"><span class="emoji">🗓️</span>Сьогодні:</span>
                <span>{{ data.current_day_name }}, {{ data.current_date.strftime('%d.%m.%Y') }}</span>
            </div>
            <div class="info-row">
                <span class="label"><span class="emoji">🎉</span>Наступна субота:</span>
                <span>{{ data.next_saturday.strftime('%d.%m.%Y') }}</span>
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    """Головна сторінка з відліком"""
    data = calculate_days_to_saturday()
    day_form = get_correct_day_form(data['days'])
    return render_template_string(HTML_TEMPLATE, data=data, day_form=day_form)

@app.route('/api/countdown')
def api_countdown():
    """API ендпоінт для отримання даних у JSON форматі"""
    data = calculate_days_to_saturday()
    return jsonify({
        'days_until_saturday': data['days'],
        'current_date': data['current_date'].strftime('%Y-%m-%d'),
        'current_day': data['current_day_name'],
        'next_saturday': data['next_saturday'].strftime('%Y-%m-%d'),
        'day_form': get_correct_day_form(data['days'])
    })

@app.route('/health')
def health():
    """Ендпоінт для перевірки здоров'я застосунку"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)