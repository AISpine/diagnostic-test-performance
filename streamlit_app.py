pip install matplotlib
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

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
        
        # Markers for colorectal and Pan-GI cancers
        ax.plot(0.5, calculate_ppv(sensitivity, specificity, 0.005), 'o', color='blue')
        ax.plot(1.5, calculate_ppv(sensitivity, specificity, 0.015), 's', color='green')
        
    ax.set_title('PPV vs. Prevalence')
    ax.set_xlabel('Prevalence (%)')
    ax.set_ylabel('PPV (%)')
    ax.legend()
    ax.grid(True)
    
    return fig

# Streamlit widgets
sensitivity = st.slider('Sensitivity (%)', min_value=50, max_value=100, value=99, step=1)
specificity_string = st.text_input('Specificities (%)', value='95,97,99')
specificities = list(map(int, specificity_string.split(',')))

# Plot
fig = create_plot(sensitivity, specificities)
st.pyplot(fig)

