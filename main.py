import pandas as pd
from cleaning import cleaning_data 
from removing_outliers import IQR_for_outliers , plot_price_distribution
from Average_prices_maps import ave_price_map , ploting_prices_localities, Bel_Province_map
from Heat_maps import heat_maps_data_encoding , heat_map
from Exploratory_Data_Analysis import prepare_data, calculate_grouped_stats, get_top_localities_per_region,plot_localities

if __name__ == "__main__":

    # Define file paths
    row_data_path = r"Data\properties.csv"
    cleaned_data_path = r"Data\properties_cleaned.csv"
    outputs_data_after_outliers_removal = r"Results\Data_after_outliers_removal"
    outliers_removal_figure_output = r'Results\Graphs'
    price_maps_path = r'Results\Belgium_average_prices_maps'
    Heat_maps_path = r'Results\Heat_Maps'
    input_path_for_maps = r"Results\Data_after_outliers_removal\Houses_and_Apartments_combined_without_outliers.csv"
    #-------------------------------  Cleaning the data ----------------------------
    data = pd.read_csv(row_data_path)
    cleaned_data = cleaning_data(data,cleaned_data_path)

    #------------------------------ Removing outliers ------------------------------
    property_types = ["APARTMENT", "HOUSE"]
    combined_data_no_outliers = IQR_for_outliers(cleaned_data, property_types, outputs_data_after_outliers_removal)

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
            output_dir=outliers_removal_figure_output
        )
        
    #------------------------------ Exploratory Data Analysis (EDA) ------------------------------   
    data = pd.read_csv(cleaned_data_path)
    data_cleaned = prepare_data(data)
    grouped_stats = calculate_grouped_stats(data_cleaned)
    cheapest_localities, most_expensive_localities = get_top_localities_per_region(grouped_stats)

    # Plotting
    plot_localities(cheapest_localities,
        title="Cheapest localities by region",
        xlabel="Locality",
        ylabel="Avg Price per sqm (€)",
        output_file="Results/Graphs/cheapest_localities.png"
    )

    plot_localities(most_expensive_localities,
        title="Most expensive localities by region",
        xlabel="Locality",
        ylabel="Avg Price per sqm (€)",
        output_file="Results/Graphs/most_expensive_localities.png"
    )
    
    #------------------------------ Heat maps creation ------------------------------
    heat_map(data=heat_maps_data_encoding(input_path_for_maps),output_dir = Heat_maps_path)
        #------------------------------ creating prices maps over Belgium and for Brusels localities ------------------------------
    for property in property_types:
        # Data with outliers
        ploting_prices_localities(data=ave_price_map (input_path_for_maps, Property = property ),colour_bar="OrRd", fig_title=f"Average {property} Prices of Localities over Brussels Province",
                                region_name='NAME_FRE',property_type =property, output_dir =price_maps_path, map_type = "prices distrubution over Brussels")
        ploting_prices_localities(data=Bel_Province_map (input_path_for_maps, Property = property ),colour_bar="Blues", fig_title=f'Average {property} Prices over Belgium Provinces',
                                region_name='NAME_2',property_type =property, output_dir =price_maps_path,map_type = "prices distrubution over Belgium")
        


