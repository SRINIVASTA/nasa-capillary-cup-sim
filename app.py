import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Page layout configuration
st.set_page_config(page_title="NASA Capillary Cup Simulators", layout="wide")
st.title("🚀 NASA Capillary Cup Engineering Suite")

# Create the two tabs
tab1, tab2 = st.tabs(["🌊 Dynamic Fluid Simulator", "🔬 Material Comparison Matrix"])

# ==============================================================================
# TAB 1: DYNAMIC FLUID SIMULATOR (REAL KINETICS ANIMATION)
# ==============================================================================
with tab1:
    st.header("Fluid Advancing & Sipping Simulation")
    st.markdown("This simulation models fluid kinetics. Highly viscous liquids like Cooking Oil wick visibly slower.")
    
    SELECTED_BEVERAGE = st.selectbox("Select Beverage Type", ["Coffee", "Fruit Juice", "Cooking Oil"])
    
    # Enhanced Database of fluid properties including viscosity (Pascal-seconds)
    beverage_properties = {
        "Coffee": {"surface_tension": 0.073, "contact_angle": 20, "viscosity": 0.001, "color": "#6f4e37"},
        "Fruit Juice": {"surface_tension": 0.060, "contact_angle": 35, "viscosity": 0.003, "color": "#ff7f27"},
        "Cooking Oil": {"surface_tension": 0.032, "contact_angle": 12, "viscosity": 0.050, "color": "#e0c068"}
    }

    fluid = beverage_properties[SELECTED_BEVERAGE]
    sigma = fluid["surface_tension"]
    theta_deg = fluid["contact_angle"]
    theta_rad = np.radians(theta_deg)
    mu = fluid["viscosity"]
    cup_half_angle_deg = 45 

    # Concus-Finn Geometry Check
    is_geometry_safe = (cup_half_angle_deg + theta_deg) < 90
    
    if is_geometry_safe:
        st.success(f"📐 Geometry Check: PASS (Total Angle: {cup_half_angle_deg + theta_deg}°). Fluid wicks perfectly.")
    else:
        st.error(f"📐 Geometry Check: FAIL (Total Angle: {cup_half_angle_deg + theta_deg}°). Capillary flow fails; spill risk!")

    # Calculate real Washburn-derived kinetics factor
    # Higher tension + lower viscosity = faster wicking speed
    wicking_power = (sigma * np.cos(theta_rad)) / mu
    
    # Scale total frames required based on a baseline (Coffee = fast, Oil = slow)
    # Coffee (~68.5) takes 25 frames. Cooking Oil (~0.62) takes 100+ frames.
    if SELECTED_BEVERAGE == "Coffee":
        wicking_end_frame = 25
    elif SELECTED_BEVERAGE == "Fruit Juice":
        wicking_end_frame = 55
    else:  # Cooking Oil
        wicking_end_frame = 100

    steps = 120
    y_coords = np.linspace(0, 10, steps)
    channel_widths = np.linspace(0.015, 0.002, steps)
    capillary_pressures = (2 * sigma * np.cos(theta_rad)) / channel_widths

    # Create CSV data download link
    df = pd.DataFrame({
        'Cup_Height_m': y_coords * 0.01, 
        'Channel_Width_m': channel_widths,
        'Capillary_Pressure_Pa': capillary_pressures
    })
    
    st.download_button(
        label="📊 Download Telemetry CSV",
        data=df.to_csv(index=False),
        file_name=f"space_cup_{SELECTED_BEVERAGE.lower().replace(' ', '_')}_telemetry.csv",
        mime="text/csv"
    )

    # Plot Construction for Streamlit Native rendering
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle(f"NASA Capillary Cup: {SELECTED_BEVERAGE} Dynamics (Zero-G)", fontsize=14, fontweight='bold')

    ax1.set_xlim(-0.01, 0.01)
    ax1.set_ylim(0, 10)
    ax1.set_ylabel("Height of Cup (y) -> Path to Lip", fontsize=10)
    ax1.set_title("Fluid Advancing Up Sharp Corner")
    ax1.plot(-channel_widths/2, y_coords, 'black', lw=2, label="Cup Wall")
    ax1.plot(channel_widths/2, y_coords, 'black', lw=2)

    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, max(capillary_pressures) + 10)
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
            
        # Standard Dynamic Wicking Phase (Frames 0 to 99)
        if frame < 100:
            sip_indicator.set_text("")
            
            # Map the timeline frame to fluid specific speed
            progress_ratio = min(frame / wicking_end_frame, 1.0)
            fluid_index = int(progress_ratio * (steps - 1))
            
            # Liquid is at full capacity resting at the lip if done wicking early
            current_y = y_coords[:fluid_index+1]
            current_widths = channel_widths[:fluid_index+1]
            p_y = y_coords[:fluid_index+1]
            p_press = capillary_pressures[:fluid_index+1]
            
        # Astronaut Sipping Phase (Frames 100 to 119)
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

    # Generate and render animation loop smoothly using Streamlit Component HTML container
    ani = animation.FuncAnimation(fig, update, frames=steps, blit=False, interval=40, repeat=True)
    ax1.legend(loc="upper left")
    plt.tight_layout()
    
    # Display the animation via its Javascript HTML converter
    st.components.v1.html(ani.to_jshtml(), height=600)
    plt.close()

