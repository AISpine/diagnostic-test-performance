import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Custom title with HTML and Markdown
st.markdown("""
            <h1 style="text-align: center;">Multi-cancer Detection Assay Performance Calculator</h1>
            <h2 style="text-align: center; font-style: italic;">(by Elie Massaad, MD, MSc)</h2>
            """, unsafe_allow_html=True)

# Define a nested dictionary with tumors and their prevalences for each age group
age_group_prevalences = {
    'All ages': {'Lung and Bronchus': 0.05, 'Colon and Rectum': 0.0366,'Pancreas': 0.0133,
                 'Liver and intrahepatic bile duct': 0.0093,'Urinary bladder': 0.0182,
                 'Esophagus': 0.0042,'Kidney/renal pelvis': 0.0172,
                 'Stomach': 0.0069,'Head&Neck': 0.0141,'Small Intestine': 0.0025,'Gallbladder': 0.0012},
    '40+': {'Lung and Bronchus': 0.1154, 'Colon and Rectum': 0.0808,'Pancreas': 0.0304,
                 'Liver and intrahepatic bile duct': 0.0211,'Urinary bladder': 0.0419,
                 'Esophagus': 0.0095,'Kidney/renal pelvis': 0.0358,
                 'Stomach': 0.015,'Head&Neck': 0.0314,'Small Intestine': 0.0033,'Gallbladder': 0.0011},
    '50+': {'Lung and Bronchus': 0.1745, 'Colon and Rectum': 0.1106,'Pancreas': 0.0448,
                 'Liver and intrahepatic bile duct': 0.0313,'Urinary bladder': 0.0631,
                 'Esophagus': 0.0141,'Kidney/renal pelvis': 0.0476,
                 'Stomach': 0.0212,'Head&Neck': 0.0439,'Small Intestine': 0.0075,'Gallbladder': 0.0040},
    '65+': {'Lung and Bronchus': 0.2937, 'Colon and Rectum': 0.1582,'Pancreas': 0.0738,
                 'Liver and intrahepatic bile duct': 0.0438,'Urinary bladder': 0.112,
                 'Esophagus': 0.0214,'Kidney/renal pelvis': 0.0625,
                 'Stomach': 0.0327,'Head&Neck': 0.0562,'Small Intestine': 0.0107,'Gallbladder': 0.0066}
}




# Define the calculation function
def calculate_ppv(sensitivity, specificity, prevalence):
    sensitivity = sensitivity / 100
    specificity = specificity / 100
    ppv = (sensitivity * (prevalence/100)) / ((sensitivity * (prevalence/100)) + ((1 - specificity) * (1 - (prevalence/100))))
    return ppv*100

# Create the plot and show individual tumors and the basket on the specificity curves
def create_plot(sensitivity, specificities, selected_tumors, tumor_prevalences):
    prevalence_range = np.linspace(0, 1.5, 100)
    fig, ax = plt.subplots()

    # Calculate the combined prevalence for the selected basket of tumors
    basket_prevalence = sum(tumor_prevalences[tumor] for tumor in selected_tumors)

    # Plot the PPV curves for each specificity
    for specificity in specificities:
        ppv_values = [calculate_ppv(sensitivity, specificity, p) for p in prevalence_range]
        ax.plot(prevalence_range, ppv_values, label=f'Specificity {specificity}%')

        # Mark the individual tumors on the curve
        for tumor in selected_tumors:
            tumor_ppv = calculate_ppv(sensitivity, specificity, tumor_prevalences[tumor])
            ax.plot(tumor_prevalences[tumor], tumor_ppv, 'o', label=f'{tumor} (PPV {tumor_ppv:.2f}%)')

        # Mark the basket on the curve
        basket_ppv = calculate_ppv(sensitivity, specificity, basket_prevalence)
        ax.plot(basket_prevalence, basket_ppv, 'X', markersize=10, label=f'Basket (PPV {basket_ppv:.2f}%)')

    plt.title('PPV vs. Prevalence for Different Specificities')
    plt.xlabel('Prevalence, %')
    plt.ylabel('PPV, %')
    # Place the legend below the plot
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True, ncol=1)
    plt.grid(True)
    plt.show()
    return fig

# Streamlit widgets for input
sensitivity = st.slider('Tier 1 Sensitivity (%)', min_value=0.0, max_value=100.0, value=99.0, step=0.1)
# Streamlit widget for inputting specificities as a comma-separated list
specificity_string = st.text_input('Specificities (%)', placeholder='Enter specificities as a comma-separated list, e.g., 95, 97.5, 99', help="Input specificities as a comma-separated list without spaces, such as '95,97.5,99'.")

# Process the input string to create a list of specificities as floats
specificities = [float(spec.strip()) for spec in specificity_string.split(',')] if specificity_string else []

# Optionally display the processed specificities to the user for verification
st.write("Processed specificities:", specificities)


# Dropdown to select age group
age_group = st.selectbox('Select Age Group', list(age_group_prevalences.keys()))

# Multi-select for choosing tumors based on selected age group
selected_tumors = st.multiselect('Select Tumors for Basket', list(age_group_prevalences[age_group].keys()))

# Generate the plot with the selected tumors and basket
tumor_prevalences = age_group_prevalences[age_group]  # Prevalences for the selected age group
fig = create_plot(sensitivity, specificities, selected_tumors, tumor_prevalences)

