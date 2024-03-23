import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Custom title with HTML and Markdown
st.markdown("""
            <h1 style="text-align: center;">Multi-cancer Early Detection Assay Performance Calculator</h1>
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
    
    for specificity in specificities:
        ppv_values = [calculate_ppv(sensitivity, specificity, p) for p in prevalence_range]
        ax.plot(prevalence_range * 100, ppv_values, label=f'Specificity {specificity}%')
        
        # Add markers for colorectal cancer prevalence at 0.5% and Pan-GI cancer at 1.5%
        colorectal_ppv = calculate_ppv(sensitivity, specificity, 0.005)
        pan_gi_ppv = calculate_ppv(sensitivity, specificity, 0.015)
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
    
    return fig

# Streamlit widgets
sensitivity = st.slider('Sensitivity (%)', min_value=0, max_value=100, value=99, step=1)
specificity_string = st.text_input('Specificities (%)', value='95,97,99')
specificities = list(map(int, specificity_string.split(',')))

# Plot
fig = create_plot(sensitivity, specificities)
st.pyplot(fig)

