
from flask import Flask, render_template, request
import plotly.express as px
import plotly.utils
import json
import os
from datetime import datetime
from processor import load_and_clean_data, get_market_stats

app = Flask(__name__)

# Load data once
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'immo_data.csv')
df = load_and_clean_data(DATA_PATH)
market_stats = get_market_stats(df)


@app.route('/', methods=['GET', 'POST'])
def home():
    all_cities = sorted(df['city'].unique())

    # --- CHART GENERATION ---
    top_cities = df['city'].value_counts().nlargest(12).index
    fig = px.box(df[df['city'].isin(top_cities)], x="city", y="price_per_m2",
                 color="city", template="plotly_white", points=False)

    fig.update_layout(
        hovermode="x unified",
        margin=dict(l=5, r=5, t=20, b=5),
        showlegend=False,
        height=380  # Optimized for Laptop screens
    )
    fig.update_xaxes(showspikes=True, spikecolor="#3b82f6", spikethickness=1)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    recommendation = None
    count = 0
    searched = False

    if request.method == 'POST':
        searched = True
        city = request.form.get('city')
        budget = float(request.form.get('budget'))
        rooms = float(request.form.get('rooms', 1))

        mask = (df['city'] == city) & (df['totalRent'] <= budget) & (df['noRooms'] >= rooms)

        if request.form.get('kitchen'): mask &= (df['hasKitchen'] == True)
        if request.form.get('balcony'): mask &= (df['balcony'] == True)
        if request.form.get('garden'): mask &= (df['garden'] == True)
        if request.form.get('lift'): mask &= (df['lift'] == True)
        if request.form.get('pets') == 'allowed': mask &= (df['petsAllowed'].isin(['yes', 'negotiable']))

        filtered = df[mask]
        count = len(filtered)
        if not filtered.empty:
            recommendation = filtered['district'].value_counts().head(5).to_dict()

    return render_template('index.html', cities=all_cities, graphJSON=graphJSON,
                           recommendation=recommendation, count=count,
                           stats=market_stats, year=datetime.now().year, searched=searched)


if __name__ == '__main__':
    app.run(debug=True)
