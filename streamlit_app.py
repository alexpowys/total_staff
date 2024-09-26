# Import python packages

import streamlit as st
import snowflake.connector
import pandas as pd


# Write directly to the app
st.title("MoD Commission Dashboard")
st.write(
    """MoD Commissions for previous cycle
    """
)

conn = snowflake.connector.connect(
        user='DEPUTYUSER',
        password='wm$4Zh62',
        account='dfzqycb-tz75056',
        warehouse='COMPUTE_WH',
        database='DEPUTY',
        schema='RAW')

cursor = conn.cursor()

query = '''
with cte as (select 
display_name,
value:Module as module_id,
t1.title as title
from deputy.fact.employees_fact_recent as t0
left join table(flatten(input => t0.training_array, outer => TRUE)) f 
left join deputy.fact.training_module_fact as t1
on module_id = t1.id)
select count(display_name) as staff_count, title from cte 
where title in ('Level 1', 'Level 2', 'Level 3', 'MOD')
group by title
order by staff_count desc;
'''

cursor.execute(query)
result = cursor.fetchall()

df = pd.DataFrame(result,
                      columns=['Staff Count', 'Training'])

# Create a simple bar chart
# See docs.streamlit.io for more types of charts
st.subheader("Commission and Total Sales")
st.bar_chart(data=df, x="Staff Count")

st.subheader("Underlying data")
st.dataframe(df, use_container_width=True)