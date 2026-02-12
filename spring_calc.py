import streamlit as st
import math

st.set_page_config(page_title="Escapement Spring Calculator", layout="wide")
st.title("Escapement Spring Calculator")

# Constants
E = 200e9  # Young's modulus (Pa) for blue-tempered steel
DENSITY_STEEL = 7850  # kg/m³

# Title
st.markdown("### Interactive Spring Design for Escapement Prototype")

# ============ SYSTEM CONFIGURATION ============
st.markdown("---")
st.markdown("#### System Configuration")
col1_sys, col2_sys= st.columns(2)

with col1_sys:
    gear_ratio = st.number_input(
        "Gear Ratio (Barrel → Balance Torque Multiplication)",
        value=6.6,
        step=0.1,
        min_value=1.0,
        max_value=20.0,
        key="gear_ratio"
    )

    friction_loss_pct = st.number_input(
        "Estimated Friction Loss (%)",
        value=25.0,
        step=1.0,
        min_value=0.0,
        max_value=100.0,
        key="friction_loss"
    ) / 100.0

with col2_sys:
    I_g_mm2 = st.number_input(
        "Balance Moment of Inertia (g·mm², from SolidWorks)",
        value=8941.6,
        key="I"
    )

    bal_mass = st.number_input(
        "Mass of Balance (g)",
        value=13.23,
        key="bal_mass"
    )

I_kg_m2 = I_g_mm2 * 1e-9

# ============ MAINSPRING INPUTS ============
st.markdown("---")
st.markdown("#### Spring Parameters")
col1_main, col1_hair = st.columns(2)

with col1_main:
    t_m_mm = st.number_input(
        "Mainspring Thickness (mm)",
        value=0.2,
        step=0.01,
        min_value=0.05,
        max_value=0.3,
        key="t_m"
    )

    b_m_mm = st.number_input(
        "Mainspring Width/Height (mm)",
        value=1.5,
        step=0.1,
        min_value=0.5,
        max_value=10.0,  # Updated max_value to float
        key="b_m"
    )

    L_mm = st.number_input(
        "Mainspring Length (mm)",
        value=2000.0,
        step=1.0,
        min_value=300.0,
        max_value=3000.0,
        key="L_mm"
    )

# ============ HAIRSPRING INPUTS ============
with col1_hair:
    t_hs_mm = st.number_input(
        "Hairspring Thickness (mm)",
        value=0.2,
        step=0.01,
        min_value=0.02,
        max_value=0.5,
        key="t_hs"
    )

    h_hs_mm = st.number_input(
        "Hairspring Width/Height (mm)",
        value=2.0,
        step=0.1,
        min_value=0.4,
        max_value=3.0,
        key="h_hs"
    )

    L_hs_mm = st.number_input(
        "Hairspring Length (mm)",
        value=700,
        step=10,
        min_value=200,
        max_value=2000,
        key="L_hs"
    )

# Convert to SI units
t_m = t_m_mm * 1e-3
b_m = b_m_mm * 1e-3
t_hs = t_hs_mm * 1e-3
h_hs = h_hs_mm * 1e-3
L_hs = L_hs_mm * 1e-3
L_m = L_mm * 1e-3

# ============ CALCULATIONS ============
st.markdown("---")
st.markdown("#### Calculated Results")

# Mainspring calculations
kappa_m = (E * b_m * (t_m ** 3)) / (12 * L_m)
tau_peak = kappa_m * 2 * math.pi * 1000  # mNm
tau_avg = (kappa_m * math.pi * 1000) * (1 - friction_loss_pct)  # mNm
tau_balance = tau_avg * gear_ratio  # mNm

# Hairspring calculations
kappa_hs = (E * h_hs * (t_hs ** 3)) / (12 * L_hs)
f_hz = math.sqrt(kappa_hs / I_kg_m2) / (2 * math.pi)

# Amplitude calculation
theta_rad = (tau_balance / 1000) / kappa_hs
theta_deg = theta_rad * 180 / math.pi

# Hairspring torque (based on amplitude)
tau_hs_peak = kappa_hs * theta_rad  # N·m

# Hairspring mass
vol_hs = h_hs * t_hs * L_hs
mass_hs_g = vol_hs * DENSITY_STEEL * 1000

