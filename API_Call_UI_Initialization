import tkinter as tk
from tkinter import messagebox, simpledialog
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import requests

class DataAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Analysis and Visualization Tool")
        self.df = None  # Placeholder for the DataFrame

        # Set window size
        self.root.geometry("800x600")

        # Predefined API for "2023 Research Payments"
        self.api_urls = {
            "2023 Research Payments API": "https://openpaymentsdata.cms.gov/api/1/datastore/query/60f290ea-f990-5ef0-845f-68b3a91f45a1"
        }

        # Create and pack widgets
        self.create_widgets()

    def create_widgets(self):
        # Create a menu bar
        menu_bar = tk.Menu(self.root)

        # Add "File" menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Add "Analysis" menu
        analysis_menu = tk.Menu(menu_bar, tearoff=0)
        analysis_menu.add_command(label="Basic Stats", command=self.show_basic_stats)
        analysis_menu.add_command(label="Show Missing Data", command=self.show_missing_data)
        menu_bar.add_cascade(label="Analysis", menu=analysis_menu)

        # Add "Visualization" menu
        visualize_menu = tk.Menu(menu_bar, tearoff=0)
        visualize_menu.add_command(label="Histogram", command=self.plot_histogram)
        visualize_menu.add_command(label="Scatter Plot", command=self.plot_scatter)
        visualize_menu.add_command(label="Pair Plot", command=self.plot_pairplot)
        menu_bar.add_cascade(label="Visualization", menu=visualize_menu)

        # Attach the menu to the root window
        self.root.config(menu=menu_bar)

        # Dropdown to select API
        self.api_label = tk.Label(self.root, text="Select API:", font=("Arial", 12))
        self.api_label.pack(pady=10)

        # Dropdown menu to select API
        self.api_var = tk.StringVar(self.root)
        self.api_var.set(list(self.api_urls.keys())[0])  # Default to "2023 Research Payments API"

        self.api_dropdown = tk.OptionMenu(self.root, self.api_var, *self.api_urls.keys())
        self.api_dropdown.pack(pady=10)

        # Button to load data
        self.load_button = tk.Button(self.root, text="Load Data", font=("Arial", 12), command=self.load_api_data)
        self.load_button.pack(pady=20)

        # Add a label for testing to see if the window is displayed correctly
        test_label = tk.Label(self.root, text="Welcome to the Data Analysis Tool!", font=("Arial", 16))
        test_label.pack(pady=20)  # Adding padding for better spacing

    def load_api_data(self):
        """Fetch data from the selected API and load it into a DataFrame."""
        selected_api = self.api_var.get()  # Get selected API name from the dropdown
        api_url = self.api_urls[selected_api]  # Get the corresponding URL

        try:
            # Fetch data from the selected API without any parameters
            print(f"Requesting URL: {api_url}")
            response = requests.get(api_url)
            
            if response.status_code == 200:
                # Extract the results portion and load it into the DataFrame
                database = response.json()
                self.df = pd.json_normalize(database['results'])  # Load 'results' into DataFrame
                messagebox.showinfo("Data Loaded", f"Data successfully loaded from {selected_api} with {len(self.df)} records.")
                print(self.df.head())  # Debugging: see the first 5 rows of the data
            else:
                messagebox.showerror("Error", f"Failed to load data from {selected_api}: {response.status_code}. Response: {response.text}")
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching data from {selected_api}: {e}")

    def show_basic_stats(self):
        """Display basic statistics of the data."""
        if self.df is not None:
            stats = self.df.describe()
            print(stats)
            messagebox.showinfo("Basic Statistics", str(stats))
        else:
            messagebox.showwarning("No Data", "Please load data first!")

    def show_missing_data(self):
        """Show the count of missing data in the DataFrame."""
        if self.df is not None:
            missing_data = self.df.isnull().sum()
            print(missing_data)
            messagebox.showinfo("Missing Data", str(missing_data))
        else:
            messagebox.showwarning("No Data", "Please load data first!")

    def plot_histogram(self):
        """Generate a histogram of a chosen column."""
        if self.df is not None:
            column = self.get_column_for_plot()
            if column:
                # Create the histogram using Seaborn
                sns.histplot(self.df[column], kde=True, bins=20)
                plt.title(f"Histogram of {column}")
                plt.xlabel(column)
                plt.ylabel("Frequency")
                plt.show()
        else:
            messagebox.showwarning("No Data", "Please load data first!")

    def plot_scatter(self):
        """Generate a scatter plot of two selected columns."""
        if self.df is not None:
            columns = self.get_columns_for_scatter()
            if columns:
                # Scatter plot using Seaborn
                sns.scatterplot(x=self.df[columns[0]], y=self.df[columns[1]])
                plt.title(f"Scatter Plot: {columns[0]} vs {columns[1]}")
                plt.xlabel(columns[0])
                plt.ylabel(columns[1])
                plt.show()
        else:
            messagebox.showwarning("No Data", "Please load data first!")

    def plot_pairplot(self):
        """Generate a pairplot of the DataFrame."""
        if self.df is not None:
            # Pair plot using Seaborn (pairwise relationships between numerical columns)
            sns.pairplot(self.df)
            plt.show()
        else:
            messagebox.showwarning("No Data", "Please load data first!")

    def get_column_for_plot(self):
        """Prompt user to select a column for the plot."""
        if self.df is not None:
            column = simpledialog.askstring("Input", "Enter column name for the histogram:")
            if column and column in self.df.columns:
                return column
            else:
                messagebox.showwarning("Invalid Input", "Please enter a valid column name.")
                return None
        return None

    def get_columns_for_scatter(self):
        """Prompt user to select two columns for the scatter plot."""
        if self.df is not None:
            column_x = simpledialog.askstring("Input", "Enter X column for scatter plot:")
            column_y = simpledialog.askstring("Input", "Enter Y column for scatter plot:")
            if column_x in self.df.columns and column_y in self.df.columns:
                return column_x, column_y
            else:
                messagebox.showwarning("Invalid Input", "Please enter valid column names.")
                return None
        return None


if __name__ == "__main__":
    root = tk.Tk()
    app = DataAnalysisApp(root)
    root.mainloop()

