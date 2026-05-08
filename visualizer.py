import matplotlib.pyplot as plt
import seaborn as sns
from processor import load_and_clean_data
import os


def create_charts(df):
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(14, 7))

    # Boxplot for all cities
    chart = sns.boxplot(x='city', y='price_per_m2', data=df, palette='Spectral')

    plt.title('Rental Price Comparison across Major German Cities', fontsize=16)
    plt.xticks(rotation=45)  # Rotate names so they don't overlap
    plt.ylabel('Euro per m2')

    plt.tight_layout()
    plt.savefig('static/price_comparison.png')
    print("✅ New chart saved with expanded city list.")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, 'data', 'immo_data.csv')
    data = load_and_clean_data(data_path)
    if data is not None:
        create_charts(data)