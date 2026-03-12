import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

st.set_page_config(page_title="GéoMap SBAA", layout="centered")

st.title("🗺️ Isopach Map Generator")
st.markdown("Upload your well data to generate a geological thickness map.")

# File uploader
uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("File loaded successfully!")
    st.write("### Preview of Well Data", df.head())

    # Map Calculation
    # Note: Ensure your Excel has columns 'X', 'Y', and 'Epais'
    try:
        x, y, z = df['X'], df['Y'], df['Epais']
        xi, yi = np.mgrid[x.min()-5:x.max()+5:300j, y.min()-5:y.max()+5:300j]
        zi = griddata((x, y), z, (xi, yi), method='cubic')

        # Plotting
        fig, ax = plt.subplots(figsize=(10, 8))
        cp = ax.contourf(xi, yi, zi, levels=20, cmap='terrain')
        plt.colorbar(cp, label='Thickness (m)')
        ax.scatter(x, y, color='red', edgecolors='white')
        
        # Add labels for wells
        for i, txt in enumerate(df['Puits']):
            ax.annotate(txt, (x[i], y[i]), fontweight='bold')

        ax.set_title("Generated Isopach Map")
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error: Make sure your columns are named 'Puits', 'X', 'Y', and 'Epais'. Details: {e}")
else:
    st.info("💡 Hint: Use the well data from your SBAA Basin table.")
