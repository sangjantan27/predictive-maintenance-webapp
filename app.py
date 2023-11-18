import pandas as pd
import streamlit as st
import altair as alt
import numpy as np 
import joblib
alt.data_transformers.disable_max_rows()

# Headings
st.write("""
    # Predictive Maintenance for Industrial Devices
    *Empowering Manufacturing Efficiency through Smart Maintenance Predictions*
""")

# Sidebar Input Details
st.sidebar.header('Input Details')

def user_input_features():
    type_device = st.sidebar.selectbox('Type',('L','M','H'))
    air_temperature = st.sidebar.slider('Air Temperature (K)', 295.0, 305.0, 300.0)
    process_temperature = st.sidebar.slider('Process Temperature (K)', 305.0, 314.0, 310.0)
    rotational_speed = st.sidebar.slider("Rotational Speed (RPM)", 1168, 2886, 1500)
    torque = st.sidebar.slider("Torque (N-m)", 3.5, 77.0, 40.0)
    tool_wear = st.sidebar.slider("Tool Wear (min)", 0, 253, 108)
    data = {'Type': type_device,
            'Air Temperature': air_temperature,
            'Process Temperature': process_temperature,
            'Rotational Speed': rotational_speed,
            'Torque': torque,
            'Tool wear': tool_wear
            }
    features = pd.DataFrame(data, index=[0])
    return features
input_df = user_input_features()
input_df_copy = input_df.copy()

tab1, tab2, tab3 = st.tabs(['Maintenance Prediction', 'Result Explanation', 'About the Project'])
# Tab 1
with tab1:
    st.warning('Attention: Adjust the sliders or select values in the **sidebar** to input essential operational data.', icon="⚠️")
    st.subheader('Input Details')
    st.write(f"""
            * **Type:** {input_df['Type'].values[0]}
            * **Air Temperature:** {input_df['Air Temperature'].values[0]} K
            * **Process Temperature:** {input_df['Process Temperature'].values[0]} K
            * **Rotational Speed:** {input_df['Rotational Speed'].values[0]} RPM
            * **Torque:** {input_df['Torque'].values[0]} Nm
            * **Tool Wear:** {input_df['Tool wear'].values[0]} min
            """)

# Feature Engineering
input_df['Power'] = 2 * np.pi * input_df['Rotational Speed'] * input_df['Torque'] / 60
input_df['temp_diff'] = input_df['Process Temperature'] - input_df['Air Temperature']
input_df['Type_H'] = 0
input_df['Type_L'] = 0
input_df['Type_M'] = 0
if input_df['Type'].values == 'L':
    input_df['Type_L'] = 1
elif input_df['Type'].values == 'M':
    input_df['Type_M'] = 1
else:
    input_df['Type_H'] = 1

input_df = input_df.drop(['Type', 'Air Temperature', 'Process Temperature', 'Rotational Speed', 'Torque'], axis = 1)

model = joblib.load("predictive_maintenance.pkl")
prediction = model.predict(input_df)
prediction_probability = model.predict_proba(input_df)

# Tab 1
with tab1:
    st.subheader('Prediction')
    if prediction == 0:
        st.success('No Maintenance Required', icon="✅")
        st.write(f"Probability: **{list(prediction_probability)[0][0]:.2%}**")
    else:
        st.error('Maintenance Needed', icon="🚨")
        st.write(f"Probability: **{list(prediction_probability)[0][1]:.2%}**")


