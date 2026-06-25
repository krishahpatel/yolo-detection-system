import streamlit as st
import sqlite3
import pandas as pd
import os
from streamlit_autorefresh import st_autorefresh



st.set_page_config(
    page_title="Workspace Monitoring Dashboard",
    layout="wide"
)

st_autorefresh(
    interval=5000,
    key="dashboard_refresh"
)

st.title("Workspace Monitoring Dashboard")




conn = sqlite3.connect(
    "logs/detections.db"
)



total_query = """
SELECT COUNT(*)
FROM detections
"""

total_count = pd.read_sql_query(
    total_query,
    conn
).iloc[0, 0]



class_query = """
SELECT
    class_name,
    COUNT(*) as count
FROM detections
GROUP BY class_name
ORDER BY count DESC
"""

class_df = pd.read_sql_query(
    class_query,
    conn
)



col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Total Detections",
        total_count
    )

with col2:
    st.metric(
        "Classes Detected",
        len(class_df)
    )



st.subheader("Detection Counts By Class")

st.dataframe(
    class_df,
    use_container_width=True
)

st.bar_chart(
    class_df.set_index("class_name")
)



st.subheader("Recent Detections")

recent_query = """
SELECT *
FROM detections
ORDER BY id DESC
LIMIT 20
"""

recent_df = pd.read_sql_query(
    recent_query,
    conn
)

st.dataframe(
    recent_df,
    use_container_width=True
)

conn.close()



st.subheader("Recent Snapshots")

snapshot_dir = "snapshots"

if os.path.exists(snapshot_dir):

    images = sorted(
        [
            os.path.join(snapshot_dir, file)
            for file in os.listdir(snapshot_dir)
            if file.lower().endswith(".jpg")
        ],
        reverse=True
    )

    if len(images) == 0:
        st.info("No snapshots available.")

    else:

        cols = st.columns(3)

        for idx, image in enumerate(images[:12]):

            with cols[idx % 3]:
                st.image(
                    image,
                    use_container_width=True
                )

else:
    st.warning(
        "Snapshots directory not found."
    )