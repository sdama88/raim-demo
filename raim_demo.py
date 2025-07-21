import streamlit as st
import os

st.set_page_config(
    page_title="Redsand RAIM™ Demo",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Sidebar Branding ---
with st.sidebar:
    if os.path.exists("redsand_logo.png"):
        st.image("redsand_logo.png", width=180)
    else:
        st.warning("Logo not found. Place 'redsand_logo.png' in the same folder.")
    st.markdown("## **RAIM™: Redsand Demo Interface**")
    st.markdown("Welcome to the simulation demo of Redsand's AI inference control system.")
    st.markdown("---")
    st.markdown("### RedBox Information")
    st.text("RedBox ID: RBX-9931-AIO")
    st.text("Location: London Edge Site")
    st.text("Specs: 8x L40S (48GB, 300W) | 1x AMD EPYC (96-core)")
    st.text("RAM: 1.5TB DDR5 ECC")
    st.text("Storage: 4x 3.84TB NVMe + 2x 16TB SATA SSD")
    st.text("Network: 2x 100GbE uplinks + 1x 1GbE Mgmt port")
    st.text("Uptime: 123 days")

# --- RedBox Configuration Selection ---
st.subheader("Select RedBox Configuration")
redbox_option = st.selectbox(
    "Choose RedBox Node:",
    [
        "RedBox One - 8x L40S",
        "RedBox Max - 64x H100 SXM",
        "RedBox Ultra - 360x H100 SXM",
        "Custom (coming soon)"
    ]
)
st.markdown(f"**Selected Configuration:** {redbox_option}")

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
st.code("Allocated: 8x L40S (48GB, 300W) | 1x AMD EPYC (96-core) | 1.5TB DDR5 ECC RAM | 4x NVMe + 2x SATA SSD")
st.success("Environment ready")

# Live Status Dashboard
st.header("4. Live Status Dashboard")
st.metric("Latency (ms)", "21.3")
st.metric("Health Status", "Healthy")
st.metric("Version", "v1.2.0")

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

# Model Scaling and GPU Allocation
st.header("9. Model Scaling")
st.markdown("**On-prem RedBox deployment – full GPU allocation only**")
auto_select = st.checkbox("Auto-select hardware based on model")

model_gpu_mapping = {
    "LLaMA 3 70B": ("H100", 4),
    "Mistral 7B": ("L40S", 1),
    "Mixtral 8x7B": ("H100", 4),
    "Falcon 40B": ("H100", 3),
    "Phi-2": ("L40S", 1),
    "Gemma 2B": ("L40S", 1),
    "Gemma 7B": ("L40S", 1),
    "Command R": ("L40S", 1),
    "OpenChat": ("L40S", 1),
    "LLaMA 2 7B": ("L40S", 1),
    "LLaMA 2 13B": ("H100", 2),
    "LLaMA 3 8B": ("L40S", 1),
    "Qwen 14B": ("H100", 2),
    "Command-R 35B": ("H100", 4),
    "Whisper Large-v2": ("L40S", 1)
}

def is_model_supported_on_redbox(model, redbox):
    h100_required = model_gpu_mapping.get(model, ("", 0))[0] == "H100"
    redbox_is_l40s = "RedBox One" in redbox
    return not (h100_required and redbox_is_l40s)

if auto_select and model_option in model_gpu_mapping:
    gpu_type, gpu_count = model_gpu_mapping[model_option]
    st.success(f"Auto-selected {gpu_count}x {gpu_type} based on {model_option}")
else:
    st.info(f"No model selected or auto-selection disabled. Using default hardware: {default_gpu_count}x {default_gpu_type}")
    gpu_type = "L40S"
    st.text("GPU Type: L40S")
    gpu_count = default_gpu_count
    st.text(f"GPU Count: {gpu_count}")

model_count = st.slider("Concurrent Models", 1, 20, 2)
auto_scale = st.checkbox("Enable Auto-Scaling")

max_models = gpu_count * 2
st.info(f"With {gpu_count}x {gpu_type}, system supports up to {max_models} models concurrently.")

if model_count > max_models:
    st.warning("Model count exceeds available GPU capacity. Expect degraded performance.")
else:
    st.success("Current load is within GPU limits.")

if not is_model_supported_on_redbox(model_option, redbox_option):
    st.error(f"Warning: {model_option} requires H100 GPUs and is not supported on {redbox_option}.")

st.progress(min(model_count / max_models, 1.0))

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
        st.metric("GPU Temperature (°C)", "63.4")
        st.metric("Fan Speed (%)", "71")
        st.metric("Power Usage (W)", "276")
        st.metric("Disk Usage", "82%")
        st.metric("CPU Load", "41.8%")
        st.metric("Memory Usage", "24.7 GB / 32 GB")

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
