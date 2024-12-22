import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd

def prepare_data(data):
    data['Price'] = pd.to_numeric(data['Price'], errors='coerce')
    data['LivingArea'] = pd.to_numeric(data['LivingArea'], errors='coerce')

    # Remove rows with missing or invalid data
    data_cleaned = data.dropna(subset=['Price', 'LivingArea'])
    data_cleaned = data_cleaned[data_cleaned['LivingArea'] > 0]

    # Calculate price per sqm
    data_cleaned['Price_per_sqm'] = data_cleaned['Price'] / data_cleaned['LivingArea']

    return data_cleaned


def calculate_grouped_stats(data_cleaned):
    grouped_stats = data_cleaned.groupby(['Region', 'Province', 'District', 'Locality']).agg(
        Average_price=('Price', 'mean'),
        Average_price_per_sqm=('Price_per_sqm', 'mean')
    ).reset_index()

    # Round Average Price per sqm
    grouped_stats['Average_price_per_sqm'] = grouped_stats['Average_price_per_sqm'].round(0)

    return grouped_stats


def get_top_localities_per_region(df, n=5):
    cheapest = df.groupby('Region').apply(lambda x: x.nsmallest(n, 'Average_price_per_sqm')).reset_index(drop=True)
    most_expensive = df.groupby('Region').apply(lambda x: x.nlargest(n, 'Average_price_per_sqm')).reset_index(drop=True)
    return cheapest, most_expensive

def plot_localities(data, title, xlabel, ylabel, output_file=None):
    plt.figure(figsize=(12, 8))
    for region in data['Region'].unique():
        region_data = data[data['Region'] == region]
        plt.bar(region_data['Locality'], region_data['Average_price_per_sqm'], label=region)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=90)  # Rotate x-axis labels for better readability
    plt.legend(title='Region', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    # Save or show the plot
    if output_file:
        plt.savefig(output_file, bbox_inches='tight')
        print(f"Plot saved to {output_file}")
    else:
        plt.show()

    plt.close()

