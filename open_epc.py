import os
import sys
import re
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Constants
DATA_FOLDER = "data"
RAW_DATA_FOLDER = "raw"
PLOT_FOLDER = "plots"

def read_data(file_path):
    """Read data from a CSV file."""
    return pd.read_csv(file_path, low_memory=False)

def set_seaborn_style_palette():
    """Set seaborn style and palette."""
    sns.set(style="whitegrid")
    sns.set_palette("viridis")

def save_plot(figure, plot_name, folder):
    """Save a plot to the specified folder."""
    if not os.path.exists(folder):
        os.makedirs(folder)
    figure.savefig(os.path.join(folder, plot_name))
    plt.close()

def process_data(df):
    """Process the data, including setting energy rating order."""
    energy_rating_order = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    df['CURRENT_ENERGY_RATING'] = pd.Categorical(df['CURRENT_ENERGY_RATING'], \
                                                 categories=energy_rating_order, ordered=True)

def plot_horizontal_bar(df):
    """Generate and save a horizontal bar plot."""
    energy_rating_order_dynamic = df['CURRENT_ENERGY_RATING'].cat.categories
    energy_rating_counts = df['CURRENT_ENERGY_RATING'].value_counts().reset_index()
    energy_rating_counts.columns = ['CURRENT_ENERGY_RATING', 'Number of Records']

    plt.figure(figsize=(10, 6))
    sns.barplot(x='Number of Records', y='CURRENT_ENERGY_RATING', data=energy_rating_counts, \
                order=energy_rating_order_dynamic)
    plt.xlabel('Number of Records')
    plt.ylabel('Current Energy Rating')
    plt.title('Distribution of Energy Ratings')
    plt.tight_layout()
    save_plot(plt, 'horizontal_bar_plot_rating_records.png', PLOT_FOLDER)

def other_plots(df):

    # Bar Chart
    plt.figure(figsize=(12, 6))
    sns.countplot(x='PROPERTY_TYPE', data=df)
    plt.xticks(rotation=45)
    plt.xlabel('Property Type')
    plt.ylabel('Count')
    plt.title('Count of Properties by Property Type')
    plt.tight_layout()
    plt.savefig(os.path.join(PLOT_FOLDER, 'bar_chart_count_prop_by_type.png'))
    plt.close()
    

def print_results(df):
    """Print results and statistics."""
    lodgements_by_local_authority = df['LOCAL_AUTHORITY'].value_counts()
    local_authority = df['LOCAL_AUTHORITY_LABEL'].value_counts()
    max_lodgements_local_authority = local_authority.idxmax()
    sum_lodgements_count = lodgements_by_local_authority.sum()

    print('-----------------------------------')
    numberEPC = f'In the latest data release, there are {sum_lodgements_count} EPC lodgments in \
    {max_lodgements_local_authority}'
    return numberEPC

def output_facts(numberEPC):
    
    file_path = "data/processed_data/EPCfacts.md"

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(numberEPC)
    


def main():
    # Check if location argument is provided
    if len(sys.argv) != 2:
        print("Usage: python script.py <location>")
        sys.exit(1)

    location = sys.argv[1].lower()

    # Read data
    folder_name = [name for name in os.listdir(os.path.join(DATA_FOLDER, RAW_DATA_FOLDER, "all-domestic-certificates")) 
                   if re.match(r'domestic-.*', name, re.IGNORECASE) and location.lower() in name.lower()]

    if not folder_name:
        print(f"No matching folder found for location: {location}")
        sys.exit(1)

    file_path = os.path.join(DATA_FOLDER, RAW_DATA_FOLDER, "all-domestic-certificates", folder_name[0], "certificates.csv")
    df = read_data(file_path)

    # Set seaborn style and palette
    set_seaborn_style_palette()

    # Process data
    process_data(df)

    # Horizontal Bar Plot
    plot_horizontal_bar(df)
    
    # other plots
    other_plots(df)

    # Print results
    numberEPC = print_results(df)
    
    output_facts(numberEPC)

if __name__ == "__main__":
    main()

