from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    news = None
    text = get_text()

    if request.method == 'POST':
        city = request.form['city']
        weather = get_weather(city)
        news = get_news()

    return render_template('index.html', weather=weather, news=news, text=text)


def get_weather(city):
    api_key = "81ab40c96d780b9b15aeba02b8f6b143"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    return response.json()


def get_news():
    api_key = "5da0819151604e68a5ffeeecbe386cf1"
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    response = requests.get(url)
    return response.json().get('articles', [])


def get_text():
    url = "https://zenquotes.io/api/random"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()[0]  # ZenQuotes возвращает список
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return {"content": "Unable to fetch quote at the moment."}
    except ValueError:
        print("Invalid JSON response")
        return {"content": "Invalid response from API."}


if __name__ == '__main__':
    app.run(debug=True)