
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
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests
from scipy import stats


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
        analysis_menu.add_command(
            label="Basic Stats", command=self.show_basic_stats)
        analysis_menu.add_command(
            label="Show Missing Data", command=self.show_missing_data)
        menu_bar.add_cascade(label="Analysis", menu=analysis_menu)

        # Add "Visualization" menu
        visualize_menu = tk.Menu(menu_bar, tearoff=0)
        visualize_menu.add_command(
            label="Histogram", command=self.plot_histogram)
        visualize_menu.add_command(
            label="Scatter Plot", command=self.plot_scatter)
        visualize_menu.add_command(
            label="Pair Plot", command=self.plot_pairplot)
        menu_bar.add_cascade(label="Visualization", menu=visualize_menu)
        # Mitch's addtion for Investigators
        visualize_menu.add_command(
            label="Investigators Count", command=self.plot_investigators_count)

        # Attach the menu to the root window
        self.root.config(menu=menu_bar)

        # Dropdown to select API
        self.api_label = tk.Label(
            self.root, text="Select API:", font=("Arial", 12))
        self.api_label.pack(pady=10)

        # Dropdown menu to select API
        self.api_var = tk.StringVar(self.root)
        # Default to "2023 Research Payments API"
        self.api_var.set(list(self.api_urls.keys())[0])

        self.api_dropdown = tk.OptionMenu(
            self.root, self.api_var, *self.api_urls.keys())
        self.api_dropdown.pack(pady=10)

        # Button to load data
        self.load_button = tk.Button(self.root, text="Load Data", font=(
            "Arial", 12), command=self.load_api_data)
        self.load_button.pack(pady=20)

        # Button to view column options (MITCH ADDITION)
        self.columns_button = tk.Button(self.root, text="View Columns", font=(
            "Arial", 12), command=self.show_columns)
        self.columns_button.pack(pady=10)

        # Add a label for testing to see if the window is displayed correctly
        test_label = tk.Label(
            self.root, text="Welcome to the Data Analysis Tool!", font=("Arial", 16))
        test_label.pack(pady=20)  # Adding padding for better spacing

        # Add a scrollbar for the Text widget
       # scrollbar = tk.Scrollbar(missing_window, command=missing_text.yview)
        # scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # missing_text.config(yscrollcommand=scrollbar.set)

    def load_api_data(self):
        """Fetch data from the selected API and load it into a DataFrame."""
        selected_api = self.api_var.get()  # Get selected API name from the dropdown
        api_url = self.api_urls[selected_api]  # Get the corresponding URL
        desired_columns = [
            'total_amount_of_payment_usdollars', 'principal_investigator_1_state',
            'form_of_payment_or_transfer_of_value', 'name_of_drug_or_biological_or_device_or_medical_supply_1',
            'product_category_or_therapeutic_area_1',
            'principal_investigator_1_primary_type_1',
            'principal_investigator_1_specialty_1', 'submitting_applicable_manufacturer_or_applicable_gpo_name',
            'principal_investigator_1_profile_id'
        ]

        try:
            limit = 500
            offset = 0
            all_data = []
            total_records = 0

            self.df = pd.DataFrame()

            while total_records < 30000:
                # Make the request with the current offset and limit
                response = requests.get(
                    api_url, params={'limit': limit, 'offset': offset})

                if response.status_code == 200:
                    # Extract the results portion from the API response
                    database = response.json()
                    results = database.get('results', [])

                    if not results:
                        # Exit the loop if no results are returned (we've reached the last page)
                        break

                    # Normalize the results for this page and apply desired columns filtering
                    normalized_data = pd.json_normalize(results)

                    # Check if all the desired columns are in the normalized data
                    missing_columns = [
                        col for col in desired_columns if col not in normalized_data.columns]

                    if missing_columns:
                        # If there are missing columns, show an error message and break
                        missing_columns_str = ', '.join(missing_columns)
                        messagebox.showerror("Missing Columns", f"The following columns are missing: {
                                             missing_columns_str}")
                        return  # Stop execution if columns are missing
                    else:
                        # If no columns are missing, filter the DataFrame to keep only the desired columns
                        normalized_data = normalized_data[desired_columns]

                        # Append this batch of data to the all_data list
                        all_data.append(normalized_data)
                        total_records += len(normalized_data)
                        print(f"Loaded {len(results)} records, total: {
                              len(all_data) * limit} records.")

                    offset += limit

                    # If total records exceed 30,000, break out of the loop
                    if total_records >= 30000:
                        break

                else:
                    messagebox.showerror("Error", f"Failed to load data from {selected_api}: {
                                         response.status_code}. Response: {response.text}")
                    break

            if all_data:
                # Once all data is collected, concatenate and assign to the DataFrame
                self.df = pd.concat(all_data, ignore_index=True)

                # If we have more than 30,000 records, truncate the DataFrame to 30,000 rows
                if len(self.df) > 30000:
                    self.df = self.df.head(30000)

                messagebox.showinfo("Data Loaded", f"Data successfully loaded from {
                                    selected_api} with {len(self.df)} records.")
                # Debugging: see the first 5 rows of the data
                print(self.df.head())
            else:
                messagebox.showwarning(
                    "No Data", "No data was loaded from the API.")

        except requests.exceptions.RequestException as e:
            # Handle specific request errors (e.g., connection issues)
            messagebox.showerror("Error", f"Request failed: {e}")
        except Exception as e:
            # General error handling
            messagebox.showerror("Error", f"Error fetching data from {
                                 selected_api}: {e}")


