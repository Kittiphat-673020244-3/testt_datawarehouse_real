import streamlit as st
import duckdb
import pandas as pd

st.set_page_config(page_title="Northwind DW Explorer", layout="wide")

st.title("📊 Northwind DW Explorer")
st.caption("Inspect and preview raw datasets, staging tables, and dimension views in dev.duckdb")

# เชื่อมต่อกับ DuckDB (ไฟล์ DB จะถูกสร้างอัตโนมัติเมื่อสั่งรัน dbt)
conn = duckdb.connect('northwind_dw_duckdb/dev.duckdb')

# ดึงตารางทั้งหมด
tables_df = conn.execute("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'main'
""").df()

tables_list = tables_df['table_name'].tolist() if not tables_df.empty else []

st.sidebar.header("📁 Table Browser")
selected_table = st.sidebar.selectbox("Select a table to inspect", tables_list if tables_list else ["No tables found"])

st.sidebar.markdown("---")
st.sidebar.subheader("Quick Stats")
st.sidebar.write(f"**Total Tables:** {len(tables_list)}")

tab1, tab2 = st.tabs(["📜 Database Schema & Overview", "🔍 Data Viewer & Metadata"])

with tab1:
    st.subheader("Database Tables Overview")
    overview_data = []
    total_rows = 0
    for tbl in tables_list:
        count = conn.execute(f"SELECT COUNT(*) FROM main.{tbl}").fetchone()[0]
        overview_data.append({"Table Name": tbl, "Row Count": count})
        total_rows += count

    col1, col2 = st.columns(2)
    col1.metric("Total Tables in 'main' Schema", len(tables_list))
    col2.metric("Total Records Across All Tables", total_rows)

    st.markdown("### Table List & Record Counts")
    if overview_data:
        st.dataframe(pd.DataFrame(overview_data), use_container_width=True)

with tab2:
    if selected_table and selected_table != "No tables found":
        st.subheader(f"Data Preview: {selected_table}")
        df_preview = conn.execute(f"SELECT * FROM main.{selected_table} LIMIT 100").df()
        st.dataframe(df_preview, use_container_width=True)

conn.close()