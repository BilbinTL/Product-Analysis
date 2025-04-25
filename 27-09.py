import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image

st.write("✅ Streamlit version:", st.__version__)
st.write("✅ Plotly version:", plotly.__version__)
st.write("✅ Pandas version:", pd.__version__)
# Set the page configuration
st.set_page_config(page_title='Dashboard', layout='wide')

# Main page content
st.title("SME Data Viewer")

# Create tabs for SME Data and Vehicle Loan Segment
sme_tab, vl_tab = st.tabs(["SME Data", "Vehicle Loan Segment"])

# SME Data Tab
with sme_tab:
    # Main page content for SME Data
    st.markdown("<h1 style='text-align: center;'>Product Analysis Apr to Aug</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Was it helpful?</h3>", unsafe_allow_html=True)

    # Description
    st.markdown("""
        <h2 style='text-align: center;'>Product Team</h2>
        <p style='text-align: center;'>We analyze and optimize product performance across various metrics to enhance our service quality.</p>
    """, unsafe_allow_html=True)

    # Load and display the logo
    image_path = 'E:\\New_web\\m LOGO.jpg'
    image = Image.open(image_path)
    st.image(image, width=350, caption="Product Team Logo", use_column_width=False)

    # Load Excel data
    excel_path = 'E:\\New_web\\Product wise disbursment ML Apr to Aug - Copy.xlsx'
    df = pd.read_excel(excel_path, sheet_name='Product name ML')
    df_t = pd.read_excel(excel_path, sheet_name='Type of loan ML')
    df_s = pd.read_excel(excel_path, sheet_name='Sales executive with branch ML', header=12)
    df_b = pd.read_excel(excel_path, sheet_name='Branch wise ML')
    df_y = pd.read_excel(excel_path, sheet_name='Yield ML')
    df_d = pd.read_excel(excel_path, sheet_name='Disb trend ML', usecols='A:B')
    df_yt = pd.read_excel(excel_path, sheet_name='Monthly Yield line ML')
    df_yb = pd.read_excel(excel_path, sheet_name='Branch wise yield ML')

    # Create a line chart with data labels for ML Disbursement Trend
    line_chart = px.line(df_d, x=df_d.columns[0], y=df_d.columns[1],
                         title="Disbursement Trend (SME)",
                         labels={df_d.columns[0]: 'Month', df_d.columns[1]: 'Amount'},
                         markers=True)
    line_chart.update_layout(yaxis=dict(range=[0, 800], tick0=500, dtick=200, tickformat=".2f"))
    line_chart.update_traces(text=df_d[df_d.columns[1]].round(2).astype(str), textposition="top right", mode='lines+markers+text')
    st.plotly_chart(line_chart, use_container_width=True)

    # Function to format DataFrame columns as percentage
    def format_as_percentage(df, columns):
        for column in columns:
            if column in df.columns:
                df[column] = (df[column] * 100).round(2).astype(str) + '%'
        return df

    # List of columns to convert to percentage in different DataFrames
    yield_month_columns = ['April', 'May', 'June', 'July', 'August', 'September', 'YTD Yield']
    df_y_formatted = format_as_percentage(df_y.copy(), yield_month_columns)

    df_yt_formatted = format_as_percentage(df_yt.copy(), ['Yield'])

    yield_month_branch = ['April', 'May', 'June', 'July', 'August', 'September']
    df_yb_formatted = format_as_percentage(df_yb.copy(), yield_month_branch)

    st.title('Yield (SME)')

    # Collapsible section for Yield data
    with st.expander("View Yield Data (SME)"):
        st.dataframe(df_y_formatted)
        st.dataframe(df_yt_formatted)
        st.dataframe(df_yb_formatted)

    # Dashboard layout with two columns for product and loan type data
    st.markdown("### Product and Loan Types (SME)")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Products")
        st.dataframe(df, use_container_width=True)
    with col2:
        st.subheader("Type of Loans")
        st.dataframe(df_t, use_container_width=True)

    # Pie chart for Product Distribution
    st.markdown("### Product Distribution (SME)")
    if 'Product Name' in df.columns and 'Total Amount' in df.columns:
        pie_chart = px.pie(df, title='Products by Total Amount (SME)', values='Total Amount', names='Product Name')
        st.plotly_chart(pie_chart, use_container_width=True)
    else:
        st.error("Required columns not found in the DataFrame for the pie chart.")

    # Filters for Branch and Month
    st.markdown("### Filter Data (SME)")
    branches = df_b['Branch Name'].unique()
    selected_branch = st.selectbox('Select Branch', options=['All'] + list(branches))
    month_columns = ['April', 'May', 'June', 'July', 'August', 'Total Amount']
    selected_month = st.selectbox('Select Month', options=['All'] + month_columns)

    # Apply filters to df_b (Branch wise data)
    filtered_df_b = df_b.copy()
    if selected_branch != 'All':
        filtered_df_b = filtered_df_b[filtered_df_b['Branch Name'] == selected_branch]
    if selected_month != 'All':
        if selected_month in filtered_df_b.columns:
            filtered_df_b = filtered_df_b[['Branch Name', selected_month]].rename(columns={selected_month: 'Total Amount'})
            filtered_df_b['Total Amount'] = filtered_df_b['Total Amount'].astype(float)
        else:
            st.error(f"Month column '{selected_month}' not found in DataFrame.")
    else:
        filtered_df_b = filtered_df_b[['Branch Name'] + month_columns]

    # Display filtered dataframe and donut chart side by side
    st.markdown("### Total Amount Distribution (SME)")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Branch-wise Disbursement Data (SME)")
        st.dataframe(filtered_df_b)
    with col2:
        if 'Total Amount' in filtered_df_b.columns and 'Branch Name' in filtered_df_b.columns:
            donut_chart = px.pie(filtered_df_b, names='Branch Name', values='Total Amount', title='Branch-wise Disbursement (SME)', hole=0.4)
            st.plotly_chart(donut_chart, use_container_width=True)
        else:
            st.error("Required columns not found in the DataFrame for the donut chart.")

    # Apply filters to df_s (Sales Executive Data)
    filtered_df_s = df_s.copy()
    if selected_branch != 'All':
        filtered_df_s = filtered_df_s[filtered_df_s['Branch Name'] == selected_branch]
    if selected_month != 'All':
        if selected_month in filtered_df_s.columns:
            filtered_df_s = filtered_df_s[['Name of Sales Executive', selected_month]].rename(columns={selected_month: 'Total Amount'})
            filtered_df_s['Total Amount'] = filtered_df_s['Total Amount'].astype(float)
        else:
            st.error(f"Month column '{selected_month}' not found in DataFrame.")

    # Sales Executive Data and Top Performers Chart
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Sales Executive Data (SME)")
        st.dataframe(filtered_df_s)
    with col2:
        if 'Name of Sales Executive' in filtered_df_s.columns and 'Total Amount' in filtered_df_s.columns:
            top_performers = filtered_df_s.sort_values(by='Total Amount', ascending=False).reset_index(drop=True)
            bar_chart = px.bar(top_performers.head(10), x='Name of Sales Executive', y='Total Amount', title='Top 10 Performers (SME)', labels={'Name of Sales Executive': 'Sales Executive', 'Total Amount': 'Total Sales'}, color='Total Amount', color_continuous_scale='Blues')
            st.subheader("Top 10 Sales Performers (SME)")
            st.plotly_chart(bar_chart, use_container_width=True)
        else:
            st.error("Required columns not found in the DataFrame for the bar chart.")

