import streamlit as st
import pandas as pd


def render_data_display(df):
    st.header("Raw Data")

    # Add search functionality
    search_term = st.text_input(
        "Search data", placeholder="Enter business name or filter term")

    # Filter data based on search term if provided
    if search_term:
        filtered_data = df[df.astype(str).apply(
            lambda row: row.str.contains(search_term, case=False).any(),
            axis=1)]
    else:
        filtered_data = df

    # Display number of records
    st.write(f"Displaying {len(filtered_data)} records")

    # Allow column selection
    all_columns = df.columns.tolist()

    # Check if the column exists before setting as default
    default_columns = []
    for col in [
            'Business Name', 'Platform', 'Amount', 'Repaid Amount',
            'risk_category', 'Date Funded'
    ]:
        if col in all_columns:
            default_columns.append(col)

    if not default_columns and all_columns:  # If none of the preferred defaults exist
        default_columns = all_columns[:min(5, len(
            all_columns))]  # Use first 5 columns or less

    selected_columns = st.multiselect("Select columns to display",
                                      options=all_columns,
                                      default=default_columns)

    # If no columns selected, use default columns
    if not selected_columns and default_columns:
        selected_columns = default_columns

    # Format currency columns before display
    display_data = filtered_data.copy()

    # Add dollar sign and format Amount column if it exists
    if 'Amount' in display_data.columns:
        display_data['Amount'] = display_data['Amount'].apply(
            lambda x: f"${x:,.0f}")

    # Add dollar sign and remove decimals from Repaid Amount column if it exists
    if 'Repaid Amount' in display_data.columns:
        display_data['Repaid Amount'] = display_data['Repaid Amount'].apply(
            lambda x: f"${x:,.0f}")

    # Format Date Funded column if it exists
    if 'Date Funded' in display_data.columns:
        display_data['Date Funded'] = pd.to_datetime(display_data['Date Funded']).dt.date

    # Display the filtered data with selected columns, hiding the index
    if selected_columns:
        st.dataframe(display_data[selected_columns], use_container_width=True, hide_index=True)
    else:
        st.dataframe(display_data, use_container_width=True, hide_index=True)

    # Add download functionality
    csv = filtered_data.to_csv(index=False)
    st.download_button(label="Download Filtered Data",
                       data=csv,
                       file_name="filtered_loan_data.csv",
                       mime="text/csv")
