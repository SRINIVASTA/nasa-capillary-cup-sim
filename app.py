# ==============================================================================
# BLOCK 1: CORE CONFIGURATIONS & PHYSICS ENGINE
# ==============================================================================
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Configure page metadata and application window parameters
st.set_page_config(page_title="NASA Capillary Cup Simulators", layout="wide")
st.title("🚀 NASA Capillary Cup Engineering Suite")

# Render structural background context and historic documentation
st.markdown("""
### 🌌 Engineering Background: The NASA Capillary Cup
In microgravity, liquids do not pour; they ball up due to surface tension and float away, presenting severe spill and inhalation hazards for astronauts. 
To solve this, astronaut Don Pettit co-invented the **NASA Capillary Cup**. 

By utilizing a sharp geometric wedge profile, the cup exploits the **Concus-Finn condition** ($\theta + \alpha < 90^\circ$, where $\theta$ is the contact angle and $\alpha$ is the wedge half-angle). 
This creates a powerful capillary pressure differential that naturally drives the liquid along the channel directly to the user's lips—completely eliminating the need for a straw or a closed bladder pouch in space.
""")

# Establish fundamental multi-fluid baseline property registry
beverage_properties = {
    "Coffee": {"surface_tension": 0.073, "contact_angle": 20, "viscosity": 0.001, "color": "#6f4e37"},
    "Fruit Juice": {"surface_tension": 0.060, "contact_angle": 35, "viscosity": 0.003, "color": "#ff7f27"},
    "Cooking Oil": {"surface_tension": 0.032, "contact_angle": 12, "viscosity": 0.050, "color": "#e0c068"}
}

# Core material performance lookup matrix
materials = {
    "Coated Polymer (NASA Choice)": {"contact_angle": 10, "color": "green", "style": "-"},
    "Standard Flight Aluminum": {"contact_angle": 40, "color": "blue", "style": "--"},
    "Hydrophobic Glass Coating": {"contact_angle": 80, "color": "orange", "style": "-."},
    "Teflon-Coated Surface (Hydrophobic)": {"contact_angle": 105, "color": "red", "style": ":"}
}

# ==============================================================================
# BLOCK 2: LAYOUT TABS & DYNAMIC UI RENDERING (ALL PLOTS & UI)
# ==============================================================================
tab1, tab2 = st.tabs(["🌊 Dynamic Fluid Simulator", "🔬 Material Comparison Matrix"])

