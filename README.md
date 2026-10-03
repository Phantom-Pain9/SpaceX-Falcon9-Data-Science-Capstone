# 🚀 SpaceX Falcon 9 First Stage Landing Prediction
### IBM Data Science Professional Certificate - Applied Data Science Capstone Project
**Author:** Phantom Pain ([@Phantom-Pain9](https://github.com/Phantom-Pain9))  
**Repository:** [SpaceX-Falcon9-Data-Science-Capstone](https://github.com/Phantom-Pain9/SpaceX-Falcon9-Data-Science-Capstone)

---

## 📌 Executive Summary
In the commercial space launch industry, launch costs are significantly determined by rocket reusability. While traditional space agencies and commercial competitors expend rocket stages, **SpaceX reuses the first stage of the Falcon 9 rocket**, advertising launch costs of roughly **\$62 million per launch**, compared to competing commercial expendable launches that often exceed **\$165 million**.

The primary objective of this project is to develop an end-to-end data science and machine learning pipeline to **predict whether the first stage of a Falcon 9 rocket will land successfully** on an autonomous spaceport drone ship (ASDS) or ground pad (RTLS). By accurately forecasting landing outcomes, launch brokers, satellite operators, and competing aerospace firms can assess the financial viability and bidding dynamics of commercial space missions.

### Key Results Summary
- **Exploratory Data Analysis:** Heavy payloads (greater than 4,000 kg) combined with specific low-earth orbits (LEO) achieved the highest success rates. The `KSC LC-39A` launch pad exhibited the highest landing success rate (**76.9%**). Over time, first-stage recovery improved dramatically from **0% in 2010–2013** to near **100% in 2020** with the deployment of Falcon 9 Block 5 boosters.
- **Predictive Performance:** Evaluated four classification algorithms (**Logistic Regression**, **Support Vector Machine**, **Decision Tree Classifier**, and **K-Nearest Neighbors**) using 10-fold cross-validation (`GridSearchCV`).
  - **Decision Tree & Logistic Regression:** Achieved **83.33% Test Accuracy** and **84.6% – 87.7% Cross-Validation Accuracy**.
  - **Confusion Matrix:** Minimal false negatives (only 3 misclassified cases on the test split), with high recall for successful landings.

---

## 🛠️ Project Architecture & Workflow
The capstone project follows the standard Data Science Lifecycle:
1. **Data Collection (REST API & Web Scraping):** Extracted historical launch, booster, and payload records using SpaceX's official API (`v4/launches/past`) and BeautifulSoup scraping of Wikipedia Falcon 9 launch logs.
2. **Data Wrangling:** Cleaned missing values, imputed mean payload masses, defined the binary target outcome `Class` (1 for successful recovery, 0 for failure), and performed one-hot encoding across categorical variables (`Orbit`, `LaunchSite`, `LandingPad`, `Serial`), producing 83 predictive features.
3. **Exploratory Data Analysis with SQL & Visualizations:** Executed SQL queries using SQLite to analyze payload distributions, launch site frequencies, and booster version performance. Plotted categorical relationships and yearly trends using Seaborn and Matplotlib.
4. **Interactive Visual Analytics:** Created geospatial maps with Folium (marker clusters, proximity distance analysis) and developed an interactive dashboard using Plotly Dash with dynamic launch site selection and payload range sliders.
5. **Predictive Modeling & Hyperparameter Tuning:** Standardized feature matrices using `StandardScaler` and tuned hyperparameters across 4 supervised classification algorithms via `GridSearchCV`.

---

## 📂 Repository Structure
```text
SpaceX-Falcon9-Data-Science-Capstone/
├── README.md                                     # Project overview, methodology, and results
├── data/
│   ├── dataset_part_1.csv                        # Processed API data
│   ├── dataset_part_2.csv                        # Wrangled data with binary Class label
│   ├── dataset_part_3.csv                        # One-hot encoded feature matrix (83 features)
│   ├── spacex_launch_geo.csv                     # Geospatial launch coordinates dataset
│   ├── spacex_launch_dash.csv                    # Dataset used in Plotly Dash dashboard
│   ├── Spacex.csv                                # Base CSV for SQLite database
│   └── my_data1.db                              # SQLite database file containing SPACEXTBL
├── figures/                                      # High-resolution charts and map captures
│   ├── 01_flight_vs_launchsite.png
│   ├── 02_payload_vs_launchsite.png
│   ├── 03_success_rate_by_orbit.png
│   ├── 04_flight_vs_orbit.png
│   ├── 05_payload_vs_orbit.png
│   ├── 06_yearly_success_trend.png
│   ├── 07_dash_pie_all_sites.png
│   ├── 08_dash_pie_ksc.png
│   ├── 09_dash_scatter_payload.png
│   ├── 10_model_accuracy_comparison.png
│   ├── 11_confusion_matrix.png
│   ├── 12_folium_launch_sites.png
│   ├── 13_folium_marker_clusters.png
│   ├── 14_folium_distance_analysis.png
│   └── sql_query_results.md                     # Markdown summary of 10 SQL query tasks
├── notebooks/                                    # Fully executed Jupyter Notebooks with outputs
│   ├── 1_Data_Collection_API.ipynb
│   ├── 2_Data_Collection_Web_Scraping.ipynb
│   ├── 3_Data_Wrangling.ipynb
│   ├── 4_EDA_with_SQL.ipynb
│   ├── 5_EDA_with_Visualization.ipynb
│   ├── 6_Interactive_Visual_Analytics_Folium.ipynb
│   └── 7_Machine_Learning_Prediction.ipynb
├── reports/
│   └── Data Science Capstone Project Report.pdf # Final submission presentation in PDF format
└── scripts/
    ├── generate_analysis_and_figures.py          # Master analysis and visualization script
    ├── generate_folium_maps.py                   # Geospatial Folium generator and Chrome renderer
    └── spacex_dash_app.py                        # Standalone Plotly Dash interactive web app
```

---

## 📊 Exploratory Data Analysis & Visualizations

### 1. Launch Sites vs. Flight Numbers and Payloads
- **Flight Number vs. Launch Site:** Early flights (1–25) were concentrated at `CCAFS LC-40` with frequent landing failures. As flight numbers progressed, launches diversified to `VAFB SLC-4E` and `KSC LC-39A`, demonstrating substantial improvements in landing success.
- **Payload Mass vs. Launch Site:** `KSC LC-39A` handles heavy missions (up to 15,600 kg) with an outstanding success rate. `VAFB SLC-4E` focuses on polar orbits with lighter-to-medium payloads (up to 9,600 kg).

### 2. Orbit Performance
- **High-Success Orbits:** `ES-L1`, `GEO`, `HEO`, `SSO`, and `VLEO` all exhibited a **100% success rate**.
- **Challenging Orbits:** `GTO` (Geostationary Transfer Orbit) missions achieved approximately **50% success rate** due to high energy re-entry velocity and thermal stress requiring extreme deceleration.

### 3. Yearly Success Rate Progression
- From **2010 to 2013**, success rate was **0%** (experimental recovery tests).
- In **2015**, the first ground pad landing succeeded (`2015-12-22`).
- In **2016–2017**, drone ship landings matured, boosting success to **60%–80%**.
- By **2020**, with Falcon 9 Block 5 boosters, landing success reached **85%–100%**.

---

## 🗄️ SQL Analysis Highlights
Executed using SQLite against the `SPACEXTBL` table:
1. **Launch Sites:** Found 4 distinct launch sites: `CCAFS LC-40`, `VAFB SLC-4E`, `KSC LC-39A`, and `CCAFS SLC-40`.
2. **NASA Missions:** Total payload mass carried by NASA (CRS) boosters amounted to **45,596 kg**.
3. **F9 v1.1 Average Payload:** The average payload mass carried by Falcon 9 v1.1 boosters was **2,534.67 kg**.
4. **First Successful Ground Landing:** Recorded on **2015-12-22** (`Success (ground pad)`).
5. **Heavy Payloads on Drone Ships:** Boosters `F9 FT B1022`, `B1026`, `B1021.2`, and `B1031.2` successfully recovered payloads between 4,000 kg and 6,000 kg.
6. **Maximum Payload Records:** Falcon 9 Block 5 boosters carried the maximum payload of **15,600 kg** (Starlink missions).

---

## 🗺️ Geospatial & Interactive Analytics

### Folium Map Insights
- Launch sites are strategically located immediately on the coastline (`CCAFS SLC-40` is only ~0.84 km from the Atlantic Ocean) to ensure safety trajectories away from population centers and over open water.
- Proximity to rail infrastructure (~1.2 km) and highways (~0.5 km) facilitates heavy booster transport from SpaceX manufacturing facilities in Hawthorne, California.

### Plotly Dash Dashboard
The interactive dashboard (`spacex_dash_app.py`) provides:
- **Site Dropdown Selector:** Allows toggling between all sites and individual launch pads.
- **Payload Range Slider:** Dynamic filtering between 0 kg and 10,000 kg.
- **Key Findings:**
  1. `KSC LC-39A` had the largest number of successful launches (10 successes).
  2. `KSC LC-39A` also had the highest success rate (76.9%).
  3. The payload range between **2,000 kg and 5,300 kg** yielded the highest success rates.
  4. Falcon 9 **Block 5 (B5)** achieved a 100% success rate across all evaluated flights.

---

## 🤖 Predictive Machine Learning Models
Four supervised classification algorithms were trained to predict first-stage landing outcomes ($Y \in \{0, 1\}$):

| Model | Cross-Validation Accuracy (10-fold) | Test Set Accuracy | Optimal Hyperparameters |
| :--- | :---: | :---: | :--- |
| **Decision Tree Classifier** | **87.68%** | **83.33%** | `criterion='gini', max_depth=8, min_samples_leaf=2, min_samples_split=10, max_features='sqrt'` |
| **Logistic Regression** | **84.64%** | **83.33%** | `C=0.01, penalty='l2', solver='lbfgs'` |
| **Support Vector Machine (SVM)** | **84.82%** | **83.33%** | `kernel='sigmoid', C=1.0, gamma=0.0316` |
| **K-Nearest Neighbors (KNN)** | **84.82%** | **83.33%** | `n_neighbors=10, algorithm='auto', p=1` |

### Confusion Matrix Analysis
- **True Positives (Successful Landings Predicted as Success):** 12
- **True Negatives (Failed Landings Predicted as Failure):** 3
- **False Positives (Failed Landings Predicted as Success):** 3
- **False Negatives (Successful Landings Predicted as Fail):** 0
- **Sensitivity / Recall:** The model achieves 100% recall for successful landings, ensuring zero false alarms for operational reusability forecasting.

---

## 💡 Strategic Business Recommendations
1. **Competitive Launch Bidding:** Aerospace competitors must anticipate that SpaceX missions utilizing Block 5 boosters have a recovery certainty of >95%, providing SpaceX with a structural cost basis of approximately \$62M. Competitors must price below \$90M or offer high-payload single-use capabilities for specialized missions to remain competitive.
2. **Payload & Orbit Planning:** High-mass commercial payloads sent to GTO orbits face higher recovery risks; clients can leverage this data to negotiate insurance premiums and secondary payload pricing.

---

## 💻 How to Run This Project
1. **Clone the repository:**
   ```bash
   git clone https://github.com/Phantom-Pain9/SpaceX-Falcon9-Data-Science-Capstone.git
   cd SpaceX-Falcon9-Data-Science-Capstone
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Plotly Dash Application:**
   ```bash
   python scripts/spacex_dash_app.py
   ```
4. **Execute all analyses and generate figures:**
   ```bash
   python scripts/generate_analysis_and_figures.py
   python scripts/generate_folium_maps.py
   ```

---
*Created as part of the IBM Data Science Professional Certificate Capstone.*