# Vehicle Loan Segment Tab
with vl_tab:
    st.markdown("<h1 style='text-align: center;'>Vehicle Loan Segment Apr to Aug</h1>", unsafe_allow_html=True)

    # Load Excel data for Vehicle Loan (VL)
    excel_path_vl = 'E:\\New_web\\Database VL.xlsx'
    df_vl = pd.read_excel(excel_path_vl, sheet_name='Product name VL')
    df_s_vl = pd.read_excel(excel_path_vl, sheet_name='Sales executive with branch VL', header=12)
    df_b_vl = pd.read_excel(excel_path_vl, sheet_name='Branch wise VL')
    df_y_vl = pd.read_excel(excel_path_vl, sheet_name='Yield VL')
    df_d_vl = pd.read_excel(excel_path_vl, sheet_name='Disb trend VL', usecols='A:B')
    df_yt_vl = pd.read_excel(excel_path_vl, sheet_name='Monthly Yield line VL')
    df_yb_vl = pd.read_excel(excel_path_vl, sheet_name='Branch wise yield VL')
    df_yd_vl = pd.read_excel(excel_path_vl, sheet_name='DSA with executive VL')
    df_b_vl=df_b_vl.round(2)
    df_vl=df_vl.round(2)  
    # Create a line chart with data labels for VL Disbursement Trend
    line_chart_vl = px.line(df_d_vl, x=df_d_vl.columns[0], y=df_d_vl.columns[1],
                            title="Disbursement Trend (Vehicle Loans)",
                            labels={df_d_vl.columns[0]: 'Month', df_d_vl.columns[1]: 'Amount'},
                            markers=True)
    line_chart_vl.update_layout(yaxis=dict(range=[0, 800], tick0=500, dtick=200, tickformat=".2f"))
    line_chart_vl.update_traces(text=df_d_vl[df_d_vl.columns[1]].round(2).astype(str), textposition="top right", mode='lines+markers+text')
    st.plotly_chart(line_chart_vl, use_container_width=True)

    # Function to format DataFrame columns as percentage
    def format_as_percentage_vl(df, columns):
        for column in columns:
            if column in df.columns:
                df[column] = (df[column] * 100).round(2).astype(str) + '%'
        return df

    # List of columns to convert to percentage in different DataFrames
    yield_month_columns_vl = ['April', 'May', 'June', 'July', 'August', 'September', 'YTD Yield']
    df_y_vl_formatted = format_as_percentage_vl(df_y_vl.copy(), yield_month_columns_vl)

    df_yt_vl_formatted = format_as_percentage_vl(df_yt_vl.copy(), ['Yield'])

    yield_month_branch_vl = ['April', 'May', 'June', 'July', 'August', 'September']
    df_yb_vl_formatted = format_as_percentage_vl(df_yb_vl.copy(), yield_month_branch_vl)

    st.title('Yield (Vehicle Loan)')
    df_y_vl_formatted=df_y_vl_formatted.round(2)
    df_yt_vl_formatted=df_yt_vl_formatted.round(2)
    df_yb_vl_formatted=df_yb_vl_formatted.round(2)
    # Collapsible section for Yield VL data
    with st.expander("View Yield Data (Vehicle Loan)"):
        st.dataframe(df_y_vl_formatted)
        st.dataframe(df_yt_vl_formatted)
        st.dataframe(df_yb_vl_formatted)

    # Dashboard layout with two columns for product and loan type data (VL)
    st.markdown("### Product and Loan Types (Vehicle Loan)")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Products")
        st.dataframe(df_vl, use_container_width=True)

    # Pie chart for Product Distribution (VL)
    st.markdown("### Product Distribution (Vehicle Loan)")
    if 'Product Name' in df_vl.columns and 'Total Amount' in df_vl.columns:
        pie_chart_vl = px.pie(df_vl, title='Products by Total Amount (Vehicle Loan)', values='Total Amount', names='Product Name')
        st.plotly_chart(pie_chart_vl, use_container_width=True)
    else:
        st.error("Required columns not found in the Vehicle Loan DataFrame for the pie chart.")

    # Filters for Branch and Month (VL)
    st.markdown("### Filter Data (Vehicle Loan)")
    branches_vl = df_b_vl['Branch Name'].unique()
    selected_branch_vl = st.selectbox('Select Branch (Vehicle Loan)', options=['All'] + list(branches_vl))
    month_columns_vl = ['April', 'May', 'June', 'July', 'August', 'Total Amount']
    selected_month_vl = st.selectbox('Select Month (Vehicle Loan)', options=['All'] + month_columns_vl)

    # Apply filters to df_b_vl (Branch wise VL data)
    filtered_df_b_vl = df_b_vl.copy()
    if selected_branch_vl != 'All':
        filtered_df_b_vl = filtered_df_b_vl[filtered_df_b_vl['Branch Name'] == selected_branch_vl]
    if selected_month_vl != 'All':
        if selected_month_vl in filtered_df_b_vl.columns:
            filtered_df_b_vl = filtered_df_b_vl[['Branch Name', selected_month_vl]].rename(columns={selected_month_vl: 'Total Amount'})
            filtered_df_b_vl['Total Amount'] = filtered_df_b_vl['Total Amount'].astype(float)
        else:
            st.error(f"Month column '{selected_month_vl}' not found in DataFrame.")
    else:
        filtered_df_b_vl = filtered_df_b_vl[['Branch Name'] + month_columns_vl]

    # Display filtered dataframe and donut chart side by side (VL)
    st.markdown("### Total Amount Distribution (Vehicle Loan)")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Branch-wise Disbursement Data (Vehicle Loan)")
        st.dataframe(filtered_df_b_vl)
    with col2:
        if 'Total Amount' in filtered_df_b_vl.columns and 'Branch Name' in filtered_df_b_vl.columns:
            donut_chart_vl = px.pie(filtered_df_b_vl, names='Branch Name', values='Total Amount', title='Branch-wise Disbursement (Vehicle Loan)', hole=0.4)
            st.plotly_chart(donut_chart_vl, use_container_width=True)
        else:
            st.error("Required columns not found in the Vehicle Loan DataFrame for the donut chart.")

    # Apply filters to df_s_vl (Sales Executive VL Data)
    filtered_df_s_vl = df_s_vl.copy()
    if selected_branch_vl != 'All':
        filtered_df_s_vl = filtered_df_s_vl[filtered_df_s_vl['Branch Name'] == selected_branch_vl]
    if selected_month_vl != 'All':
        if selected_month_vl in filtered_df_s_vl.columns:
            filtered_df_s_vl = filtered_df_s_vl[['Name of Sales Executive', selected_month_vl]].rename(columns={selected_month_vl: 'Total Amount'})
            filtered_df_s_vl['Total Amount'] = filtered_df_s_vl['Total Amount'].astype(float)
        else:
            st.error(f"Month column '{selected_month_vl}' not found in DataFrame.")

    # Sales Executive Data and Top Performers Chart (VL)
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Sales Executive Data (Vehicle Loan)")
        st.dataframe(filtered_df_s_vl)
    with col2:
        if 'Name of Sales Executive' in filtered_df_s_vl.columns and 'Total Amount' in filtered_df_s_vl.columns:
            top_performers_vl = filtered_df_s_vl.sort_values(by='Total Amount', ascending=False).reset_index(drop=True)
            bar_chart_vl = px.bar(top_performers_vl.head(10), x='Name of Sales Executive', y='Total Amount', title='Top 10 Performers (Vehicle Loan)', labels={'Name of Sales Executive': 'Sales Executive', 'Total Amount': 'Total Sales'}, color='Total Amount', color_continuous_scale='Oranges')
            st.subheader("Top 10 Sales Performers (Vehicle Loan)")
            st.plotly_chart(bar_chart_vl, use_container_width=True)
        else:


            st.error("Required columns not found in the Vehicle Loan DataFrame for the bar chart.")

   # DSA with Sales Executive section