#################
# #Appends to DF each API pull
#                         # Append this batch of data to the main DataFrame
#                         self.df = pd.concat([self.df, normalized_data], ignore_index=True)

#                         print(f"Loaded {len(results)} records, total: {len(self.df)} records.")

#                     offset += limit
#                 else:
#                     messagebox.showerror("Error", f"Failed to load data from {selected_api}: {response.status_code}. Response: {response.text}")
#                     break

#             if not self.df.empty:
#                 messagebox.showinfo("Data Loaded", f"Data successfully loaded from {selected_api} with {len(self.df)} records.")
#                 print(self.df.head())  # Debugging: see the first 5 rows of the data
#             else:
#                 messagebox.showwarning("No Data", "No data was loaded from the API.")
#         except Exception as e:
#             messagebox.showerror("Error", f"Error fetching data from {selected_api}: {e}")
  #### ####################################
# '''
#             # Fetch data from the selected API without any parameters
#             print(f"Requesting URL: {api_url}")
#             response = requests.get(api_url)

#             if response.status_code == 200:
#                 # Extract the results portion and load it into the DataFrame
#                 database = response.json()
#                 self.df = pd.json_normalize(database['results'])  # Load 'results' into DataFrame
#                 # Limit to desired columns only (check if columns exist)
#                 ####
#                 missing_columns = [col for col in desired_columns if col not in self.df.columns]

#                 if missing_columns:
#                 # If there are missing columns, show an error message
#                     missing_columns_str = ', '.join(missing_columns)
#                     messagebox.showerror("Missing Columns", f"The following columns are missing: {missing_columns_str}")
#                     return  # Stop execution if columns are missing
#                 else:
#                 # If no columns are missing, filter the DataFrame to keep only the desired columns
#                     self.df = self.df[desired_columns]
#                     messagebox.showinfo("Data Loaded", f"Data successfully loaded from {selected_api} with {len(self.df)} records.")
#                     print(self.df.head())  # Debugging: see the first 5 rows of the data


#                 ####
#                 #self.df = self.df[desired_columns] if all(col in self.df.columns for col in desired_columns) else self.df
#                 #messagebox.showinfo("Data Loaded", f"Data successfully loaded from {selected_api} with {len(self.df)} records.")
#                 #print(self.df.head())# Debugging: see the first 5 rows of the data
#                 #print(self.df.columns())

