import streamlit as st
import os
import random

st.set_page_config(
    page_title="Redsand RAIM™ Demo",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- RedBox Configuration Selection ---
st.subheader("Select RedBox Configuration")
redbox_option = st.selectbox(
    "Choose RedBox Node:",
    [
        "RedBox One - 8x L40S",
        "RedBox Max - 64x H100 SXM",
        "RedBox Ultra - 360x H100 SXM"      
    ]
)

# Extract GPU details dynamically
gpu_info = redbox_option.split("-")[1].strip()

# --- Sidebar Branding ---
with st.sidebar:
    if os.path.exists("redsand_logo.png"):
        st.image("redsand_logo.png", width=180)
    else:
        st.warning("Logo not found. Place 'redsand_logo.png' in the same folder.")
    st.markdown("## **RAIM™: Redsand Demo Interface**")
    st.markdown("Welcome to the simulation demo of Redsand's AI Inference Platform control system.")
    st.markdown("---")
    st.markdown("### RedBox Information")
    st.text(f"GPUs: {gpu_info}")

st.markdown(f"**Selected Configuration:** {redbox_option}")

# Extract GPU details from RedBox selection
gpu_info = redbox_option.split("-")[-1].strip()
default_gpu_type = gpu_info.split()[1]
default_gpu_count = int(gpu_info.split()[0].replace("x", ""))

# Default RedBox provisioning
gpu_type = default_gpu_type
gpu_count = default_gpu_count

# --- Title with Branding ---
st.markdown("<h1 style='color:#d03d3d;'>Redsand RAIM™ Demo</h1>", unsafe_allow_html=True)
st.caption("Simulated walk-through for agentic model deployment and management at the edge.")

# Upload or Select Model
st.header("1. Upload or Select Model")
model_option = st.selectbox(
    "Choose an open-source model:",
    [
        "LLaMA 2 7B",
        "LLaMA 2 13B",
        "LLaMA 3 8B",
        "LLaMA 3 70B",
        "Mistral 7B",
        "Mixtral 8x7B",
        "Falcon 7B",
        "Falcon 40B",
        "Phi-2",
        "Command R",
        "OpenChat",
        "Gemma 2B",
        "Gemma 7B",
        "Qwen 14B",
        "Command-R 35B",
        "Whisper Large-v2",
        "CustomVision",
        "Upload your own"
    ]
)

uploaded_files = st.file_uploader(
    "Upload model weights and config files (if needed):",
    type=[".pt", ".bin", ".json", ".h5", ".onnx", ".model"],
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"Uploaded {len(uploaded_files)} files:")
    for f in uploaded_files:
        st.write(f.name)
else:
    st.info("No model files uploaded yet.")

# One Click Deploy
st.header('2. One Click "Deploy"')
if st.button("Deploy Now"):
    with st.spinner("Packaging and validating model..."):
        st.success("Model packaged successfully")
        st.info("Compatibility check passed")

# Automatic Provisioning
st.header("3. Automatic Provisioning")
st.write("Spinning up runtime environment...")
st.code(f"Allocated: {gpu_count}x {gpu_type}")
st.success("Environment ready")

# Live Status Dashboard
st.header("4. Live Status Dashboard")
base_latency = {
    "L40S": 21.3,
    "H100": 15.7
}

latency = base_latency.get(gpu_type, 25.0) + random.uniform(-2.5, 2.5)
health_status = "Healthy" if random.random() > 0.1 else "Degraded"
version = "v1.2.0"

st.metric("Latency (ms)", f"{latency:.1f}")
st.metric("Health Status", health_status)
st.metric("Version", version)

# Integrate Monitoring
st.header("5. Integrate Monitoring")
monitor_option = st.radio("Monitoring Option:", ["Basic Logs", "Custom Prometheus/Grafana", "Third-party Integration"])
if monitor_option:
    st.success(f"{monitor_option} enabled")

# Upgrade or Reset
st.header("6. Upgrade or Reset")
col1, col2 = st.columns(2)
with col1:
    new_version = st.file_uploader("Upload new model version")
    if new_version:
        st.success(f"Version {new_version.name} ready for upgrade")
with col2:
    if st.button("Reset Deployment"):
        st.warning("Deployment reset")

# SLA Monitoring in Secure Networks
st.header("7. SLA Monitoring in Secure Networks")
st.markdown("""
For deployments without direct internet access, Redsand enables SLA tracking using:
- On-prem monitoring tools
- Secure telemetry exports
- Customer-certified audit logs

All methods follow agreed integration terms and comply with secure network policies.
""")

# One Click Upgrade or Rollback
st.header("8. One Click Upgrade or Rollback")
version_select = st.selectbox("Select model version:", ["v1.2.0", "v1.1.3", "v1.0.9"])
col3, col4 = st.columns(2)
with col3:
    if st.button("Upgrade"):
        st.success(f"Upgraded to {version_select}")
with col4:
    if st.button("Rollback"):
        st.info(f"Rolled back to {version_select}")

# Model Scaling
st.header("9. Model Scaling")
st.markdown("**On-prem RedBox deployment – full GPU allocation only**")
auto_select = st.checkbox("Auto-select hardware based on model")

model_gpu_mapping = {
    "LLaMA 3 70B": ("H100", 4, 3),
    "Mistral 7B": ("L40S", 1, 200),
    "Mixtral 8x7B": ("H100", 4, 96),
    "Falcon 40B": ("H100", 3, 96),
    "Phi-2": ("L40S", 1, 200),
    "Gemma 2B": ("L40S", 1, 200),
    "Gemma 7B": ("L40S", 1, 200),
    "Command R": ("L40S", 1, 12),
    "OpenChat": ("L40S", 1, 200),
    "LLaMA 2 7B": ("L40S", 1, 200),
    "LLaMA 2 13B": ("H100", 2, 144),
    "LLaMA 3 8B": ("L40S", 1, 200),
    "Qwen 14B": ("H100", 2, 144),
    "Command-R 35B": ("H100", 4, 12),
    "Whisper Large-v2": ("L40S", 1, 400)
}

def is_model_supported_on_redbox(model, redbox):
    h100_required = model_gpu_mapping.get(model, ("", 0))[0] == "H100"
    redbox_is_l40s = "RedBox One" in redbox
    return not (h100_required and redbox_is_l40s)

if auto_select and model_option in model_gpu_mapping:
    optimal_gpu_type, optimal_gpu_count, _ = model_gpu_mapping[model_option]
    if optimal_gpu_type != default_gpu_type:
        st.warning(f"Model {model_option} is typically optimal on {optimal_gpu_count}x {optimal_gpu_type}, but using selected RedBox: {default_gpu_count}x {default_gpu_type}")
    gpu_type = default_gpu_type
    gpu_count = default_gpu_count
else:
    gpu_type = default_gpu_type
    gpu_count = default_gpu_count
    st.info(f"Using selected RedBox configuration: {gpu_count}x {gpu_type}")

model_count = st.slider("Concurrent Model Instances", 1, 20, 2)
max_models = gpu_count * 2

if model_count > max_models:
    st.warning("Model count exceeds available GPU capacity. Expect degraded performance.")
else:
    st.success("Current load is within GPU limits.")

st.progress(min(model_count / max_models, 1.0))

# RedBox Offline Mode and Hardware Stats
st.header("10. RedBox Node Details")
expand = st.expander("Show Node Hardware Telemetry")
with expand:
    offline = st.checkbox("Simulate Offline Mode")
    if offline:
        st.error("Node is currently offline. Telemetry paused.")
    else:
        st.success("Node online and responsive.")
        base_temp = 63 if gpu_type == "L40S" else 58
        st.metric("GPU Temperature (°C)", f"{base_temp + random.uniform(-2, 3):.1f}")
        st.metric("Fan Speed (%)", f"{random.randint(60, 80)}")
        st.metric("Power Usage (W)", f"{random.randint(250, 400)}")
        st.metric("Disk Usage", f"{random.randint(70, 90)}%")
        st.metric("CPU Load", f"{random.uniform(35, 55):.1f}%")
        st.metric("Memory Usage", f"{random.uniform(22, 26):.1f} GB / 32 GB")

# Security and Integration (Seldon-Aligned)
st.header("11. Security & Integration")
sec_expand = st.expander("Show Security & Integration Options")
with sec_expand:
    st.subheader("Network & Access Control")
    st.checkbox("Enable TLS/mTLS for control and data plane")
    st.checkbox("Integrate with OIDC / SSO (e.g., Keycloak, Azure AD)")
    st.checkbox("Enable Istio JWT for service mesh auth")

    st.subheader("Image & Registry Management")
    st.checkbox("Scan container images for CVEs (e.g., using Snyk)")
    st.checkbox("Mirror deployment images to internal/private registry")

    st.subheader("Logging & Audit Trails")
    st.checkbox("Enable request/response logging")
    st.checkbox("Export telemetry to ELK/S3")

    st.subheader("Runtime & Deployment Policies")
    st.checkbox("Enforce RBAC for deployment control")
    st.checkbox("Apply Kubernetes network policies")
    st.checkbox("Enable offline mode buffering with telemetry sync")

st.markdown("---")
st.caption("This simulation is for illustrative purposes only and does not represent final performance or deployment conditions.")
