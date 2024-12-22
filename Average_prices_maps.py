import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import os
# import matplotlib.ticker as ticker

def ave_price_map (Data_path_for_maps,Property):
    locality_mapping = {
    'Ixelles': 'Ixelles',
    'IXELLES': 'Ixelles',
    'Elsene': 'Ixelles',  
    'Ixelles - Chatelain': 'Ixelles',
    
    'Molenbeek-Saint-Jean': 'Molenbeek-Saint-Jean',
    'MOLENBEEK-SAINT-JEAN': 'Molenbeek-Saint-Jean',
    'Molenbeek-saint-jean': 'Molenbeek-Saint-Jean',
    'Sint-Jans-Molenbeek': 'Molenbeek-Saint-Jean',
    'SINT-JANS-MOLENBEEK': 'Molenbeek-Saint-Jean',

    'Auderghem': 'Auderghem',
    'AUDERGHEM': 'Auderghem',
    'Auderghem - Oudergem': 'Auderghem',

    'Saint-Gilles': 'Saint-Gilles',
    'SAINT-GILLES': 'Saint-Gilles',
    'Sint-Gillis': 'Saint-Gilles',

    'Watermael-Boitsfort': 'Watermael-Boitsfort',
    'WATERMAEL-BOITSFORT': 'Watermael-Boitsfort',

    'Schaerbeek': 'Schaerbeek',
    'Schaarbeek': 'Schaerbeek',
    'SCHAERBEEK': 'Schaerbeek',

    'Saint-Josse-Ten-Noode': 'Saint-Josse-ten-Noode',
    'SAINT-JOSSE-TEN-NOODE': 'Saint-Josse-ten-Noode',

    'Woluwe-Saint-Lambert': 'Woluwe-Saint-Lambert',
    'WOLUWE-SAINT-LAMBERT': 'Woluwe-Saint-Lambert',
    'Sint-Lambrechts-Woluwe': 'Woluwe-Saint-Lambert',
    'Woluwé-Saint-Lambert': 'Woluwe-Saint-Lambert',

    'Bruxelles': 'Bruxelles',
    'BRUXELLES': 'Bruxelles',
    'Brussels': 'Bruxelles',
    'BRUSSEL': 'Bruxelles',
    'Brussel': 'Bruxelles',
    'Bruxelles  2': 'Bruxelles',
    'Brussel 1': 'Bruxelles',
    'Pentagone (Bruxelles)': 'Bruxelles',

    'Berchem-Sainte-Agathe': 'Berchem-Sainte-Agathe',
    'BERCHEM-SAINTE-AGATHE': 'Berchem-Sainte-Agathe',
    'Sint-Agatha-Berchem': 'Berchem-Sainte-Agathe',
    'SINT-AGATHA-BERCHEM': 'Berchem-Sainte-Agathe',
    'Etterbeek': 'Etterbeek',
    'ETTERBEEK': 'Etterbeek',
    'Evere': 'Evere',
    'Jette': 'Jette',
    'JETTE': 'Jette',
    'Koekelberg': 'Koekelberg',
    'KOEKELBERG': 'Koekelberg',
    'Anderlecht': 'Anderlecht',
    'ANDERLECHT': 'Anderlecht',
    'Forest': 'Forest',
    'FOREST': 'Forest',
    'Vorst': 'Forest',  
    'Vorst': 'Forest',
    'Ganshoren': 'Ganshoren',
    'GANSHOREN': 'Ganshoren',
    'Uccle': 'Uccle',
    'UKKEL': 'Uccle',  
    'Ukkel': 'Uccle',
    'UCCLE': 'Uccle',
    'Woluwe-Saint-Pierre': 'Woluwe-Saint-Pierre',
    'WOLUWE-SAINT-PIERRE': 'Woluwe-Saint-Pierre',
    'Laeken': 'Laeken',
    'LAEKEN': 'Laeken',
    'LAEKEN (BRU.)': 'Laeken',
    'Neder-over-Heembeek': 'Neder-Over-Heembeek',
    'Neder-Over-Heembeek': 'Neder-Over-Heembeek',
    'NEDER-OVER-HEEMBEEK (BRU.)': 'Neder-Over-Heembeek',
    'Haren (Brussel)': 'Haren',
    'HAREN': 'Haren',
    'Sint-Pieters-Woluwe': 'Woluwe-Saint-Pierre'
}
# assigning average prices per municipality
    data = pd.read_csv(Data_path_for_maps) # --> file path

    df_brussels = data[data['Region'] == 'Brussels']
    Brussels_h_A = df_brussels[df_brussels['PropertyType'] == Property]
    Brussels_h_A['Locality'] = Brussels_h_A['Locality'].replace(locality_mapping)