# --- TAB 1: DYNAMIC ANIMATION VIEW ---
with tab1:
    st.header("Fluid Advancing & Sipping Simulation")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        SELECTED_BEVERAGE = st.selectbox("Select Baseline Fluid Template", list(beverage_properties.keys()))
    
    fluid = beverage_properties[SELECTED_BEVERAGE]
    
    st.markdown("#### 🛠️ Manual Physics Overrides")
    col_s1, col_s2, col_s3 = st.columns(3)
    
    with col_s1:
        sigma = st.slider("Surface Tension (N/m)", 0.010, 0.100, fluid["surface_tension"], 0.001, help="Force per unit length acting at the fluid interface.")
    with col_s2:
        theta_deg = st.slider("Fluid Contact Angle (degrees)", 0, 110, fluid["contact_angle"], 1, help="Angle where the liquid interface meets the solid cup surface.")
    with col_s3:
        mu_m_pa = st.slider("Viscosity (mPa·s)", 0.5, 100.0, float(fluid["viscosity"] * 1000), 0.5, help="Fluid internal friction/resistance to flow.")
    
    # Structural conversions and math processing mapped out from inputs
    mu = mu_m_pa / 1000.0
    theta_rad = np.radians(theta_deg)
    cup_half_angle_deg = 45 

    is_geometry_safe = (cup_half_angle_deg + theta_deg) < 90
    
    if is_geometry_safe:
        st.success(f"📐 Concus-Finn Stability Check: PASS (Total Wedge + Wetting Angle: {cup_half_angle_deg + theta_deg}°). Capillary flow is physically stable.")
    else:
        st.error(f"📐 Concus-Finn Stability Check: FAIL (Total Wedge + Wetting Angle: {cup_half_angle_deg + theta_deg}°). Hydrophobic properties will cause flow collapse!")

    base_power = (0.073 * np.cos(np.radians(20))) / 0.001
    current_power = (sigma * np.cos(theta_rad)) / mu if np.cos(theta_rad) > 0 else 0.001
    
    if current_power > 0:
        wicking_end_frame = int(max(10, min(95, 25 * (base_power / current_power))))
    else:
        wicking_end_frame = 95

    steps = 120
    y_coords = np.linspace(0, 10, steps)
    channel_widths = np.linspace(0.015, 0.002, steps)
    cos_clamped = max(0.0, np.cos(theta_rad))
    capillary_pressures = (2 * sigma * cos_clamped) / channel_widths

    df = pd.DataFrame({
        'Cup_Height_m': y_coords * 0.01, 
        'Channel_Width_m': channel_widths,
        'Capillary_Pressure_Pa': capillary_pressures
    })
    
    st.download_button(
        label="📊 Download Telemetry CSV Configuration",
        data=df.to_csv(index=False),
        file_name=f"custom_space_cup_telemetry.csv",
        mime="text/csv"
    )

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle(f"NASA Capillary Cup: {SELECTED_BEVERAGE} Custom Dynamics (Zero-G)", fontsize=14, fontweight='bold')

    ax1.set_xlim(-0.01, 0.01)
    ax1.set_ylim(0, 10)
    ax1.set_ylabel("Height of Cup (y) -> Path to Lip", fontsize=10)
    ax1.set_title("Fluid Advancing Up Sharp Corner")
    ax1.plot(-channel_widths/2, y_coords, 'black', lw=2, label="Cup Wall")
    ax1.plot(channel_widths/2, y_coords, 'black', lw=2)

    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, max(capillary_pressures) + 10 if max(capillary_pressures) > 0 else 50)
    ax2.set_xlabel("Height along Cup Wall (y)", fontsize=10)
    ax2.set_ylabel("Capillary Pressure (Pascals)", fontsize=10)
    ax2.set_title("Geometric Pressure Build-up")
    
    pressure_line, = ax2.plot([], [], color='red', lw=2, label="Pressure")
    sip_indicator = ax1.text(0, 9, "", color="red", fontsize=12, fontweight="bold", ha="center")

    fluid_container = []

    def update(frame):
        if len(fluid_container) > 0:
            fluid_container.remove()
            fluid_container.clear()
            
        if not is_geometry_safe:
            current_y, current_widths, p_y, p_press = [], [], [], []
            sip_indicator.set_text("FLOW COLLAPSED: REPELLED")
        elif frame < 100:
            sip_indicator.set_text("")
            progress_ratio = min(frame / wicking_end_frame, 1.0)
            fluid_index = int(progress_ratio * (steps - 1))
            
            current_y = y_coords[:fluid_index+1]
            current_widths = channel_widths[:fluid_index+1]
            p_y = y_coords[:fluid_index+1]
            p_press = capillary_pressures[:fluid_index+1]
        else:
            sip_indicator.set_text(">>> ASTRONAUT SIPPING... <<<")
            drain_factor = (120 - frame) / 20.0  
            sip_index = int((steps - 1) * drain_factor)
            current_y = y_coords[:sip_index+1]
            current_widths = channel_widths[:sip_index+1]
            p_y, p_press = [], []

        if len(current_y) > 0:
            fill_plot = ax1.fill_betweenx(current_y, -current_widths/2, current_widths/2, color=fluid["color"], alpha=0.9)
            fluid_container.append(fill_plot)
        else:
            fill_plot = ax1.fill_betweenx([], [], [], color=fluid["color"], alpha=0)
            fluid_container.append(fill_plot)
            
        pressure_line.set_data(p_y, p_press)
        return pressure_line, fill_plot, sip_indicator

    ani = animation.FuncAnimation(fig, update, frames=steps, blit=False, interval=40, repeat=True)
    ax1.legend(loc="upper left")
    plt.tight_layout()
    
    st.components.v1.html(ani.to_jshtml(), height=530)
    plt.close()

    st.markdown("### 📊 Peak Steady-State Telemetry Dashboard")
    dash_col1, dash_col2, dash_col3 = st.columns(3)
    
    peak_pressure = capillary_pressures[-1] if is_geometry_safe else 0.0
    max_height = 10.0 if is_geometry_safe else 0.0
    channel_lip_width = channel_widths[-1] * 1000 
    
    with dash_col1:
        # FIXED: Self-calculating baseline to ensure perfect delta variance against true Coffee (68.60 Pa)
        true_coffee_base = (2 * 0.073 * np.cos(np.radians(20))) / 0.002
        st.metric(
            label="Peak Capillary Pressure (At Lip Corner)", 
            value=f"{peak_pressure:.2f} Pa",
            delta=f"{(peak_pressure - true_coffee_base):.2f} Pa vs Base Coffee" if SELECTED_BEVERAGE != "Coffee" else "Baseline Template"
        )
    with dash_col2:
        st.metric(label="Achieved Wicking Path Height", value=f"{max_height:.1f} cm")
    with dash_col3:
        st.metric(label="Narrowest Structural Critical Width", value=f"{channel_lip_width:.2f} mm")

