from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_BASE = "https://api.pokemontcg.io/v2"
HEADERS = {"X-Api-Key": "1abf4078-c671-4458-8a48-b518d8460372"}  # Eğer anahtar gerekiyorsa buraya ekle

@app.route('/')
def index():
    query = request.args.get('q', '')
    set_query = request.args.get('set', '')
    page = int(request.args.get('page', 1))
    page_size = 25

    params = {
        'page': page,
        'pageSize': page_size
    }

    if query:
        params['q'] = f'name:{query}*'
    if set_query:
        params['q'] = f'set.name:{set_query}'

    response = requests.get(f'{API_BASE}/cards', headers=HEADERS, params=params)
    data = response.json().get('data', [])
    total_count = int(response.json().get('totalCount', len(data)))
    total_pages = (total_count + page_size - 1) // page_size

    return render_template(
        'index.html',
        cards=data,
        query=query,
        set_query=set_query,
        page=page,
        total_pages=total_pages
    )

TYPE_ALIASES = {
    "Metal": "Steel",
    "Lightning": "Electric",
    "Darkness": "Dark",
    "Colorless": "Normal"  # istersen burada bırakabilirsin
}

@app.route('/card/<card_id>')
def card_detail(card_id):
    res = requests.get(f"{API_BASE}/cards/{card_id}", headers=HEADERS)
    card = res.json().get("data", {})

    # Tip adlarını dönüştür
    if "types" in card:
        card["types"] = [TYPE_ALIASES.get(t, t) for t in card["types"]]

    return render_template("card_detail.html", card=card)

if __name__ == '__main__':
    app.run(debug=True)

