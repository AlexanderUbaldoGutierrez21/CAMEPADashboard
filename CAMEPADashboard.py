import pandas as pd
import plotly.express as px
import streamlit as st

# Set Page Configuration
st.set_page_config(
    page_title="Panama EV Sales Outlook 2015-2024",
    layout="wide"
)

# Load Data from Excel file
@st.cache_data
def load_data():
    df = pd.read_excel(
        io="EV Growth Panama.xlsx",
        engine="openpyxl",
        sheet_name="EVPanama",
        nrows=11,
    )
    # Normalize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    return df

df = load_data()

st.sidebar.image("Logo.png", width=120)

# Side Bar
st.sidebar.title("E-Mobility Chamber of Panama 2024")
st.sidebar.header("⚙️ Settings")
year_column = 'Years' if 'Years' in df.columns else df.columns[0]
years = st.sidebar.multiselect(
    "Select a Year",
    options=df[year_column].unique(),
    default=df[year_column].unique(),
    key="years_multiselect"
)

df_selection = df[df[year_column].isin(years)]

# Main Page
st.title("Panama EV Sales Outlook 2015-2024")
st.markdown("---")

# TOP KPI'S 
total_ev = int(df_selection.get("Unit EVs Sold", df_selection.iloc[:, 2]).sum())
total_hybrid = int(df_selection.get("Unit Hybrid Vehicles Sold", df_selection.iloc[:, 1]).sum())

col1, col2 = st.columns(2)
col1.metric("Total Electric Vehicle (BEV) Sales", f"{total_ev:,}")
col2.metric("Total Hybrid Vehicle Sales", f"{total_hybrid:,}")

st.markdown("---")

# Function to create bar chart
def create_bar_chart(data, x, y, title, color="#121840"):
    fig = px.bar(
        data,
        x=x,
        y=y,
        title=f"<b>{title}</b>",
        color_discrete_sequence=[color] * len(data),
        template="plotly_white",
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, title=None),
        yaxis=dict(title=None, tickformat=","),
        showlegend=False
    )
    return fig

# Electric Vehicle (BEV) Sales 2015-2024
fig_ev_sales = create_bar_chart(df_selection, year_column, df_selection.columns[2], "Electric Vehicle (BEV) Sales 2015-2024")

# Hybrid Vehicle Sales 2015-2024
fig_hybrid_sales = create_bar_chart(df_selection, year_column, df_selection.columns[1], "Hybrid Vehicle Sales 2015-2024")

# Display charts
with st.container():
    col1, col2 = st.columns(2)
with st.container(border=True):
    st.plotly_chart(fig_ev_sales, use_container_width=True)
    st.markdown("<u style='font-size: 12px;'>Data Updated: October 2024</u>", unsafe_allow_html=True)
with st.container(border=True):
    st.plotly_chart(fig_hybrid_sales, use_container_width=True)
    st.markdown("<u style='font-size: 12px;'>Data Updated: October 2024</u>", unsafe_allow_html=True)
  
# Run and Update App   
    from streamlit.runtime.scriptrunner import RerunData, RerunException

def clear_streamlit_cache():
    raise RerunException(RerunData())
