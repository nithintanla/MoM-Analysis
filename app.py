import streamlit as st
import pandas as pd

# Set the page layout to wide
st.set_page_config(layout="wide")

st.title('Excel Files Analysis App')

# Upload last month Excel file
last_month_file = st.file_uploader("Choose Last Month Excel file", type=["xlsx"], key="last_month")

# Upload current month Excel file
curr_month_file = st.file_uploader("Choose Current Month Excel file", type=["xlsx"], key="curr_month")

if last_month_file and curr_month_file:
    # Read each Excel file
    last_month_df = pd.read_excel(last_month_file)
    curr_month_df = pd.read_excel(curr_month_file)
    
    # Remove the row with "Overall" from the "Brand" column
    last_month_df = last_month_df[last_month_df['Brand'] != 'Overall']
    curr_month_df = curr_month_df[curr_month_df['Brand'] != 'Overall']
    
    # Add "NetBillableMsgs" column
    last_month_df['NetBillableMsgs'] = last_month_df['Messages Sent'] - last_month_df['Messages Expired']
    curr_month_df['NetBillableMsgs'] = curr_month_df['Messages Sent'] - curr_month_df['Messages Expired']
    
    # Tag the dataframes
    last_month_df['Month'] = 'Last Month'
    curr_month_df['Month'] = 'Current Month'
    
    # Combine the dataframes
    combined_df = pd.concat([last_month_df, curr_month_df])
    
    # Get unique aggregators
    aggregators = combined_df['Aggregator'].unique()
    
    # Select an aggregator
    selected_aggregator = st.selectbox("Select Aggregator", aggregators)
    
    # Filter dataframes based on selected aggregator
    last_month_df = last_month_df[last_month_df['Aggregator'] == selected_aggregator]
    curr_month_df = curr_month_df[curr_month_df['Aggregator'] == selected_aggregator]
    
    # Identify new brands in the current month
    gained_brands = curr_month_df[~curr_month_df['Brand'].isin(last_month_df['Brand'])]
    st.write("Gained Brands")
    st.dataframe(gained_brands)
    
    # Identify lost brands from the last month
    lost_brands = last_month_df[~last_month_df['Brand'].isin(curr_month_df['Brand'])]
    st.write("Lost Brands")
    st.dataframe(lost_brands)
    
    # Identify common brands in both months
    common_brands = last_month_df[last_month_df['Brand'].isin(curr_month_df['Brand'])]
    st.write("Common Brands")
    st.dataframe(common_brands)
    
    # Calculate the sum of NetBillableMsgs for each case
    summary_data = {
        "Category": ["Last Month", "Current Month", "Gained Brands", "Lost Brands", "Common Brands"],
        "NetBillableMsgs Sum": [
            last_month_df['NetBillableMsgs'].sum(),
            curr_month_df['NetBillableMsgs'].sum(),
            gained_brands['NetBillableMsgs'].sum(),
            lost_brands['NetBillableMsgs'].sum(),
            common_brands['NetBillableMsgs'].sum()
        ]
    }
    summary_df = pd.DataFrame(summary_data)
    
    # Display the summary table
    st.write("Summary of Net Billable Messages")
    st.dataframe(summary_df)
else:
    st.write("Please upload both the Last Month and Current Month Excel files.")