# Vehicle Loan Segment Tab
with vl_tab:
    
    st.markdown("## DSA with Sales Executive")

    # Create filters for DSA data
    sales_executives = df_yd_vl['Name Of Sales Executive'].unique()
    selected_executive = st.selectbox('Select Sales Executive', options=['All'] + list(sales_executives))

    # Apply filters to df_yd_vl (DSA Data)
    filtered_df_yd_vl = df_yd_vl.copy()
    if selected_branch_vl != 'All':
        filtered_df_yd_vl = filtered_df_yd_vl[filtered_df_yd_vl['Branch'] == selected_branch_vl]
    if selected_executive != 'All':
        filtered_df_yd_vl = filtered_df_yd_vl[filtered_df_yd_vl['Name Of Sales Executive'] == selected_executive]

    # Display the filtered DataFrame
    filtered_df_yd_vl=filtered_df_yd_vl.round(2)
    st.markdown("### Filtered DSA Data")
    st.dataframe(filtered_df_yd_vl, use_container_width=True)

    # Show summary statistics button
    if st.button('Show Summary Statistics (Vehicle Loan)'):
        # Calculate summary statistics
        branch_count = filtered_df_yd_vl['Branch'].nunique()  # Count of unique branches
        dsa_count = filtered_df_yd_vl['DSA'].count()  # Count of non-null DSA entries
        emp_count = filtered_df_yd_vl['Name Of Sales Executive'].nunique()  # Count of unique sales executives
        April_1 = filtered_df_yd_vl['April'].sum(numeric_only=True).round(2)  # Sum of numeric columns
        May_2 =  filtered_df_yd_vl['May'].sum(numeric_only=True).round(2)
        June_3 = filtered_df_yd_vl['June'].sum(numeric_only=True).round(2)
        July_4 = filtered_df_yd_vl['July'].sum(numeric_only=True).round(2)
        August_5 = filtered_df_yd_vl['August'].sum(numeric_only=True).round(2)
        September_6 = filtered_df_yd_vl['September'].sum(numeric_only=True).round(2)
        October_7 = filtered_df_yd_vl['October'].sum(numeric_only=True).round(2)
        November_7 = filtered_df_yd_vl['November'].sum(numeric_only=True).round(2)
        Total_amt = filtered_df_yd_vl['Total Amount'].sum(numeric_only=True).round(2)
        # Display results in a collapsible section
        with st.expander("Summary Statistics (Vehicle Loan)", expanded=True):
            st.markdown("### Count of Entries:")
            st.write(f"No of Branches: {branch_count}")
            st.write(f"No of DSA: {dsa_count}")
            st.write(f"No of Sales Executives: {emp_count}")

            st.markdown("### Sum of Numeric Columns:")
            st.write(f"April: {April_1}")
            st.write(f"May: {May_2}")
            st.write(f"June: {June_3}") 
            st.write(f"July: {July_4}")
            st.write(f"August: {August_5}")
            st.write(f"Total Amount: {Total_amt}")
            
