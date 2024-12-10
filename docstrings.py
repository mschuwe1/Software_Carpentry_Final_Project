
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

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
        analysis_menu.add_command(
            label="Search Principal Investigator", command=self.search_by_pi)

        # Add "Visualization" menu
        visualize_menu = tk.Menu(menu_bar, tearoff=0)
        visualize_menu.add_command(
            label="Histogram", command=self.plot_histogram)
        menu_bar.add_cascade(label="Visualization", menu=visualize_menu)
        # Mitch's addtion for Investigators lookup
        visualize_menu.add_command(
            label="Investigators Count", command=self.plot_investigators_count)

        # Saved for potential future use of Scatter and Pair Plots
        # visualize_menu.add_command(
        #     label="Scatter Plot", command=self.plot_scatter)
        # visualize_menu.add_command(
        #     label="Pair Plot", command=self.plot_pairplot)

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
        """Fetched data from the selected API and loads it into a DataFrame.
        The CMS API gives us a json with 4 dictonary objects. We only need to keep the one labeled 'results'.
        Uses the json_normalize function to parse the results into a pandas dataframe. 
        Also limits the columns it pulls in from the results in order to speed up the processing time. 
        If a column is not found, raises an error.
        We also limit to the first 30,000 records to speed processing. Could be increased in future iteratons. 
        """
        selected_api = self.api_var.get()  # Get selected API name from the dropdown
        api_url = self.api_urls[selected_api]  # Get the corresponding URL
        desired_columns = [
            'total_amount_of_payment_usdollars', 'principal_investigator_1_state',
            'form_of_payment_or_transfer_of_value', 'name_of_drug_or_biological_or_device_or_medical_supply_1',
            'product_category_or_therapeutic_area_1',
            'principal_investigator_1_primary_type_1',
            'principal_investigator_1_specialty_1', 'submitting_applicable_manufacturer_or_applicable_gpo_name',
            'principal_investigator_1_profile_id', 'principal_investigator_1_first_name', 'principal_investigator_1_last_name',
            'clinicaltrials_gov_identifier'
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
                        # Exit the loop if no results are returned
                        break

                    # Normalize the results for this page and apply columns filtering
                    normalized_data = pd.json_normalize(results)

                    # Check if all the desired columns are in the normalized data
                    missing_columns = [
                        col for col in desired_columns if col not in normalized_data.columns]

                    if missing_columns:
                        # If there are missing columns, show an error message and break
                        missing_columns_str = ', '.join(missing_columns)
                        messagebox.showerror("Missing Columns", f"The following columns are missing: {
                                             missing_columns_str}")
                        return  # Stop if columns are missing
                    else:
                        # If no columns are missing, filter the DataFrame to keep only the desired columns
                        normalized_data = normalized_data[desired_columns]

                        # Append this round of the resluts data to the all_data list
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
                # Used while we were debugging: see the first 5 rows of the data
                # print(self.df.head())
                
                self.clean_data()
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


#######

#######
# '''
# Here we define the function for cleaning the data once its compiled into the pandas dataframe. 
# Ensure the USD payments are numbers, then remove rows with blank, 0 or more than 1,000,000
# Also we remove top and bottom 5th percentiles. 
# Also we cut out a portion of the investigator clinical specialty string that is not useful. 
# '''
# ####
####


    def clean_data(self):
        """Clean data by removing rows with NaN in the total_amount_of_payment_usdollars column."""
        if self.df is not None:
            print("Starting data cleaning...")
            # Remove rows with NaN in 'total_amount_of_payment_usdollars'

            self.df['total_amount_of_payment_usdollars'] = pd.to_numeric(
                self.df['total_amount_of_payment_usdollars'], errors='coerce')
            
            self.df = self.df.dropna(
                subset=['total_amount_of_payment_usdollars'])

            # Remove rows where 'total_amount_of_payment_usdollars' is 0
            self.df = self.df[self.df['total_amount_of_payment_usdollars'] != 0]
            # Remove rows where 'total_amount_of_payment_usdollars' is above 1,000,000
            self.df = self.df[self.df['total_amount_of_payment_usdollars'] <= 1000000]

            # Remove outliers: Keep values between 1st and 99th percentiles
            lower_percentile = self.df['total_amount_of_payment_usdollars'].quantile(
                0.05)
            upper_percentile = self.df['total_amount_of_payment_usdollars'].quantile(
                0.95)

            self.df = self.df[(self.df['total_amount_of_payment_usdollars'] >= lower_percentile) &
                              (self.df['total_amount_of_payment_usdollars'] <= upper_percentile)]

            
        
        # Check if the required column exists in the DataFrame
            if 'principal_investigator_1_specialty_1' not in self.df.columns:
                messagebox.showwarning("Missing Column", "'principal_investigator_1_specialty_1' column is missing!")
                return
            
            # Print column names and data types for diagnostic purposes
            # used for testing bugs as we wrote
            # print("Column Names:", self.df.columns)
            # print("Data Types:\n", self.df.dtypes)
            
            # Check first few rows to inspect the content
            #print("Sample Data (first 5 rows):\n", self.df['principal_investigator_1_specialty_1'].head())
    
            # Check if there are any NaN values in the column
            #print("NaN values in 'principal_investigator_1_specialty_1':", self.df['principal_investigator_1_specialty_1'].isna().sum())
    
            # Clean the 'principal_investigator_1_specialty_1' column by removing the first 25 characters (if valid)
            if 'principal_investigator_1_specialty_1' in self.df.columns:
                # Ensure all values are strings and slice after 25th character
                self.df['principal_investigator_1_specialty_1'] = self.df['principal_investigator_1_specialty_1'].apply(
                    lambda x: str(x)[36:] if isinstance(x, str) else x
                )

        # Print the cleaned data to verify
            #print("Cleaned Data:\n", self.df['principal_investigator_1_specialty_1'].head())

            messagebox.showinfo(
                "Data Cleaned", "Rows with NaN values and outliers have been removed.")
        else:
            messagebox.showwarning("No Data", "Please load data first!")

    def show_basic_stats(self):
        """Display basic stats of the data."""
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
        """
        Generate a histogram for a selected column with options for bin width and maximum X-axis.
        
        This function creates a UI window where the user can:
        1. Select a column from the loaded DataFrame.
        2. Specify the bin width for the histogram (optional).
        3. Set a maximum value for the X-axis (optional).
        
        The histogram displays:
        - A density curve (KDE) alongside the histogram.
        - Summary statistics (mean, median, mode, and range) as a text box on the plot.
        
        Uses seaborn for visualization and matplotlib for plotting adjustments.
        
        Preconditions:
        - A DataFrame must be loaded with numeric data in the selected column.
        
        Raises:
        - A warning if no data is available.
        - A ValueError if the bin width or max X-axis input is invalid.
        """
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
                """
                Generate and display a histogram for the selected column.
                
                This function processes the selected column from the DataFrame and:
                1. Calculates an appropriate number of bins based on user-provided bin width or the Freedman-Diaconis rule.
                2. Plots the histogram with a density curve (KDE) using seaborn.
                3. Optionally restricts the X-axis range to a user-defined maximum value.
                4. Annotates the plot with summary statistics (mean, median, mode, and range).
                
                Preconditions:
                - The DataFrame must be loaded with numeric data in the selected column.
                - Valid numeric values must be entered for optional bin width and maximum X-axis range, if provided.
                
                Raises:
                - A warning if no valid numeric data is available for the selected column.
                - An error if user-provided inputs (bin width or max X-axis) are not numeric.
                
                """

                selected_column = column_var.get()
                # Drop NaN values for clean plotting
                data = self.df[selected_column].dropna()

                try:
                    # Attempt to convert data to numeric, coercing errors
                    data = pd.to_numeric(data.str.replace(
                        r'[^\d.]', '', regex=True), errors='coerce').dropna()
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
        """
        Generate a bar plot showing the count of unique investigators grouped by a selected variable.
        
        This function creates a UI window where the user can:
        1. Select a column from the DataFrame to group the investigators by.
        2. Optionally specify a minimum and/or maximum count to filter the results.
        
        The resulting bar plot uses seaborn to display:
        - The unique count of investigators for each category in the selected column.
        
        Preconditions:
        - The DataFrame must be loaded and contain the 'principal_investigator_1_profile_id' column.
        
        Raises:
        - A warning if the selected column is invalid or not present in the DataFrame.
        - A ValueError if the minimum or maximum count inputs are not valid numbers.
        """

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
                """
                Generate a bar plot based on the count of unique investigators grouped by a selected variable.
                
                This function:
                1. Groups the DataFrame by the user-selected column.
                2. Counts the unique occurrences of 'principal_investigator_1_profile_id' for each group.
                3. Optionally filters the results based on user-specified minimum and/or maximum count values.
                4. Plots the filtered data as a bar plot using seaborn.
                
                Preconditions:
                - The DataFrame must be loaded and contain the 'principal_investigator_1_profile_id' column.
                
                Raises:
                - A warning if the selected column is not present in the DataFrame.
                - An error if the minimum or maximum count inputs are invalid (non-numeric).
                
                """

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

                # Group by the selected variable and count unique investigators
                investigator_counts = df.groupby(
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

    def search_by_pi(self):
        """
        Search for rows in the DataFrame based on PI's profile ID, first name, and/or last name.
        
        This function opens a UI window where the user can:
        1. Enter a profile ID, first name, last name, or any combination of these to filter the DataFrame.
        2. View the matching rows in a new window.
        3. Optionally export the search results to a CSV or Excel file.
        
        Preconditions:
        - The DataFrame must be loaded with the columns:
          - 'principal_investigator_1_profile_id'
          - 'principal_investigator_1_first_name'
          - 'principal_investigator_1_last_name'
        
        Raises:
        - A warning if no data is available or if the search yields no results.
        """
        if self.df is not None:
            # Prompt the user to enter the search criteria
            search_window = tk.Toplevel(self.root)
            search_window.title("Search Principal Investigator")

            # Create input fields for Profile ID, First Name, and Last Name
            tk.Label(search_window, text="Profile ID:",
                     font=("Arial", 12)).pack(pady=5)
            profile_id_entry = tk.Entry(search_window)
            profile_id_entry.pack(pady=5)

            tk.Label(search_window, text="First Name:",
                     font=("Arial", 12)).pack(pady=5)
            first_name_entry = tk.Entry(search_window)
            first_name_entry.pack(pady=5)

            tk.Label(search_window, text="Last Name:",
                     font=("Arial", 12)).pack(pady=5)
            last_name_entry = tk.Entry(search_window)
            last_name_entry.pack(pady=5)

            def perform_search():
                """
                Perform a search for rows in the DataFrame based on entered PI criteria.
                
                This function:
                1. Retrieves user-input values for PI's profile ID, first name, and/or last name.
                2. Filters the DataFrame dynamically based on the provided criteria.
                3. Displays the matching rows in a new window.
                4. Allows the user to export the search results to a CSV or Excel file.
                
                Preconditions:
                - The DataFrame must be loaded with the columns:
                  - 'principal_investigator_1_profile_id'
                  - 'principal_investigator_1_first_name'
                  - 'principal_investigator_1_last_name'
                
                Raises:
                - A warning if no matching rows are found based on the entered criteria.
                - An error if exporting the results fails due to an invalid file path or write error.
                """
                
                profile_id = profile_id_entry.get().strip()
                first_name = first_name_entry.get().strip()
                last_name = last_name_entry.get().strip()

                # Apply filters dynamically based on entered values
                filtered_df = self.df.copy()
                if profile_id:
                    filtered_df = filtered_df[filtered_df['principal_investigator_1_profile_id'] == profile_id]
                if first_name:
                    filtered_df = filtered_df[filtered_df['principal_investigator_1_first_name'].str.contains(
                        first_name, case=False, na=False)]
                if last_name:
                    filtered_df = filtered_df[filtered_df['principal_investigator_1_last_name'].str.contains(
                        last_name, case=False, na=False)]

                # Check if any rows match the criteria
                if filtered_df.empty:
                    messagebox.showinfo(
                        "No Results", "No matching rows found for the provided criteria.")
                    return

                # Display the matching rows
                results_window = tk.Toplevel(self.root)
                results_window.title("Search Results")

                results_text = tk.Text(
                    results_window, wrap=tk.WORD, font=("Arial", 10))
                results_text.pack(fill=tk.BOTH, expand=True)
                results_text.insert(tk.END, filtered_df.to_string(index=False))

                def export_results():
                    """
                    Export the filtered search results to a CSV or Excel file.
                    
                    This function:
                    1. Opens a file dialog for the user to select the file name and format (CSV or Excel).
                    2. Saves the current filtered DataFrame to the chosen file.
                    
                    Preconditions:
                    - A filtered DataFrame must be available from the search results.
                    
                    Raises:
                    - An error if the file cannot be written due to an invalid path or permissions issue.
                    - A warning if the user cancels the save dialog.
                    """

                    file_path = tk.filedialog.asksaveasfilename(
                        defaultextension=".csv",
                        filetypes=[("CSV files", "*.csv"),
                                   ("Excel files", "*.xlsx")],
                        title="Save Results"
                    )
                    if file_path:
                        try:
                            if file_path.endswith(".xlsx"):
                                filtered_df.to_excel(file_path, index=False)
                            else:
                                filtered_df.to_csv(file_path, index=False)
                            messagebox.showinfo(
                                "Export Successful", f"Results exported to {file_path}")
                        except Exception as e:
                            messagebox.showerror(
                                "Export Error", f"An error occurred while exporting: {e}")

                # Add an Export button
                tk.Button(results_window, text="Export",
                          command=export_results, font=("Arial", 12)).pack(pady=10)

                # Add a Close button
                tk.Button(results_window, text="Close", command=results_window.destroy, font=(
                    "Arial", 12)).pack(pady=10)

            # Add a Search button
            tk.Button(search_window, text="Search",
                      command=perform_search, font=("Arial", 12)).pack(pady=20)

            # Add a Close button
            tk.Button(search_window, text="Close", command=search_window.destroy, font=(
                "Arial", 12)).pack(pady=10)
        else:
            messagebox.showwarning("No Data", "Please load data first!")

    def get_column_for_plot(self):
        """
        Prompt the user to select a column for a plot.
        
        This function:
        1. Opens a dialog box for the user to input the name of a column.
        2. Validates the input to ensure the column exists in the DataFrame.
        3. Returns the selected column name if valid.
        
        Preconditions:
        - The DataFrame must be loaded.
        
        Returns:
        - The name of the selected column if it exists in the DataFrame.
        
        Raises:
        - A warning if the input is invalid or the column does not exist in the DataFrame.
        """

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

    def show_columns(self):
        """
        Display the list of column names in the DataFrame.
        
        This function:
        1. Opens a new window to display all column names from the loaded DataFrame.
        2. Uses a listbox widget to present the column names for easy viewing.
        3. Includes a Close button to exit the window.
        
        Preconditions:
        - The DataFrame must be loaded.
        
        Raises:
        - A warning if no data is loaded into the DataFrame.
        """

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