# ==============================================================================
# TAB 2: MATERIAL COMPARISON MATRIX
# ==============================================================================
with tab2:
    st.header("Material Impact Comparison Profile")
    st.markdown("Analyzes how various structural choices affect wicking acceleration pressures for baseline Coffee.")

    materials = {
        "Coated Polymer (NASA Choice)": {"contact_angle": 10, "color": "green", "style": "-"},
        "Standard Flight Aluminum": {"contact_angle": 40, "color": "blue", "style": "--"},
        "Hydrophobic Glass Coating": {"contact_angle": 80, "color": "orange", "style": "-."},
        "Teflon-Coated Surface (Hydrophobic)": {"contact_angle": 105, "color": "red", "style": ":"}
    }

    surface_tension_coffee = 0.073  
    height_cm = np.linspace(0, 10, 200)
    channel_width_m = np.linspace(0.015, 0.002, 200)

    fig2, ax_mat = plt.subplots(figsize=(10, 6))
    ax_mat.set_title("Material Impact: How Cup Materials Alter Zero-G Wicking Pressure", fontsize=12, fontweight='bold')
    ax_mat.set_xlabel("Height along Cup Wall (cm)", fontsize=10)
    ax_mat.set_ylabel("Capillary Pressure (Pascals)", fontsize=10)

    for mat_name, props in materials.items():
        theta_deg = props["contact_angle"]
        theta_rad = np.radians(theta_deg)
        pressure = (2 * surface_tension_coffee * np.cos(theta_rad)) / channel_width_m
        ax_mat.plot(height_cm, pressure, label=f"{mat_name} ({theta_deg} deg)", 
                 color=props["color"], linestyle=props["style"], lw=2.5)

    ax_mat.axhline(0, color='black', linestyle='-', alpha=0.5, label="Zero Net Flow Boundary")
    ax_mat.set_xlim(0, 10)
    ax_mat.grid(True, linestyle="--", alpha=0.5)
    ax_mat.legend(loc="upper left", frameon=True, shadow=True)

    ax_mat.text(1, -25, "NEGATIVE PRESSURE:\nTeflon repels liquid.\nCoffee forms a ball\nand floats away.", color="red", fontsize=9, fontweight="bold")
    ax_mat.text(5, 50, "POSITIVE PRESSURE:\nCoated Polymer draws\nfluid instantly up\nto the rim.", color="green", fontsize=9, fontweight="bold")

    plt.tight_layout()
    
    # Display the static evaluation chart using native streamlit wrapper
    st.pyplot(fig2)
    plt.close()