# Display the plot
st.pyplot(fig)

# Custom title with HTML and Markdown
st.markdown("<h1 style='text-align: center;'>Confusion Matrix for Tier 1</h1>", unsafe_allow_html=True)



# Assume tumor_prevalences and selected_tumors are defined elsewhere in your code

# Function to display the confusion matrix with annotations for multiple specificities
def display_confusion_matrix(sensitivity, specificities, basket_prevalence, total_population):
    for spec in specificities:
        disease_cases = total_population * (basket_prevalence/100)
        tp = (sensitivity/100) * disease_cases
        fn = disease_cases - tp
        tn = (spec/100) * (total_population - disease_cases)
        fp = (total_population - disease_cases) - tn
        ppv = tp / (tp + fp) if tp + fp > 0 else 0
        npv = tn / (tn + fn) if tn + fn > 0 else 0
              
        # Create the 2x2 table with annotations
        confusion_matrix = {
            'Cancer': [f"TP={tp:.0f}", f"FN={fn:.0f}"],
            'Non-Cancer': [f"FP={fp:.0f}", f"TN={tn:.0f}"],
            'PPV / NPV': [f"PPV={ppv:.2%}", f"NPV={npv:.2%}"]
        }

        # Convert the dictionary to a DataFrame
        confusion_matrix_df = pd.DataFrame(confusion_matrix, index=['Test Result Positive', 'Test Result Negative']) 

        # Display the specificity and the DataFrame
        st.markdown(f"### Confusion Matrix for Specificity: {spec:.2f}%")
        st.dataframe(confusion_matrix_df, height=150)

# Calculate basket_prevalence outside the function
basket_prevalence = sum(tumor_prevalences[tumor] for tumor in selected_tumors)
total_population = 100000  # Example population size for testing

# Sensitivity and specificities should come from user input or predefined values

# Now call the function to display the confusion matrices
display_confusion_matrix(sensitivity, specificities, basket_prevalence, total_population)

# Custom title with HTML and Markdown for Tier 2
st.markdown("<h1 style='text-align: center;'>Confusion Matrix for Tier 2 (Reflex testing)</h1>", unsafe_allow_html=True)

# Function to display the confusion matrix for tier 1 and return PPVs and total positives for tier 2
def calculate_tier1(sensitivity, specificities, basket_prevalence, total_population):
    tier1_results = []
    for spec in specificities:
        # Calculate the actual numbers
        disease_cases = total_population * (basket_prevalence/100)
        tp = (sensitivity/100) * disease_cases
        fn = disease_cases - tp
        tn = (spec/100) * (total_population - disease_cases)
        fp = (total_population - disease_cases) - tn

        # Calculate PPV and NPV
        ppv = tp / (tp + fp) if tp + fp > 0 else 0
        npv = tn / (tn + fn) if tn + fn > 0 else 0

        # Save the results for tier 2 calculations
        tier1_results.append({'specificity': spec, 'ppv': ppv, 'total_positives': tp + fp})
    return tier1_results

# Function to display the confusion matrix for tier 2
def display_reflex_test_matrix(tier2_sensitivity, tier2_specificity, tier1_ppv, total_positives):
    # The prevalence for tier 2 is the PPV from tier 1
    prevalence_tier2 = tier1_ppv
    total_population_tier2 = total_positives

    # Calculate the actual numbers for tier 2
    disease_cases_tier2 = total_population_tier2 * (prevalence_tier2/100)
    tp_tier2 = (tier2_sensitivity/100) * disease_cases_tier2
    fn_tier2 = disease_cases_tier2 - tp_tier2
    tn_tier2 = (tier2_specificity/100) * (total_population_tier2 - disease_cases_tier2)
    fp_tier2 = (total_population_tier2 - disease_cases_tier2) - tn_tier2

    # Create and display the 2x2 table for tier 2
    confusion_matrix_tier2 = pd.DataFrame({
        'Cancer': [f"TP={tp_tier2:.0f}", f"FN={fn_tier2:.0f}"],
        'Non-Cancer': [f"FP={fp_tier2:.0f}", f"TN={tn_tier2:.0f}"],
    }, index=['Test Result Positive', 'Test Result Negative'])
    
    st.dataframe(confusion_matrix_tier2)


# Display the sliders for reflex test specificity and sensitivity
st.markdown("## Reflex Test Parameters")
tier2_sensitivity = st.slider('Reflex Test Sensitivity (%)', min_value=0.0, max_value=100.0, value=99.0, step=0.1)
tier2_specificity = st.slider('Reflex Test Specificity (%)', min_value=0.0, max_value=100.0, value=99.0, step=0.1)

# Calculate tier 1 and get results for tier 2
tier1_results = calculate_tier1(sensitivity, specificities, basket_prevalence, total_population)

# Display a title for reflex test matrices
st.markdown("## Reflex Test Matrices")

# Loop through tier 1 results to display reflex test matrices
for result in tier1_results:
    st.markdown(f"### Reflex Test Matrix for Initial Specificity: {result['specificity']:.2f}%")
    display_reflex_test_matrix(tier2_sensitivity / 100, tier2_specificity / 100, result['ppv'], result['total_positives'])
