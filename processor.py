
import pandas as pd


def load_and_clean_data(filepath):
    try:
        # Load the CSV
        df = pd.read_csv(filepath, low_memory=False)

        # Mapping Kaggle columns to clean names
        cols = {
            'regio2': 'city', 'regio3': 'district', 'baseRent': 'baseRent',
            'totalRent': 'totalRent', 'livingSpace': 'livingSpace',
            'noRooms': 'noRooms', 'hasKitchen': 'hasKitchen', 'balcony': 'balcony',
            'petsAllowed': 'petsAllowed', 'garden': 'garden', 'lift': 'lift'
        }

        # Filter existing columns and rename
        df = df[list(cols.keys())].rename(columns=cols)
        df = df.dropna(subset=['baseRent', 'livingSpace', 'city'])

        # Formatting
        df['city'] = df['city'].str.title().str.replace('_', ' ')
        df['district'] = df['district'].str.replace('_', ' ')

        # Outlier filtering
        df = df[(df['baseRent'] > 150) & (df['baseRent'] < 8000)]
        df['price_per_m2'] = (df['baseRent'] / df['livingSpace']).round(2)

        return df
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def get_market_stats(df):
    return {
        'total_listings': f"{len(df):,}",
        'avg_rent': f"€{round(df['totalRent'].mean(), 2)}",
        'city_count': df['city'].nunique(),
        'top_city': df.groupby('city')['price_per_m2'].mean().idxmax()
    }
