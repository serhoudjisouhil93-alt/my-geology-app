import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import io

st.set_page_config(page_title="GéoMap SBAA", layout="centered")

st.title("🗺️ Isopach Map Generator")
st.markdown("Version 2.0 - Professional Contour Mode")

# --- SIDEBAR: SAMPLE DATA ---
st.sidebar.header("Sample Data")
sample_data = {
    'Puits': ['SBAA-1', 'DECH-1', 'BDW-1', 'ODZ-1', 'OTRT-1', 'LT-1bis', 'OTLA-1', 'MGR-1'],
    'X': [80, 20, 65, 60, 45, 25, 15, 85],
    'Y': [85, 90, 65, 50, 45, 25, 10, 40],
    'Epais': [70, 68, 48, 185, 188, 173, 54, 253]
}
df_sample = pd.DataFrame(sample_data)

def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    return output.getvalue()

st.sidebar.download_button(
    label="📥 Download Sample Excel",
    data=to_excel(df_sample),
    file_name='sample_well_data.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)

# --- MAIN APP ---
uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("File loaded successfully!")
    
    try:
        x, y, z = df['X'], df['Y'], df['Epais']
        
        # INCREASED BUFFER: Extending the map 20 units beyond wells (approx. "2cm" scale)
        margin = 20 
        xi, yi = np.mgrid[x.min()-margin:x.max()+margin:500j, y.min()-margin:y.max()+margin:500j]
        
        zi = griddata((x, y), z, (xi, yi), method='cubic')

        fig, ax = plt.subplots(figsize=(10, 8))
        
        # NO COLORS: Using only contour lines as requested
        contours = ax.contour(xi, yi, zi, levels=15, colors='black', linewidths=0.8)
        
        # Adding labels to the contour lines (Crucial for "Interpretation")
        ax.clabel(contours, inline=True, fontsize=8, fmt='%1.0f')
        
        # Plot well locations
        ax.scatter(x, y, color='red', marker='o', s=50, label='Wells')
        
        # Better Labels for Interpretation
        for i, txt in enumerate(df['Puits']):
            ax.annotate(f"{txt}\n({z[i]}m)", (x[i], y[i]), 
                        xytext=(5, 5), textcoords='offset points',
                        fontsize=9, fontweight='bold')

        ax.set_title("Carte Isopache - Interpretation Mode", fontsize=14)
        ax.set_xlabel("Eastings (X)")
        ax.set_ylabel("Northings (Y)")
        ax.grid(True, linestyle='--', alpha=0.5)
        
        st.pyplot(fig)
        
        st.info("💡 Note: Colors were removed and boundaries extended per Professor's feedback.")

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("💡 Hint: Use the sidebar to download sample data if you don't have a file ready.")
