#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 22:55:53 2024

@author: mitchelllipke
"""

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
        #Mitch's addtion for Investigators
        visualize_menu.add_command(label="Investigators Count", command=self.plot_investigators_count)

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

        # Button to view column options (MITCH ADDITION)
        self.columns_button = tk.Button(self.root, text="View Columns", font=("Arial", 12), command=self.show_columns)
        self.columns_button.pack(pady=10)

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

    # def plot_histogram(self):
    #     """Generate a histogram of a chosen column."""
    #     if self.df is not None:
    #         column = self.get_column_for_plot()
    #         if column:
    #             # Create the histogram using Seaborn
    #             sns.histplot(self.df[column], kde=True, bins=20)
    #             plt.title(f"Histogram of {column}")
    #             plt.xlabel(column)
    #             plt.ylabel("Frequency")
    #             plt.show()
    #     else:
    #         messagebox.showwarning("No Data", "Please load data first!")


#MITCH CODE BEGIN#
    # def plot_histogram(self):
    #     """Generate a histogram of a chosen column using a dropdown for selection."""
    #     if self.df is not None:
    #         # Create a new Toplevel window for column selection
    #         histogram_window = tk.Toplevel(self.root)
    #         histogram_window.title("Select Column for Histogram")
    
    #         # Add a label for instruction
    #         instruction_label = tk.Label(histogram_window, text="Select a column for the histogram:", font=("Arial", 12))
    #         instruction_label.pack(pady=10)
    
    #         # Dropdown for column selection
    #         column_var = tk.StringVar(histogram_window)
    #         column_var.set(self.df.columns[0])  # Default to the first column
    #         column_dropdown = tk.OptionMenu(histogram_window, column_var, *self.df.columns)
    #         column_dropdown.pack(pady=10)
    
    #         # Button to generate the histogram
    #         # def generate_histogram():
    #         #     selected_column = column_var.get()
    #         #     sns.histplot(self.df[selected_column], kde=True, bins=20)
    #         #     plt.title(f"Histogram of {selected_column}")
    #         #     plt.xlabel(selected_column)
    #         #     plt.ylabel("Frequency")
    #         #     plt.show()
 
    #         def generate_histogram():
    #             selected_column = column_var.get()
    #             data = self.df[selected_column].dropna()  # Drop NaN values for clean plotting
            
    #             if data.empty:
    #                 messagebox.showwarning("No Data", f"No valid data in column '{selected_column}'.")
    #                 return
            
    #             # Calculate optimal bins using Freedman-Diaconis rule
    #             q75, q25 = data.quantile([0.75, 0.25])
    #             iqr = q75 - q25  # Interquartile range
    #             bin_width = 2 * iqr / len(data) ** (1 / 3)  # Freedman-Diaconis rule
    #             num_bins = max(1, int((data.max() - data.min()) / bin_width))  # Ensure at least 1 bin
            
    #             # Plot the histogram
    #             plt.figure(figsize=(10, 6))
    #             sns.histplot(data, kde=True, bins=num_bins, color='blue', edgecolor='black')
    #             plt.title(f"Histogram of {selected_column}", fontsize=16)
    #             plt.xlabel(selected_column, fontsize=14)
    #             plt.ylabel("Frequency", fontsize=14)
    #             plt.grid(True, linestyle='--', alpha=0.7)  # Add gridlines for better readability
    #             plt.tight_layout()  # Adjust layout to fit elements nicely
    #             plt.show()
   
 
    #         generate_button = tk.Button(histogram_window, text="Generate Histogram", command=generate_histogram, font=("Arial", 12))
    #         generate_button.pack(pady=10)
    
    #         # Close button
    #         close_button = tk.Button(histogram_window, text="Close", command=histogram_window.destroy, font=("Arial", 12))
    #         close_button.pack(pady=10)
            

    
    #     else:
    #         messagebox.showwarning("No Data", "Please load data first!")

    def plot_histogram(self):
        """Generate a histogram of a chosen column using a dropdown for selection."""
        if self.df is not None:
            # Create a new Toplevel window for column selection
            histogram_window = tk.Toplevel(self.root)
            histogram_window.title("Select Column for Histogram")
    
            # Add a label for instruction
            instruction_label = tk.Label(histogram_window, text="Select a column for the histogram:", font=("Arial", 12))
            instruction_label.pack(pady=10)
    
            # Dropdown for column selection
            column_var = tk.StringVar(histogram_window)
            column_var.set(self.df.columns[0])  # Default to the first column
            column_dropdown = tk.OptionMenu(histogram_window, column_var, *self.df.columns)
            column_dropdown.pack(pady=10)
    
            # Button to generate the histogram
            def generate_histogram():
                selected_column = column_var.get()
                data = self.df[selected_column].dropna()  # Drop NaN values for clean plotting
            
                try:
                    # Attempt to convert data to numeric, coercing errors
                    data = pd.to_numeric(data.str.replace('[^\d.]', '', regex=True), errors='coerce').dropna()
                except AttributeError:
                    # If .str operations fail (e.g., already numeric), continue
                    data = pd.to_numeric(data, errors='coerce').dropna()
            
                if data.empty:
                    messagebox.showwarning("No Data", f"No valid numeric data in column '{selected_column}'.")
                    return
            
                # Calculate optimal bins using Freedman-Diaconis rule
                q75, q25 = data.quantile([0.75, 0.25])
                iqr = q75 - q25  # Interquartile range
                bin_width = 2 * iqr / len(data) ** (1 / 3)  # Freedman-Diaconis rule
                num_bins = max(1, int((data.max() - data.min()) / bin_width))  # Ensure at least 1 bin
            
                # Plot the histogram
                plt.figure(figsize=(10, 6))
                sns.histplot(data, kde=True, bins=num_bins, color='blue', edgecolor='black')
                plt.title(f"Histogram of {selected_column}", fontsize=16)
                plt.xlabel(selected_column, fontsize=14)
                plt.ylabel("Frequency", fontsize=14)
                plt.grid(True, linestyle='--', alpha=0.7)  # Add gridlines for better readability
                plt.tight_layout()  # Adjust layout to fit elements nicely
                plt.show()


            generate_button = tk.Button(histogram_window, text="Generate Histogram", command=generate_histogram, font=("Arial", 12))
            generate_button.pack(pady=10)
    
            # Close button
            close_button = tk.Button(histogram_window, text="Close", command=histogram_window.destroy, font=("Arial", 12))
            close_button.pack(pady=10)
    
        else:
            messagebox.showwarning("No Data", "Please load data first!")
    
    # def plot_investigators_count(self):
    #     """Generate a count of unique investigators grouped by different variables."""
    #     if self.df is not None:
    #         # Check column names and print for debugging
    #         print(self.df.columns)  # Debugging line to check the actual columns in your dataframe
            
    #         # Create a new Toplevel window for variable selection
    #         count_window = tk.Toplevel(self.root)
    #         count_window.title("Select Variable for Investigators Count")
            
    #         # Add a label for instruction
    #         instruction_label = tk.Label(count_window, text="Select a variable to group by:", font=("Arial", 12))
    #         instruction_label.pack(pady=10)
            
    #         # Dropdown for variable selection (all columns in the dataframe)
    #         variable_var = tk.StringVar(count_window)
    #         variable_var.set(self.df.columns[0])  # Default to the first column
    #         variable_dropdown = tk.OptionMenu(count_window, variable_var, *self.df.columns)
    #         variable_dropdown.pack(pady=10)
            
    #         # # Button to generate the count plot

    #         def generate_count_plot():
    #             selected_variable = variable_var.get()
    #             if selected_variable not in self.df.columns:
    #                 messagebox.showwarning("Invalid Column", f"{selected_variable} is not a valid column.")
    #                 return
                
    #             # Clean column names for uniform access (strip spaces and lower case)
    #             self.df.columns = self.df.columns.str.strip().str.lower()
    
    #             # Check again for the column names
    #             print(self.df.columns)  # Debugging line to check cleaned column names
                
    #             # If the column name for investigators is not correct, try the cleaned version:
    #             investigator_column = 'principal_investigator_1_profile_id'  # Assuming the column is lowercase
    #             if investigator_column not in self.df.columns:
    #                 messagebox.showwarning("Missing Data", f"Column for investigators not found: {investigator_column}.")
    #                 return
                
    #             # Group by the selected variable and count unique investigators
    #             investigator_counts = self.df.groupby(selected_variable)[investigator_column].nunique().reset_index()
    #             investigator_counts.columns = [selected_variable, 'Investigator Count']
                
    #             # Plot the result using seaborn barplot
    #             plt.figure(figsize=(10, 6))
    #             sns.barplot(x=investigator_counts[selected_variable], y=investigator_counts['Investigator Count'], palette="viridis")
    #             plt.title(f"Number of Investigators by {selected_variable}", fontsize=16)
    #             plt.xlabel(selected_variable, fontsize=14)
    #             plt.ylabel("Investigator Count", fontsize=14)
    #             plt.xticks(rotation=45, ha='right')  # Rotate labels if needed
    #             plt.tight_layout()
    #             plt.show()
            
    #         # Generate button
    #         generate_button = tk.Button(count_window, text="Generate Investigator Count", command=generate_count_plot, font=("Arial", 12))
    #         generate_button.pack(pady=10)
            
    #         # Close button
    #         close_button = tk.Button(count_window, text="Close", command=count_window.destroy, font=("Arial", 12))
    #         close_button.pack(pady=10)
        
    #     else:
    #         messagebox.showwarning("No Data", "Please load data first!")
    def plot_investigators_count(self):
        """Generate a count of unique investigators grouped by different variables."""
        if self.df is not None:
            # Check column names and print for debugging
            print(self.df.columns)  # Debugging line to check the actual columns in your dataframe
    
            # Create a new Toplevel window for variable selection
            count_window = tk.Toplevel(self.root)
            count_window.title("Select Variable for Investigators Count")
    
            # Add a label for instruction
            instruction_label = tk.Label(count_window, text="Select a variable to group by:", font=("Arial", 12))
            instruction_label.pack(pady=10)
    
            # Dropdown for variable selection (all columns in the dataframe)
            variable_var = tk.StringVar(count_window)
            variable_var.set(self.df.columns[0])  # Default to the first column
            variable_dropdown = tk.OptionMenu(count_window, variable_var, *self.df.columns)
            variable_dropdown.pack(pady=10)
    
            # Checkbox to toggle filtering out missing data
            filter_missing_var = tk.BooleanVar()
            filter_missing_checkbox = tk.Checkbutton(count_window, text="Filter out missing data", variable=filter_missing_var)
            filter_missing_checkbox.pack(pady=10)
    
            # Button to generate the count plot
            def generate_count_plot():
                selected_variable = variable_var.get()
                if selected_variable not in self.df.columns:
                    messagebox.showwarning("Invalid Column", f"{selected_variable} is not a valid column.")
                    return
    
                # Clean column names for uniform access (strip spaces and lower case)
                self.df.columns = self.df.columns.str.strip().str.lower()
    
                # Check again for the column names
                print(self.df.columns)  # Debugging line to check cleaned column names
    
                # If the column name for investigators is not correct, try the cleaned version:
                investigator_column = 'principal_investigator_1_profile_id'  # Assuming the column is lowercase
                if investigator_column not in self.df.columns:
                    messagebox.showwarning("Missing Data", f"Column for investigators not found: {investigator_column}.")
                    return
    
                # Create a copy of the DataFrame to avoid modifying the original
                filtered_df = self.df.copy()
    
                # Debugging: Print the number of rows before filtering
                print(f"Rows before filtering: {len(filtered_df)}")
    
                # Print the number of missing values for the selected variable
                missing_values = filtered_df[selected_variable].isnull().sum()
                print(f"Missing values in {selected_variable}: {missing_values}")
    
                # If the checkbox is checked, filter out rows where the selected variable is missing
                if filter_missing_var.get():
                    filtered_df = filtered_df.dropna(subset=[selected_variable])
                    # Debugging: Print the number of rows after filtering
                    print(f"Rows after filtering: {len(filtered_df)}")
    
                # Group by the selected variable and count unique investigators
                investigator_counts = filtered_df.groupby(selected_variable)[investigator_column].nunique().reset_index()
                investigator_counts.columns = [selected_variable, 'Investigator Count']
    
                # Plot the result using seaborn barplot
                plt.figure(figsize=(10, 6))
                sns.barplot(x=investigator_counts[selected_variable], y=investigator_counts['Investigator Count'], palette="viridis")
                plt.title(f"Number of Investigators by {selected_variable}", fontsize=16)
                plt.xlabel(selected_variable, fontsize=14)
                plt.ylabel("Investigator Count", fontsize=14)
                plt.xticks(rotation=45, ha='right')  # Rotate labels if needed
                plt.tight_layout()
                plt.show()
    
            # Generate button
            generate_button = tk.Button(count_window, text="Generate Investigator Count", command=generate_count_plot, font=("Arial", 12))
            generate_button.pack(pady=10)
    
            # Close button
            close_button = tk.Button(count_window, text="Close", command=count_window.destroy, font=("Arial", 12))
            close_button.pack(pady=10)
    
        else:
            messagebox.showwarning("No Data", "Please load data first!")



### MITCH END    

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
    
    #### MITCH ADDITION ####
    # def show_columns(self):
    #     """Display the list of column names in the DataFrame."""
    #     if self.df is not None:
    #         columns = self.df.columns.tolist()  # Get the list of column names
    #         messagebox.showinfo("Column Options", f"Available Columns:\n{', '.join(columns)}")
    #     else:
    #         messagebox.showwarning("No Data", "Please load data first!")
    def show_columns(self):
        """Display the list of column names in a new window."""
        if self.df is not None:
            # Create a new Toplevel window
            columns_window = tk.Toplevel(self.root)
            columns_window.title("Column Options")
    
            # Add a label for column names
            columns_label = tk.Label(columns_window, text="Available Columns:", font=("Arial", 12))
            columns_label.pack(pady=10)
    
            # Add a listbox to display the column names
            columns_listbox = tk.Listbox(columns_window, height=15, width=50)
            for column in self.df.columns:
                columns_listbox.insert(tk.END, column)
            columns_listbox.pack(pady=10)
    
            # Add a Close button to exit the window
            close_button = tk.Button(columns_window, text="Close", command=columns_window.destroy, font=("Arial", 12))
            close_button.pack(pady=10)
        else:
            messagebox.showwarning("No Data", "Please load data first!")



if __name__ == "__main__":
    root = tk.Tk()
    app = DataAnalysisApp(root)
    root.mainloop()