# Tab 2
with tab2:
    st.write("*See how your input data aligns with the predictive analysis. Understand where your devices stand in comparison to the data, facilitating informed decisions on maintenance priorities.*")
    input_feature = st.selectbox('Feature',('Type', 'Air Temperature', 'Process Temperature', 'Rotational Speed', 'Torque', 'Tool Wear'))
    data = pd.read_csv("predictive_maintenance.csv")
    data.columns = ['UDI', 'Product ID', 'Type', 'Air Temperature', 'Process Temperature', 'Rotational Speed', 'Torque', 'Tool wear', 'Machine failure', 'Failure type']
    data = data.drop(['UDI', 'Product ID', 'Failure type'], axis = 1)
    data = data[data['Machine failure'] == prediction[0]]
    if input_feature == 'Type':
        chart = alt.Chart(data).mark_bar().encode(
            x='Type:O',
            y="count()",
            color=alt.condition(
                alt.datum.Type == input_df_copy['Type'].values[0],
                alt.value('orange'), 
                alt.value('steelblue'))
        )
        st.altair_chart(chart, use_container_width = True)
    elif input_feature == 'Air Temperature':
        base = alt.Chart(data)

        bar = base.mark_bar().encode(
            alt.X('Air Temperature:Q').bin().axis(None),
            y='count()',
            color = alt.value('steelblue')
        )
        rule = base.mark_rule(color='orange').encode(
            x = alt.datum(input_df_copy['Air Temperature'].values[0]),
            size=alt.value(3)
        )
        st.altair_chart(bar + rule , use_container_width = True)
    elif input_feature == 'Process Temperature':
        base = alt.Chart(data)

        bar = base.mark_bar().encode(
            alt.X('Process Temperature:Q').bin().axis(None),
            y='count()',
            color = alt.value('steelblue')
        )
        rule = base.mark_rule(color='orange').encode(
            x = alt.datum(input_df_copy['Process Temperature'].values[0]),
            size=alt.value(3)
        )
        st.altair_chart(bar + rule , use_container_width = True)   
    elif input_feature == 'Rotational Speed':
        base = alt.Chart(data)

        bar = base.mark_bar().encode(
            alt.X('Rotational Speed:Q').bin().axis(None),
            y='count()',
            color = alt.value('steelblue')
        )
        rule = base.mark_rule(color='orange').encode(
            x = alt.datum(input_df_copy['Rotational Speed'].values[0]),
            size=alt.value(3)
        )
        st.altair_chart(bar + rule , use_container_width = True) 
    elif input_feature == 'Torque':
        base = alt.Chart(data)

        bar = base.mark_bar().encode(
            alt.X('Torque:Q').bin().axis(None),
            y='count()',
            color = alt.value('steelblue')
        )
        rule = base.mark_rule(color='orange').encode(
            x = alt.datum(input_df_copy['Torque'].values[0]),
            size=alt.value(3)
        )
        st.altair_chart(bar + rule , use_container_width = True) 
    else:
        base = alt.Chart(data)

        bar = base.mark_bar().encode(
            alt.X('Tool wear:Q').bin().axis(None),
            y='count()',
            color = alt.value('steelblue')
        )
        rule = base.mark_rule(color='orange').encode(
            x = alt.datum(input_df_copy['Tool wear'].values[0]),
            size=alt.value(3)
        )
        st.altair_chart(bar + rule , use_container_width = True) 


# Tab 3
with tab3:
    st.write("""
        This project revolves around using data from a manufacturing company's industrial devices. The data helps predict when these devices need maintenance, preventing breakdowns and saving money. As companies grow, keeping track of maintenance manually becomes hard. So, we propose a smart solution: using data from sensors to predict when maintenance is needed.

        The goal is to analyze the data from these sensors to figure out the best time to do maintenance on the devices. We'll use advanced techniques to do this efficiently.

        * **Type:**  Categorized as L, M, or H representing low (50% of all products), medium (30%), and high (20%) product quality variants, each with a variant-specific serial number.
        * **Air Temperature [K]:** The temperature of the surrounding air measured in Kelvin.
        * **Process Temperature [K]:** The temperature of the manufacturing process measured in Kelvin.
        * **Rotational Speed [rpm]:** The speed at which the device rotates, measured in revolutions per minute.
        * **Torque [Nm]:** The torque applied to the device, measured in Newton-meters.
        * **Tool Wear [min]:** The duration of tool usage, measured in minutes.

        By studying this data, we have created accurate models to predict maintenance needs. This will help the company know when to fix their devices, reducing downtime and costs. Automating this process is a modern solution to the challenges of keeping up with maintenance as companies get bigger and their operations get more complex.
    """)