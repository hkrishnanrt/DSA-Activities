from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

CSV_PATH = "data/Cleaned.csv"
df = pd.read_csv(CSV_PATH)
df['type'] = df['type'].astype(str)
df['director'] = df['director'].astype(str)
df['country'] = df['country'].astype(str)
df['cast'] = df['cast'].astype(str)
df['title'] = df['title'].astype(str)

CONTENT_TYPES = sorted(df['type'].dropna().unique().tolist())

def get_aggregations(sub_df):
    directors = sub_df['director'].dropna().str.strip()
    directors = directors[directors.str.lower() != 'unknown']
    top_directors = directors.value_counts().head(10)

    countries = sub_df['country'].dropna().str.strip()
    countries = countries[countries.str.lower() != 'unknown']
    top_countries = countries.value_counts().head(10)

    cast_series = (
        sub_df['cast'].dropna()
        .str.split(',')
        .explode()
        .str.strip()
    )
    cast_series = cast_series[
        cast_series.str.lower().ne('unknown') & (cast_series != '')
    ]
    top_actors = cast_series.value_counts().head(10)

    return {
        'top_directors': top_directors,
        'top_countries': top_countries,
        'top_actors': top_actors
    }

@app.route('/', methods=['GET', 'POST'])
def home():
    selected_type = request.form.get('content_type', 'All')
    search_title = request.form.get('search_title', '').strip()

    filtered_df = df
    if selected_type and selected_type != 'All':
        filtered_df = filtered_df[filtered_df['type'] == selected_type]
    if search_title:
        filtered_df = filtered_df[filtered_df['title'].str.contains(search_title, case=False, na=False)]

    aggs = get_aggregations(filtered_df)
    return render_template(
        'index.html',
        content_types=['All'] + CONTENT_TYPES,
        selected_type=selected_type,
        search_title=search_title,
        top_directors=aggs['top_directors'].items(),
        top_countries=aggs['top_countries'].items(),
        top_actors=aggs['top_actors'].items()
    )

if __name__ == "__main__":
    app.run(debug=True)