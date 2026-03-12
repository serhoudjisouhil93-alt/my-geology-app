import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import io

st.set_page_config(page_title="GéoMap SBAA", layout="centered")

st.title("🗺️ Isopach Map Generator")
st.markdown("Upload your well data to generate a geological thickness map.")

# --- NEW: SAMPLE DATA SECTION ---
st.sidebar.header("Sample Data")
sample_data = {
    'Puits': ['SBAA-1', 'DECH-1', 'BDW-1', 'ODZ-1', 'OTRT-1', 'LT-1bis', 'OTLA-1', 'MGR-1'],
    'X': [80, 20, 65, 60, 45, 25, 15, 85],
    'Y': [85, 90, 65, 50, 45, 25, 10, 40],
    'Epais': [70, 68, 48, 185, 188, 173, 54, 253]
}
df_sample = pd.DataFrame(sample_data)

# Function to convert df to excel for download
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
# -------------------------------

uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

# Use sample data if no file is uploaded (optional, or just wait for upload)
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("File loaded successfully!")
    
    try:
        x, y, z = df['X'], df['Y'], df['Epais']
        xi, yi = np.mgrid[x.min()-5:x.max()+5:300j, y.min()-5:y.max()+5:300j]
        zi = griddata((x, y), z, (xi, yi), method='cubic')

        fig, ax = plt.subplots(figsize=(10, 8))
        cp = ax.contourf(xi, yi, zi, levels=20, cmap='terrain')
        plt.colorbar(cp, label='Thickness (m)')
        ax.scatter(x, y, color='red', edgecolors='white')
        
        for i, txt in enumerate(df['Puits']):
            ax.annotate(txt, (x[i], y[i]), fontweight='bold')

        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error: Ensure columns are 'Puits', 'X', 'Y', 'Epais'. Details: {e}")
else:
    st.info("💡 Hint: Download the sample file from the sidebar to test the app!")

st.markdown("---")
st.markdown("""
**🎓 Academic Contribution** *This tool was developed by SERHOUDJI Souhil Abderrahim as a free resource for the geological community and future students. 
It is dedicated to the advancement of Digital Geosciences in Algeria.*
""")
