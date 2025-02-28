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

    # Display number of records and max loan amount
    st.write(f"Displaying {len(filtered_data)} records")
    
    # Show max loan amount if data exists and column exists
    if not filtered_data.empty and 'amount' in filtered_data.columns:
        max_loan = filtered_data['amount'].max()
        st.write(f"Maximum loan amount: ${max_loan:,.0f}")

    # Allow column selection
    all_columns = df.columns.tolist()

    # Check if the column exists before setting as default
    default_columns = []
    for col in [
            'business_name', 'platform', 'amount', 'repaid_amount', 'fees',
            'risk_category', 'funded_date', 'vintage'
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

    # Keep a sortable copy of the data
    sortable_data = filtered_data.copy()
    
    # Format currency columns for display purposes
    display_data = filtered_data.copy()

    # Format Date Funded column if it exists
    if 'funded_date' in display_data.columns:
        display_data['funded_date'] = pd.to_datetime(
            display_data['funded_date']).dt.date
    
    # Add dollar sign and format Amount column if it exists
    if 'amount' in display_data.columns:
        display_data['amount'] = display_data['amount'].apply(
            lambda x: f"${x:,.0f}")

    # Add dollar sign and remove decimals from Repaid Amount column if it exists
    if 'repaid_amount' in display_data.columns:
        display_data['repaid_amount'] = display_data['repaid_amount'].apply(
            lambda x: f"${x:,.0f}")

    # Add dollar sign and remove decimals from fees column if it exists
    if 'fees' in display_data.columns:
        display_data['fees'] = display_data['fees'].apply(
            lambda x: f"${x:,.0f}")

    # Display the filtered data with selected columns, hiding the index
    # Use the original numeric data for sorting while showing the formatted display data
    if selected_columns:
        st.dataframe(
            data=display_data[selected_columns],
            use_container_width=True,
            hide_index=True,
            # Provide the original numeric data for proper sorting
            column_config={
                "amount": st.column_config.NumberColumn(
                    format="$%d",
                    help="Loan amount",
                    step=1000,
                ),
                "repaid_amount": st.column_config.NumberColumn(
                    format="$%d",
                    help="Amount repaid so far",
                    step=1000,
                ),
                "fees": st.column_config.NumberColumn(
                    format="$%d",
                    help="Fees collected",
                    step=100,
                )
            }
        )
    else:
        st.dataframe(
            data=display_data,
            use_container_width=True,
            hide_index=True,
            # Provide the original numeric data for proper sorting
            column_config={
                "amount": st.column_config.NumberColumn(
                    format="$%d",
                    help="Loan amount",
                    step=1000,
                ),
                "repaid_amount": st.column_config.NumberColumn(
                    format="$%d",
                    help="Amount repaid so far",
                    step=1000,
                ),
                "fees": st.column_config.NumberColumn(
                    format="$%d",
                    help="Fees collected",
                    step=100,
                )
            }
        )

    # Add download functionality
    csv = filtered_data.to_csv(index=False)
    st.download_button(label="Download Filtered Data",
                       data=csv,
                       file_name="filtered_loan_data.csv",
                       mime="text/csv")