#### The below file is the main/targeted data to be displayed ####
    avg_price_per_locality_houses = Brussels_h_A.groupby('Locality')['Price'].mean().reset_index() 
    # this is the shape file for Brussels Municipalities, sheck the path of it.
    shape_files= r'Data/Brussels_Municipalities/Brussels_-_Municipalities.shp'
    Brussels_localities_map = gpd.read_file(shape_files)
    # merging the average prices based on the localities
    merged_data_localities_houses = Brussels_localities_map.merge(avg_price_per_locality_houses, left_on='NAME_FRE', right_on='Locality')

    return merged_data_localities_houses 

def ploting_prices_localities(data,colour_bar,fig_title, region_name,property_type,output_dir, map_type): 
    fig, ax = plt.subplots(figsize=(10, 10))
    vmin = data['Price'].min()  
    vmax = data['Price'].max()  
    data.plot(column='Price', cmap=colour_bar, ax=ax, edgecolor='black',vmin=vmin, vmax=vmax, legend=False ) # legend=False as it will be set later. 

    # creating the customised colour bar
    sm = plt.cm.ScalarMappable(cmap=colour_bar, norm=plt.Normalize(vmin=vmin, vmax=vmax))
    sm._A = [] # is a workaround to avoid an error that arises when the mappable object does not have any data associated with it.
    cbar = fig.colorbar(sm, ax=ax, shrink=0.65)
    cbar.ax.set_ylabel('Average Price (€)', rotation=270, labelpad=15)
    #cbar.ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.0f'))  # Change format as needed

    # Adding the locality names to the map
    for x, y, label in zip(data.geometry.centroid.x, 
                        data.geometry.centroid.y, 
                        data[region_name]):  # or the standardized name column
            ax.text(x, y, label, fontsize=8, ha='center', color='black', weight='bold', 
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
            plt.title(fig_title, fontsize=15)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    if output_dir:
        plot_filename = os.path.join(output_dir, f'{property_type}_{map_type}.png')
        plt.savefig(plot_filename, bbox_inches='tight')
        print(f"Plot saved to {plot_filename}")
    else:
        plt.show()

    # Close the plot to free memory
    plt.close()
def Bel_Province_map (Data_path_for_maps,Property):
    shape_file =r"Data/BELGIUM_Provinces/BELGIUM_-_Provinces.shp"
    Belgium_Province = gpd.read_file(shape_file)
    data = pd.read_csv(Data_path_for_maps)
    # Standardize province names
    provinces_mapping = {
        'Antwerp': 'Antwerpen',
        'Walloon Brabant': 'Brabant Wallon',
        'Brussels': 'Bruxelles',  
        'Flemish Brabant': 'Vlaams Brabant',
        'East Flanders':'Oost-Vlaanderen',
        'West Flanders':'West-Vlaanderen'
    }
    data['Province'] = data['Province'].replace(provinces_mapping)
    proviencies_a_h = data[data['PropertyType'] == Property]
    avg_price_per_prov_h_a = proviencies_a_h.groupby('Province')['Price'].mean().reset_index()
    merged_data_prov_h_a = Belgium_Province.merge(avg_price_per_prov_h_a, left_on='NAME_2', right_on='Province')
    return merged_data_prov_h_a
