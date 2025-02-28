import streamlit as st


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
    default_columns = [
        'Business Name', 'Platform', 'Amount', 'Repaid Amount', 'Risk Category'
    ]
    selected_columns = st.multiselect("Select columns to display",
                                      options=all_columns,
                                      default=default_columns)

    # If no columns selected, use default columns
    if not selected_columns:
        selected_columns = default_columns

    # Display the filtered data with selected columns
    st.dataframe(filtered_data[selected_columns], use_container_width=True)

    # Add download functionality
    csv = filtered_data.to_csv(index=False)
    st.download_button(label="Download Filtered Data",
                       data=csv,
                       file_name="filtered_loan_data.csv",
                       mime="text/csv")