#             else:
#                 messagebox.showerror("Error", f"Failed to load data from {selected_api}: {response.status_code}. Response: {response.text}")
#         except Exception as e:
#             messagebox.showerror("Error", f"Error fetching data from {selected_api}: {e}")
# '''
#######
# adding function to clean based on first removing with NaN in total amounts column, then eliminiate outliers
#######


    def clean_data(self):
        """Clean data by removing rows with NaN in the total_amount_of_payment_usdollars column."""
        if self.df is not None:
            # Remove rows with NaN in 'total_amount_of_payment_usdollars'
            self.df = self.df.dropna(
                subset=['total_amount_of_payment_usdollars'])

            # Remove rows where 'total_amount_of_payment_usdollars' is 0
            self.df = self.df[self.df['total_amount_of_payment_usdollars'] != 0]
            # Remove rows where 'total_amount_of_payment_usdollars' is above 1,000,000
            self.df = self.df[self.df['total_amount_of_payment_usdollars'] <= 1000000]

            # Remove outliers: Keep values between 1st and 99th percentiles
            lower_percentile = self.df['total_amount_of_payment_usdollars'].quantile(
                0.1)
            upper_percentile = self.df['total_amount_of_payment_usdollars'].quantile(
                0.90)

            self.df = self.df[(self.df['total_amount_of_payment_usdollars'] >= lower_percentile) &
                              (self.df['total_amount_of_payment_usdollars'] <= upper_percentile)]

            # Clean the 'principal_investigator_1_specialty_1' column by removing the first part of phrases containing 'Allopathic & Osteopathic Physician'

            if 'principal_investigator_1_specialty_1' in self.df.columns:
                self.df['principal_investigator_1_specialty_1'] = self.df['principal_investigator_1_specialty_1'].apply(
                    lambda x: str(x).split(
                        'Allopathic & Osteopathic Physician', 1)[-1].strip()
                    if isinstance(x, str) and 'Allopathic & Osteopathic Physician' in x else x
                )

            messagebox.showinfo(
                "Data Cleaned", "Rows with NaN values and outliers have been removed.")
        else:
            messagebox.showwarning("No Data", "Please load data first!")

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
        """Generate a histogram of a chosen column with adjustable bin width and maximum X-axis, with statistics displayed."""
        if self.df is not None:
            # Create a new Toplevel window for column selection, bin width, and max X-axis
            histogram_window = tk.Toplevel(self.root)
            histogram_window.title("Select Column and Settings for Histogram")

            # Add a label for instruction
            instruction_label = tk.Label(
                histogram_window, text="Select a column for the histogram:", font=("Arial", 12))
            instruction_label.pack(pady=10)

            # Dropdown for column selection
            column_var = tk.StringVar(histogram_window)
            column_var.set(self.df.columns[0])  # Default to the first column
            column_dropdown = tk.OptionMenu(
                histogram_window, column_var, *self.df.columns)
            column_dropdown.pack(pady=10)

            # Entry for bin width
            bin_width_label = tk.Label(
                histogram_window, text="Enter bin width (leave blank for auto):", font=("Arial", 12))
            bin_width_label.pack(pady=10)

            bin_width_entry = tk.Entry(histogram_window)
            bin_width_entry.pack(pady=10)

            # Entry for maximum X-axis value
            max_x_label = tk.Label(
                histogram_window, text="Enter maximum X-axis value (leave blank for auto):", font=("Arial", 12))
            max_x_label.pack(pady=10)

            max_x_entry = tk.Entry(histogram_window)
            max_x_entry.pack(pady=10)

            # Button to generate the histogram
            def generate_histogram():
                selected_column = column_var.get()
                # Drop NaN values for clean plotting
                data = self.df[selected_column].dropna()

                try:
                    # Attempt to convert data to numeric, coercing errors
                    data = pd.to_numeric(data.str.replace(
                        '[^\d.]', '', regex=True), errors='coerce').dropna()
                except AttributeError:
                    # If .str operations fail (e.g., already numeric), continue
                    data = pd.to_numeric(data, errors='coerce').dropna()

                if data.empty:
                    messagebox.showwarning("No Data", f"No valid numeric data in column '{
                                           selected_column}'.")
                    return

                # Get the bin width from user input
                bin_width = bin_width_entry.get()
                try:
                    bin_width = float(bin_width) if bin_width else None
                except ValueError:
                    messagebox.showerror(
                        "Invalid Input", "Please enter a valid numeric value for bin width.")
                    return

                # Determine the number of bins
                if bin_width and bin_width > 0:
                    range_min, range_max = data.min(), data.max()
                    num_bins = int((range_max - range_min) / bin_width)
                else:
                    # Auto-determine bins using Freedman-Diaconis rule
                    q75, q25 = data.quantile([0.75, 0.25])
                    iqr = q75 - q25
                    bin_width = 2 * iqr / len(data) ** (1 / 3)
                    num_bins = max(
                        1, int((data.max() - data.min()) / bin_width))

                # Get the maximum X-axis value from user input
                max_x = max_x_entry.get()
                try:
                    max_x = float(max_x) if max_x else None
                except ValueError:
                    messagebox.showerror(
                        "Invalid Input", "Please enter a valid numeric value for maximum X-axis.")
                    return

                # Calculate statistics
                mean_value = data.mean()
                median_value = data.median()
                mode_value = data.mode()[0] if not data.mode().empty else 'N/A'
                range_value = data.max() - data.min()

                # Plot the histogram
                plt.figure(figsize=(10, 6))
                sns.histplot(data, kde=True, bins=num_bins,
                             color='blue', edgecolor='black')
                plt.title(f"Histogram of {selected_column}", fontsize=16)
                plt.xlabel(selected_column, fontsize=14)
                plt.ylabel("Frequency", fontsize=14)
                # Add gridlines for better readability
                plt.grid(True, linestyle='--', alpha=0.7)

                # Set the X-axis limits (always start at 0, use user-defined max if provided)
                plt.xlim(left=0, right=max_x if max_x else data.max())

                # Display statistics as an annotation on the plot
                stats_text = (f"Mean: {mean_value:.2f}\n"
                              f"Median: {median_value:.2f}\n"
                              f"Mode: {mode_value}\n"
                              f"Range: {range_value:.2f}")
                plt.gca().text(0.95, 0.95, stats_text, transform=plt.gca().transAxes,
                               fontsize=12, verticalalignment='top', horizontalalignment='right',
                               bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=1'))

                plt.tight_layout()  # Adjust layout to fit elements nicely
                plt.show()

            generate_button = tk.Button(
                histogram_window, text="Generate Histogram", command=generate_histogram, font=("Arial", 12))
            generate_button.pack(pady=10)

            # Close button
            close_button = tk.Button(
                histogram_window, text="Close", command=histogram_window.destroy, font=("Arial", 12))
            close_button.pack(pady=10)

        else:
            messagebox.showwarning("No Data", "Please load data first!")

    def plot_investigators_count(self):
        """Generate a count of unique investigators grouped by different variables."""
        if self.df is not None:
            # Create a new Toplevel window for variable selection
            count_window = tk.Toplevel(self.root)
            count_window.title(
                "Select Variable and Range for Investigators Count")

            # Add a label for instruction
            instruction_label = tk.Label(
                count_window, text="Select a variable to group by:", font=("Arial", 12))
            instruction_label.pack(pady=10)

            # Dropdown for variable selection (all columns in the dataframe)
            variable_var = tk.StringVar(count_window)
            variable_var.set(self.df.columns[0])  # Default to the first column
            variable_dropdown = tk.OptionMenu(
                count_window, variable_var, *self.df.columns)
            variable_dropdown.pack(pady=10)

            # Checkbox to toggle filtering out missing data
            filter_missing_var = tk.BooleanVar()
            filter_missing_checkbox = tk.Checkbutton(
                count_window, text="Filter out missing data", variable=filter_missing_var)
            filter_missing_checkbox.pack(pady=10)

            # Add entry fields for minimum and maximum counts
            min_label = tk.Label(
                count_window, text="Minimum Count:", font=("Arial", 12))
            min_label.pack(pady=5)
            min_entry = tk.Entry(count_window)
            min_entry.pack(pady=5)

            max_label = tk.Label(
                count_window, text="Maximum Count:", font=("Arial", 12))
            max_label.pack(pady=5)
            max_entry = tk.Entry(count_window)
            max_entry.pack(pady=5)

            # Button to generate the count plot
            def generate_count_plot():
                selected_variable = variable_var.get()
                if selected_variable not in self.df.columns:
                    messagebox.showwarning("Invalid Column", f"{
                                           selected_variable} is not a valid column.")
                    return

                investigator_column = 'principal_investigator_1_profile_id'
                if investigator_column not in self.df.columns:
                    messagebox.showwarning("Missing Data", f"Column for investigators not found: {
                                           investigator_column}.")
                    return

                # Create a filtered DataFrame
                filtered_df = self.df.copy()
                if filter_missing_var.get():
                    filtered_df = filtered_df.dropna(
                        subset=[selected_variable])

                # Group by the selected variable and count unique investigators
                investigator_counts = filtered_df.groupby(
                    selected_variable)[investigator_column].nunique().reset_index()
                investigator_counts.columns = [
                    selected_variable, 'Investigator Count']

                # Apply range filtering based on user input
                try:
                    min_count = int(
                        min_entry.get()) if min_entry.get() else None
                    max_count = int(
                        max_entry.get()) if max_entry.get() else None

                    if min_count is not None:
                        investigator_counts = investigator_counts[
                            investigator_counts['Investigator Count'] >= min_count]
                    if max_count is not None:
                        investigator_counts = investigator_counts[
                            investigator_counts['Investigator Count'] <= max_count]
                except ValueError:
                    messagebox.showerror(
                        "Invalid Input", "Please enter valid numbers for minimum and maximum counts.")
                    return

                # Plot the result using seaborn barplot
                plt.figure(figsize=(10, 6))
                sns.barplot(
                    x=investigator_counts[selected_variable],
                    y=investigator_counts['Investigator Count'],
                    palette="viridis"
                )
                plt.title(f"Number of Investigators by {
                          selected_variable}", fontsize=16)
                plt.xlabel(selected_variable, fontsize=14)
                plt.ylabel("Investigator Count", fontsize=14)
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                plt.show()

            # Generate button
            generate_button = tk.Button(
                count_window, text="Generate Investigator Count", command=generate_count_plot, font=("Arial", 12))
            generate_button.pack(pady=10)

            # Close button
            close_button = tk.Button(
                count_window, text="Close", command=count_window.destroy, font=("Arial", 12))
            close_button.pack(pady=10)

        else:
            messagebox.showwarning("No Data", "Please load data first!")


# MITCH END

#    def plot_scatter(self):
#        """Generate a scatter plot of two selected columns."""
#        if self.df is not None:
#            columns = self.get_columns_for_scatter()
#            if columns:
        # Scatter plot using Seaborn
#                sns.scatterplot(x=self.df[columns[0]], y=self.df[columns[1]])
#                plt.title(f"Scatter Plot: {columns[0]} vs {columns[1]}")
#                plt.xlabel(columns[0])
#                plt.ylabel(columns[1])
#                plt.show()
#        else:
#            messagebox.showwarning("No Data", "Please load data first!")


    def plot_scatter(self):
        """Generate a scatter plot of two selected columns and display it in the UI."""
        if self.df is not None:
            columns = self.get_columns_for_scatter()  # Get user-selected columns
            if columns:
                column_x, column_y = columns

                # Create a figure for the scatter plot
                plt.figure(figsize=(6, 6))
                sns.scatterplot(x=self.df[column_x], y=self.df[column_y])
                plt.title(f"Scatter Plot: {column_x} vs {column_y}")
                plt.xlabel(column_x)
                plt.ylabel(column_y)

                # Create a Toplevel window to display the plot
                plot_window = tk.Toplevel(self.root)
                plot_window.title(f"Scatter Plot: {column_x} vs {column_y}")

                # Create a Frame to hold the plot
                plot_frame = tk.Frame(plot_window)
                plot_frame.pack(fill=tk.BOTH, expand=True)

                # Create the canvas to embed the plot
                # Pass the matplotlib figure to the canvas
                canvas = FigureCanvasTkAgg(plt.gcf(), master=plot_frame)
                canvas.draw()

                # Pack the canvas into the plot frame
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

                # Optional: Add a close button to close the plot window
                close_button = tk.Button(
                    plot_window, text="Close", command=plot_window.destroy, font=("Arial", 12))
                close_button.pack(pady=10)

            else:
                messagebox.showwarning(
                    "Invalid Input", "Please select valid column names.")
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
            column = simpledialog.askstring(
                "Input", "Enter column name for the histogram:")
            if column and column in self.df.columns:
                return column
            else:
                messagebox.showwarning(
                    "Invalid Input", "Please enter a valid column name.")
                return None
        return None

    def get_columns_for_scatter(self):
        """Prompt user to select two columns for the scatter plot."""
        if self.df is not None:
            scatter_window = tk.Toplevel(self.root)
            scatter_window.title("Select Columns for Scatter Plot")

            # Dropdowns for column selection
            column_x_var = tk.StringVar(scatter_window)
            column_y_var = tk.StringVar(scatter_window)

            column_x_var.set(self.df.columns[0])  # Default to first column
            column_y_var.set(self.df.columns[1])  # Default to second column

            column_x_dropdown = tk.OptionMenu(
                scatter_window, column_x_var, *self.df.columns)
            column_y_dropdown = tk.OptionMenu(
                scatter_window, column_y_var, *self.df.columns)

            column_x_dropdown.pack(pady=10)
            column_y_dropdown.pack(pady=10)

            def generate_scatter_plot():
                selected_column_x = column_x_var.get()
                selected_column_y = column_y_var.get()

                if selected_column_x in self.df.columns and selected_column_y in self.df.columns:
                    sns.scatterplot(
                        x=self.df[selected_column_x], y=self.df[selected_column_y])
                    plt.title(f"Scatter Plot: {selected_column_x} vs {
                              selected_column_y}")
                    plt.xlabel(selected_column_x)
                    plt.ylabel(selected_column_y)
                    plt.show()

            generate_button = tk.Button(
                scatter_window, text="Generate Scatter Plot", command=generate_scatter_plot)
            generate_button.pack(pady=10)

            scatter_window.mainloop()

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
            columns_label = tk.Label(
                columns_window, text="Available Columns:", font=("Arial", 12))
            columns_label.pack(pady=10)

            # Add a listbox to display the column names
            columns_listbox = tk.Listbox(columns_window, height=15, width=50)
            for column in self.df.columns:
                columns_listbox.insert(tk.END, column)
            columns_listbox.pack(pady=10)

            # Add a Close button to exit the window
            close_button = tk.Button(
                columns_window, text="Close", command=columns_window.destroy, font=("Arial", 12))
            close_button.pack(pady=10)
        else:
            messagebox.showwarning("No Data", "Please load data first!")


if __name__ == "__main__":
    root = tk.Tk()
    app = DataAnalysisApp(root)
    root.mainloop()