# Display results in organized sections
col_result_1, col_result_2, col_result_3 = st.columns(3)

with col_result_1:
    st.markdown("#### Mainspring")
    st.metric("κ_m (N·m/rad)", f"{kappa_m:.6f}")
    st.metric("Peak Torque (mNm)", f"{tau_peak:.2f}")
    st.metric("Avg Torque (mNm)", f"{tau_avg:.2f}")
    st.metric("Balance Torque (mNm)", f"{tau_balance:.2f}")

with col_result_2:
    st.markdown("#### Hairspring")
    st.metric("κ_hs (N·m/rad)", f"{kappa_hs:.6f}")
    st.metric("Natural Frequency (Hz)", f"{f_hz:.2f}")
    st.metric("Max Torque (mNm)", f"{tau_hs_peak * 1000:.2f}")
    st.metric("Mass (g)", f"{mass_hs_g:.2f}")
    
    # Check if mass is reasonable
    if mass_hs_g > bal_mass * 0.1:  # 10% of balance
        st.warning(f"⚠️ Hairspring mass is {mass_hs_g/bal_mass*100:.0f}% of balance—may affect I")

with col_result_3:
    st.markdown("#### System Performance")
    st.metric("Balance Amplitude (deg)", f"{theta_deg:.0f}°")
    st.metric("Amplitude (rad)", f"{theta_rad:.3f}")
    
    # Amplitude feedback
    if 250 <= theta_deg <= 350:
        st.success(f"✓ Amplitude in target range (250-350°)")
    elif theta_deg < 250:
        st.warning(f"⚠️ Amplitude too low ({theta_deg:.0f}°)—increase mainspring or reduce hairspring κ")
    else:
        st.warning(f"⚠️ Amplitude too high ({theta_deg:.0f}°)—reduce mainspring or increase hairspring κ")

# ============ ADJUSTMENT GUIDANCE ============
st.markdown("---")
st.markdown("## Quick Adjustment Guide")

guidance_col1, guidance_col2 = st.columns(2)

with guidance_col1:
    st.markdown("""
    **To INCREASE amplitude:**
    - Thicken mainspring
    - Widen mainspring
    - Thin hairspring
    
    **To DECREASE amplitude:**
    - Thin mainspring
    - Narrow mainspring
    - Thicken hairspring
    - Lengthen hairspring
    """)

with guidance_col2:
    st.markdown("""
    **To INCREASE frequency:**
    - Thicken hairspring (faster oscillation)
    - Shorten hairspring
    - Widen hairspring
    
    **To DECREASE frequency:**
    - Thin hairspring
    - Lengthen hairspring
    - Increase balance mass
    """)

# ============ FORMULA REFERENCE ============
st.markdown("---")
st.markdown("## Formula Reference")

formula_expander = st.expander("Click to view formulas")

with formula_expander:
    st.markdown("""
    #### Mainspring Constant (κ_m)
    κ_m = (E × b_m × t_m³) / (12 × L_m)
    
    - E = 200 GPa (Young's modulus for blue-tempered steel)
    - b_m = width (m)
    - t_m = thickness (m) — **cubed, so thickness has huge effect**
    - L_m = length (m)
    
    #### Peak Torque (full 1 rotation = 2π rad)
    τ_peak = κ_m × 2π × 1000
    
    #### Average Torque (mid-run at π rad)
    τ_avg = κ_m × π × 1000
    
    #### Torque at Balance
    τ_balance = τ_avg × gear_ratio
    
    #### Hairspring Constant (κ_hs)
    κ_hs = (E × h_hs × t_hs³) / (12 × L_hs)
    
    **Same formula as mainspring!**
    
    #### Natural Frequency
    f = √(κ_hs / I) / (2π)
    
    - I = balance moment of inertia (from SolidWorks)
    - **Frequency is independent of mainspring strength**
    
    #### Balance Amplitude
    θ_max (rad) = τ_balance / κ_hs
    θ_max (deg) = θ_max (rad) × 180/π

    #### Hairspring Max Torque
    τ_hs_max = κ_hs × θ_max
    
    #### Hairspring Mass
    mass = volume × density = (h_hs × t_hs × L_hs) × 7850 kg/m³
    """)

st.markdown("---")
st.markdown("*Prototype for escapement testing — evaluates different movements and gear ratios*")