# --- TAB 2: STATIC EVALUATION GRAPH VIEW ---
with tab2:
    st.header("Material Impact Comparison Profile")
    st.markdown("Analyzes how various structural choices affect wicking acceleration pressures for baseline Coffee.")

    surface_tension_coffee = 0.073  
    height_cm = np.linspace(0, 10, 200)
    channel_width_m = np.linspace(0.015, 0.002, 200)

    fig2, ax_mat = plt.subplots(figsize=(10, 6))
    ax_mat.set_title("Material Impact: How Cup Materials Alter Zero-G Wicking Pressure", fontsize=12, fontweight='bold')
    ax_mat.set_xlabel("Height along Cup Wall (cm)", fontsize=10)
    ax_mat.set_ylabel("Capillary Pressure (Pascals)", fontsize=10)

    for mat_name, props in materials.items():
        theta_deg_mat = props["contact_angle"]
        theta_rad_mat = np.radians(theta_deg_mat)
        pressure = (2 * surface_tension_coffee * np.cos(theta_rad_mat)) / channel_width_m
        ax_mat.plot(height_cm, pressure, label=f"{mat_name} ({theta_deg_mat} deg)", 
                 color=props["color"], linestyle=props["style"], lw=2.5)

    ax_mat.axhline(0, color='black', linestyle='-', alpha=0.5, label="Zero Net Flow Boundary")
    ax_mat.set_xlim(0, 10)
    ax_mat.grid(True, linestyle="--", alpha=0.5)
    ax_mat.legend(loc="upper left", frameon=True, shadow=True)

    ax_mat.text(1, -25, "NEGATIVE PRESSURE:\nTeflon repels liquid.\nCoffee forms a ball\nand floats away.", color="red", fontsize=9, fontweight="bold")
    ax_mat.text(5, 50, "POSITIVE PRESSURE:\nCoated Polymer draws\nfluid instantly up\nto the rim.", color="green", fontsize=9, fontweight="bold")

    plt.tight_layout()
    st.pyplot(fig2)
    plt.close()

# ==============================================================================
# BLOCK 3: BACKEND ENGINE MATHEMATICAL TRANSFORMATIONS & TELEMETRY REGISTRY
# ==============================================================================
def run_telemetry_diagnostics(fluid_name, p_tension, p_angle, p_viscosity):
    """
    Calculates numerical matrices for automated pipeline logging.
    Keeps the background calculations cleanly separated from UI rendering loops.
    """
    profile_data = {
        "Logged Fluid Model": fluid_name,
        "Surface Energy Coefficient": p_tension,
        "Wetting Equilibrium Angle": p_angle,
        "Dynamic Friction Drag (Pa·s)": p_viscosity,
        "Calculated Concus-Finn Delta": 90 - (45 + p_angle)
    }
    return profile_data

# Execute verification logging cycle in the background
diagnostics_log = run_telemetry_diagnostics(SELECTED_BEVERAGE, sigma, theta_deg, mu)
