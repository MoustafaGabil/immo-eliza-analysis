import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter
import warnings
import os

def IQR_for_outliers(data, property_types, output_dir):
    combined_data_no_outlier = pd.DataFrame()  # Empty DataFrame to hold combined data

    for property_type in property_types:
        pro = data[data["PropertyType"] == property_type]
        percentile25 = pro["Price"].quantile(0.25)
        percentile75 = pro["Price"].quantile(0.75)
        IQR = percentile75 - percentile25

        upper_limit = percentile75 + 1.5 * IQR  # Determine upper and lower limits for outliers
        lower_limit = percentile25 - 1.5 * IQR
        data_no_outlier = pro[(pro["Price"] <= upper_limit) & (pro["Price"] >= lower_limit)]  # Remove outliers

        individual_filename = f"{property_type}_without_outliers.csv"  # Saving the data separately
        data_no_outlier.to_csv(f"{output_dir}/{individual_filename}", index=False)

        combined_data_no_outlier = pd.concat([combined_data_no_outlier, data_no_outlier], ignore_index=True)  # Append to combined DataFrame

    # Save the combined data without outliers to a single CSV file
    combined_filename = "Houses_and_Apartments_combined_without_outliers.csv"
    combined_data_no_outlier.to_csv(f"{output_dir}/{combined_filename}", index=False)

    return combined_data_no_outlier


def plot_price_distribution(data_with_outliers, data_no_outlier, property_type,output_dir):
    warnings.filterwarnings('ignore')

    # Plotting distributions and boxplots
    plt.figure(figsize=(16, 12))

    # Distribution with outliers
    plt.subplot(2, 2, 1)
    sns.histplot(data_with_outliers['Price'], bins=30, kde=True)
    plt.title(f'Distribution of {property_type} Prices in Belgium with Outliers')
    plt.ylabel('Frequency of Prices')
    plt.xlabel('Price (€)')
    plt.ticklabel_format(style='plain', axis='x')
    plt.xticks(rotation=15)

    # Boxplot with outliers
    plt.subplot(2, 2, 2)
    sns.boxplot(x=data_with_outliers['Price'])
    formatter = FuncFormatter(lambda x, _: f'{int(x):,}')
    plt.gca().xaxis.set_major_formatter(formatter)
    plt.title(f'Boxplot of {property_type} Prices in Belgium with Outliers')
    plt.xlabel('Price (€)')
    plt.xticks(rotation=15)

    # Distribution without outliers
    plt.subplot(2, 2, 3)
    sns.histplot(data_no_outlier['Price'], bins=30, kde=True)
    plt.title(f'Distribution of {property_type} Prices in Belgium Without Outliers')
    plt.ylabel('Frequency of Prices')
    plt.xlabel('Price (€)')
    plt.ticklabel_format(style='plain', axis='x')
    plt.xticks(rotation=15)

    # Boxplot without outliers
    plt.subplot(2, 2, 4)
    sns.boxplot(x=data_no_outlier['Price'])
    formatter = FuncFormatter(lambda x, _: f'{int(x):,}')
    plt.gca().xaxis.set_major_formatter(formatter)
    plt.title(f'Boxplot of {property_type} Prices in Belgium Without Outliers')
    plt.xlabel('Price (€)')
    plt.xticks(rotation=15)

        # Save or show the plots
    if output_dir:
        plot_filename = os.path.join(output_dir, f'{property_type}_price_distribution.png')
        plt.savefig(plot_filename, bbox_inches='tight')
        print(f"Plot saved to {plot_filename}")
    else:
        plt.show()

    # Close the plot to free memory
    plt.close()
