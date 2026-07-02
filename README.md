# 🚀 NASA Capillary Cup Engineering Suite

An interactive fluid dynamics simulator built to showcase microgravity wicking kinetics, the **Concus-Finn stability condition**, and material surface behavior of the famous zero-gravity coffee cup used aboard the International Space Station (ISS).

## 🌌 Project Background & History
In microgravity, liquids do not pour; they ball up due to surface tension and float away, presenting severe spill and inhalation hazards for astronauts. To solve this problem, NASA astronaut **Dr. Donald Pettit**, alongside fluid physicists **Dr. Mark Weislogel**, **Paul Concus**, and **Robert Finn**, co-invented the **NASA Capillary Cup**.

By utilizing a sharp geometric wedge profile, the cup exploits the **Concus-Finn condition**:
$$\theta + \alpha < 90^\circ$$
*(Where $\theta$ is the fluid contact angle and $\alpha$ is the wedge half-angle)*

This creates a powerful capillary pressure differential that naturally drives the liquid along the channel directly to the user's lips—completely eliminating the need for a straw or a closed bladder pouch in space.

---

## 🛠️ App Architecture (3-Block Modular Design)
The software is engineered in a clean, production-ready 3-block pipeline within `app.py`:
1. **Block 1: Core Configurations & Physics Engine** — Manages basic setups, dependency mapping, and fluid constant registries.
2. **Block 2: Layout Tabs & Dynamic UI Rendering** — Handles user override sliders, calculates Washburn kinetics, renders the interactive animation stream, and populates the telemetry dashboard.
3. **Block 3: Backend Engine Diagnostics** — Processes and pipes mathematical pipeline validation logs away from the main UI thread.

---

## 🔬 Features & Simulation Capabilities
*   **Dynamic Kinetics Canvas:** Models actual Washburn velocity parameters. Highly viscous liquids like Cooking Oil wick visibly slower than low-viscosity Coffee.
*   **Real-time Physics Overrides:** Manual sliders let you manipulate surface tension, wetting contact angles, and dynamic drag on the fly.
*   **Concus-Finn Safety Tripwire:** The rendering engine automatically triggers a fluid flow collapse sequence if your custom angles violate the microgravity geometric boundaries.
*   **Peak Telemetry Dashboard:** Generates accurate mathematical output logs mapping out peak Pascal pressure constraints at the wedge lip.

---

## 🚀 Quick Local Deployment
Ensure you have Python installed, then clone the repository and initialize the dependencies:

```bash
git clone https://github.com
cd YOUR_REPO_NAME
pip install -r requirements.txt
streamlit run app.py
```

---

## 📜 Credits & Acknowledgments
*   **Lead Software Developer:** Developed and engineered by **Srinivasta**.
*   **Invention & Physics Concept:** Built upon the pioneering aerospace hardware co-invented by Astronaut **Dr. Donald Pettit** and fluid physicist **Dr. Mark Weislogel**.
*   **Mathematical Foundations:** Derived from the foundational zero-G wedge stability equations established by **Paul Concus** and **Robert Finn**.
*   **Agency Support:** Conceptual models and telemetry references provided courtesy of the National Aeronautics and Space Administration (**NASA**).
