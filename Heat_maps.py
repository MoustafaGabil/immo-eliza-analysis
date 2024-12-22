import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
def heat_maps_data_encoding (input_path_for_maps):
        # Filter the DataFrame for a specific region
    data_totl = pd.read_csv(input_path_for_maps)
    # Dictionary to map kitchen types to numerical values
    kitchen_type_assig = {
        "NOT_INSTALLED": 0,
        "USA_UNINSTALLED": 0,
        "SEMI_EQUIPPED": 1,
        "USA_SEMI_EQUIPPED": 2,
        "INSTALLED": 3,
        "USA_INSTALLED": 4,
        "HYPER_EQUIPPED": 5,
        "USA_HYPER_EQUIPPED": 6
    }

    # Dictionary to map building conditions to numerical values
    building_con = {
        "TO_RESTORE": 0,
        "TO_RENOVATE": 0,
        "TO_BE_DONE_UP": 1,
        "GOOD": 3,
        "JUST_RENOVATED": 4,
        "AS_NEW": 5
    }

    # Applying the mapping to the columns in the dataframe
    data_totl['KitchenType_Q'] = data_totl['KitchenType'].replace(kitchen_type_assig)
    data_totl['building_cond_Q'] = data_totl['StateBuilding'].replace(building_con)
    
    return data_totl


def heat_map(data,output_dir):
    ############################ for ALL Properties ######################
    selected_parameters = data[['Price', 'FacadeCount', 'BedroomCount', 'LivingArea','Terrace_Area','Garden_Area','ConstructionYear','KitchenType_Q','building_cond_Q']]
    correlation_matrix = selected_parameters.corr(method='spearman')
    plt.figure(figsize=(8,6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
    name='Correlation Matrix Heatmap for ALL Properties'
    plt.title(name)
    if output_dir:
        plot_filename = os.path.join(output_dir, name +'.png')
        plt.savefig(plot_filename, bbox_inches='tight')
        print(f"Plot saved to {plot_filename}")
    else:
        plt.show()
        
    ############################ For Houses and Apartments ###############
    PropertySubtype = ['HOUSE','APARTMENT']
    for property in PropertySubtype:
        data =data[data['PropertySubtype']== property] 
        correlation_matrix = selected_parameters.corr(method='spearman')
        plt.figure(figsize=(8,6))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
        map_title = f'Correlation Matrix Heatmap for {property}'
        plt.title(map_title)
        if output_dir:
            plot_filename = os.path.join(output_dir, map_title +'.png')
            plt.savefig(plot_filename, bbox_inches='tight')
            print(f"Plot saved to {plot_filename}")
        else:
            plt.show()
            
    ############################ per region ############################
    regions = ['Brussels','Flanders','Wallonie']
    for region in regions:
        data =data[data['Region'] == region] 
        correlation_matrix = selected_parameters.corr(method='spearman')
        plt.figure(figsize=(8,6))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
        map_title = f'Correlation Matrix Heatmap for houses and apartments in {region}'
        plt.title(map_title)
        if output_dir:
            plot_filename = os.path.join(output_dir, map_title +'.png')
            plt.savefig(plot_filename, bbox_inches='tight')
            print(f"Plot saved to {plot_filename}")
        else:
            plt.show()
    




