import numpy as np
import pandas as pd
from Cleaning.cleaning import cleaning_data  # Import the cleaning function
from Cleaning.removing_outliers import IQR_for_outliers , plot_price_distribution
from Average_prices_maps import ave_price_map , ploting_prices_localities, Bel_Province_map
import os

# Define file paths
row_data_path = r"Cleaning\properties.csv"
cleaned_data_path = r"Cleaning\properties_cleaned.csv"
graphs_output_path = r"Results\final_Data_results"
figure_output = r'Results\Graphs'
price_maps_path = r'Results\Belgium_average_prices_maps'
Heat_maps_path = r'Results\Heat_Maps'
path_for_maps = r"Results\final_Data_results\Houses_and_Apartments_combined_without_outliers.csv"
#-------------------------------  Cleaning the data ----------------------------
data = pd.read_csv(row_data_path)
cleaned_data = cleaning_data(data,cleaned_data_path)

#------------------------------ Removing outliers ------------------------------
property_types = ["APARTMENT", "HOUSE"]
combined_data_no_outliers = IQR_for_outliers(cleaned_data, property_types, graphs_output_path)

print("Data cleaning and outlier removal complete.")

#Plot distributions for each property type
for property_type in property_types:
    # Data with outliers
    data_with_outliers = cleaned_data[cleaned_data["PropertyType"] == property_type]
    
    # Data without outliers
    data_no_outliers = combined_data_no_outliers[combined_data_no_outliers["PropertyType"] == property_type]
    
    # Plot the distributions
    plot_price_distribution(
        data_with_outliers=data_with_outliers,
        data_no_outlier=data_no_outliers,
        property_type=property_type,
        output_dir=figure_output
    )

#------------------------------ creating prices maps over Belgium and for Brusels localities ------------------------------
for property in property_types:
    # Data with outliers
    ploting_prices_localities(data=ave_price_map (path_for_maps, Property = property ),colour_bar="OrRd", fig_title=f"Average {property} Prices of Localities over Brussels Province",
                            region_name='NAME_FRE',property_type =property, output_dir =price_maps_path, map_type = "prices distrubution over Brussels")
    ploting_prices_localities(data=Bel_Province_map (path_for_maps, Property = property ),colour_bar="Blues", fig_title=f'Average {property} Prices over Belgium Provinces',
                            region_name='NAME_2',property_type =property, output_dir =price_maps_path,map_type = "prices distrubution over Belgium")
    
#------------------------------ Heat maps creation ------------------------------

