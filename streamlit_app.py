import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Custom title with HTML and Markdown
st.markdown("""
            <h1 style="text-align: center;">Multi-cancer detection assay performance calculator</h1>
            <h2 style="text-align: center; font-style: italic;">(by Elie Massaad, MD, MSc)</h2>
            """, unsafe_allow_html=True)

# Define the calculation function
def calculate_ppv(sensitivity, specificity, prevalence):
    sensitivity = sensitivity / 100
    specificity = specificity / 100
    ppv = (sensitivity * prevalence) / ((sensitivity * prevalence) + ((1 - specificity) * (1 - prevalence)))
    return ppv * 100

# Create the plot
def create_plot(sensitivity, specificities):
    prevalence_range = np.linspace(0, 0.03, 100)
    fig, ax = plt.subplots()
    
    ppv_table_data = []
    
    for specificity in specificities:
        ppv_values = [calculate_ppv(sensitivity, specificity, p) for p in prevalence_range]
        ax.plot(prevalence_range * 100, ppv_values, label=f'Specificity {specificity}%')
        
        # Calculate PPV for colorectal and Pan-GI cancer prevalences
        colorectal_ppv = calculate_ppv(sensitivity, specificity, 0.005)
        pan_gi_ppv = calculate_ppv(sensitivity, specificity, 0.015)
        
        # Append the PPV values for the table
        ppv_table_data.append({'Specificity': specificity,
                               'Colorectal Cancer PPV (%)': colorectal_ppv,
                               'Pan-GI Cancer PPV (%)': pan_gi_ppv})
        
      # Define the style for each type of marker
        colorectal_marker_style = {'color': 'blue', 'marker': 'o', 'markersize': 8}
        pan_gi_marker_style = {'color': 'green', 'marker': 's', 'markersize': 8}
        plt.plot(0.5, colorectal_ppv, **colorectal_marker_style, label='Colorectal Cancer (0.5% Prevalence)' if specificity == specificities[0] else "")
        plt.plot(1.5, pan_gi_ppv, **pan_gi_marker_style, label='Pan-GI Cancer (1.5% Prevalence)' if specificity == specificities[0] else "")

    plt.title('PPV vs. Prevalence for Different Specificities')
    plt.xlabel('Prevalence, %')
    plt.ylabel('PPV, %')
    plt.legend()
    plt.grid(True)
    
    plt.show()
    
    # Return the figure and the table data
    return fig, ppv_table_data

# Streamlit widgets for input
sensitivity = st.slider('Sensitivity (%)', min_value=0, max_value=100, value=99, step=1)
specificity_string = st.text_input('Specificities (%)', value='95,97,99')
specificities = list(map(int, specificity_string.split(',')))

# Generate the plot and table data
fig, ppv_table_data = create_plot(sensitivity, specificities)

# Display the plot
st.pyplot(fig)

# Create a DataFrame from the PPV values and display it as a table
ppv_df = pd.DataFrame(ppv_table_data)
st.table(ppv_df)


