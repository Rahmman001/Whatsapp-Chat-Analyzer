# Chatalyze 💬

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Chatalyze** is a premium, client-side WhatsApp chat analytics dashboard designed with an Apple-inspired **Aurora Dark** aesthetic. It provides secure, local, and visually stunning insights into your chat histories.

✨ **[Live Demo Link](https://whatsapp-chat-analyzer-jmraadfzxo7vih3qztyzv6.streamlit.app/)**

---

## 🌌 The Design System: Aurora Dark

Inspired by modern Apple Vision Pro and macOS designs, Chatalyze features a cinematic user interface:
* **Interactive Aurora Background**: A slowly spinning conic-gradient disk combined with shifting radial color overlays (deep purple, ocean blue, and indigo).
* **Shimmering Typography**: Dynamic gradient-flowing headers that smoothly transition across the color spectrum.
* **Bento Glassmorphism**: Hover-glow metric cards (`box-shadow` scaling) and frosted pill navigation tabs.
* **Flawless UI Integration**: Seamless, custom CSS styling paired with a JavaScript DOM MutationObserver to override native Streamlit limits and prevent overlapping elements.

---

## 🚀 Key Features

### 1. Temporal & Engagement Distribution
* **Monthly Macro Trend**: Track chat volumes month-over-month to view long-term interaction patterns.
* **Daily Micro Trend**: Spot short-term fluctuations and communication surges.
* **Operational Heatmaps**: Multi-dimensional heatmaps showing communication density across hours of the day and days of the week.

### 2. Lexical & Semantic Footprint
* **Term Frequency Graphs**: Isolate the most frequently used words by any participant or overall.
* **Semantic Word Cloud**: A visual cluster showing the core subjects of conversation.
* **Emoji Distribution**: A responsive Altair donut chart reflecting emoji habits, displaying symbols floating outside slice segments.

### 3. Group Chat Dynamics (Macro View)
* **Top Contributors**: Absolute contribution charts comparing messaging volumes per person.
* **Share of Voice**: Interactive table mapping exact percentage weight of messages with styled gradient scales.

---

## 🛡️ Privacy First (Zero Data Telemetry)

Your privacy is paramount. **Chatalyze runs entirely locally**:
* No chats are ever uploaded to any database or external server.
* The analysis engine preprocesses and parses raw WhatsApp `.txt` exports purely in-memory using python.
* Zero logging, zero telemetry.

---

## 🛠️ Installation & Setup

### Prerequisites
Ensure you have **Python 3.8+** installed on your system.

### 1. Clone the repository
```bash
git clone https://github.com/Rahmman001/Whatsapp-Chat-Analyzer.git
cd Whatsapp-Chat-Analyzer
```

### 2. Set up a virtual environment
```bash
# Create environment
python3 -m venv .venv

# Activate environment (Mac/Linux)
source .venv/bin/activate

# Activate environment (Windows)
.venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the dashboard
```bash
streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser to experience Chatalyze!

---

## 📖 How to Export Your WhatsApp Chat

To analyze a conversation, export it as a text file from your device:

### iOS (Apple)
1. Open the target WhatsApp chat.
2. Tap the contact name or group subject at the top.
3. Scroll down and select **Export Chat**.
4. Choose **Without Media** (this analyzer uses text telemetry).
5. Share or save the `.zip` file, extract the `.txt` file, and drop it into the uploader.

### Android
1. Open the target WhatsApp chat.
2. Tap the **Three Dots Menu** (top-right corner).
3. Select **More** > **Export Chat**.
4. Choose **Without Media**.
5. Save the generated `.txt` file and upload it directly.

---

## 🧪 Tech Stack & Libraries
* **Framework**: [Streamlit](https://streamlit.io/) (for building local-first interactive Python webapps)
* **Data Processing**: [Pandas](https://pandas.pydata.org/) (for chat parsing, formatting, and mathematical operations)
* **Visualizations**: [Matplotlib](https://matplotlib.org/) & [Seaborn](https://seaborn.pydata.org/) (tailored for dark background themeing)
* **Interactive Charts**: [Altair](https://altair-viz.github.io/) (for responsive donut charts)
* **Text Extraction**: [URLExtract](https://github.com/lrei/urlextract), [WordCloud](https://github.com/amueller/word_cloud), [Emoji](https://github.com/carpedm20/emoji)
* **Styling & Overrides**: CSS3 Custom Properties & JavaScript MutationObserver

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.
