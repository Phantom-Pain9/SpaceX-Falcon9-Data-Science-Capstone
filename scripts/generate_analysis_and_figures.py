import os
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, accuracy_score

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 1.0

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(base_dir, 'data')
fig_dir = os.path.join(base_dir, 'figures')
os.makedirs(fig_dir, exist_ok=True)

# 1. Load Data
df2 = pd.read_csv(os.path.join(data_dir, 'dataset_part_2.csv'))
df3 = pd.read_csv(os.path.join(data_dir, 'dataset_part_3.csv'))
df_geo = pd.read_csv(os.path.join(data_dir, 'spacex_launch_geo.csv'))
df_dash = pd.read_csv(os.path.join(data_dir, 'spacex_launch_dash.csv'))
df_sql = pd.read_csv(os.path.join(data_dir, 'Spacex.csv'))

print("Data loaded successfully.")

# Palette: Green for success (1), Red/Orange for failure (0)
custom_palette = {0: "#e74c3c", 1: "#2ecc71"}

# ==========================================
# FIGURE 1: Flight Number vs Launch Site
# ==========================================
plt.figure(figsize=(12, 6), dpi=300)
sns.scatterplot(
    data=df2, x="FlightNumber", y="LaunchSite", hue="Class",
    palette=custom_palette, s=120, alpha=0.9, edgecolor='black', linewidth=0.8
)
plt.title("Flight Number vs. Launch Site by Landing Outcome", fontsize=15, fontweight='bold', pad=15)
plt.xlabel("Flight Number", fontsize=12, fontweight='bold')
plt.ylabel("Launch Site", fontsize=12, fontweight='bold')
plt.legend(title="Outcome", labels=["Failure (0)", "Success (1)"], loc="lower right", frameon=True)
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "01_flight_vs_launchsite.png"))
plt.close()

# ==========================================
# FIGURE 2: Payload Mass vs Launch Site
# ==========================================
plt.figure(figsize=(12, 6), dpi=300)
sns.scatterplot(
    data=df2, x="PayloadMass", y="LaunchSite", hue="Class",
    palette=custom_palette, s=120, alpha=0.9, edgecolor='black', linewidth=0.8
)
plt.title("Payload Mass (kg) vs. Launch Site by Landing Outcome", fontsize=15, fontweight='bold', pad=15)
plt.xlabel("Payload Mass (kg)", fontsize=12, fontweight='bold')
plt.ylabel("Launch Site", fontsize=12, fontweight='bold')
plt.legend(title="Outcome", labels=["Failure (0)", "Success (1)"], loc="lower right", frameon=True)
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "02_payload_vs_launchsite.png"))
plt.close()

# ==========================================
# FIGURE 3: Success Rate by Orbit Type
# ==========================================
plt.figure(figsize=(12, 6), dpi=300)
orbit_success = df2.groupby('Orbit')['Class'].mean().reset_index()
orbit_success = orbit_success.sort_values(by='Class', ascending=False)
bars = plt.bar(orbit_success['Orbit'], orbit_success['Class'] * 100, color='#3498db', edgecolor='#2980b9', width=0.6)
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 1.5, f'{yval:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
plt.title("Landing Success Rate by Mission Orbit Type", fontsize=15, fontweight='bold', pad=15)
plt.xlabel("Orbit Type", fontsize=12, fontweight='bold')
plt.ylabel("Success Rate (%)", fontsize=12, fontweight='bold')
plt.ylim(0, 115)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "03_success_rate_by_orbit.png"))
plt.close()

# ==========================================
# FIGURE 4: Flight Number vs Orbit Type
# ==========================================
plt.figure(figsize=(12, 6), dpi=300)
sns.scatterplot(
    data=df2, x="FlightNumber", y="Orbit", hue="Class",
    palette=custom_palette, s=120, alpha=0.9, edgecolor='black', linewidth=0.8
)
plt.title("Flight Number vs. Orbit Type by Landing Outcome", fontsize=15, fontweight='bold', pad=15)
plt.xlabel("Flight Number", fontsize=12, fontweight='bold')
plt.ylabel("Orbit Type", fontsize=12, fontweight='bold')
plt.legend(title="Outcome", labels=["Failure (0)", "Success (1)"], loc="lower right", frameon=True)
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "04_flight_vs_orbit.png"))
plt.close()

# ==========================================
# FIGURE 5: Payload Mass vs Orbit Type
# ==========================================
plt.figure(figsize=(12, 6), dpi=300)
sns.scatterplot(
    data=df2, x="PayloadMass", y="Orbit", hue="Class",
    palette=custom_palette, s=120, alpha=0.9, edgecolor='black', linewidth=0.8
)
plt.title("Payload Mass (kg) vs. Orbit Type by Landing Outcome", fontsize=15, fontweight='bold', pad=15)
plt.xlabel("Payload Mass (kg)", fontsize=12, fontweight='bold')
plt.ylabel("Orbit Type", fontsize=12, fontweight='bold')
plt.legend(title="Outcome", labels=["Failure (0)", "Success (1)"], loc="lower right", frameon=True)
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "05_payload_vs_orbit.png"))
plt.close()

# ==========================================
# FIGURE 6: Yearly Launch Success Trend
# ==========================================
df2['Year'] = pd.to_datetime(df2['Date']).dt.year
yearly_success = df2.groupby('Year')['Class'].mean().reset_index()

plt.figure(figsize=(12, 6), dpi=300)
plt.plot(yearly_success['Year'], yearly_success['Class'] * 100, marker='o', linewidth=3, markersize=8, color='#27ae60')
for _, row in yearly_success.iterrows():
    plt.text(row['Year'], row['Class']*100 + 3, f"{row['Class']*100:.1f}%", ha='center', va='bottom', fontsize=10, fontweight='bold')
plt.title("SpaceX Falcon 9 Landing Success Rate Over Time (2010 - 2020)", fontsize=15, fontweight='bold', pad=15)
plt.xlabel("Year", fontsize=12, fontweight='bold')
plt.ylabel("Success Rate (%)", fontsize=12, fontweight='bold')
plt.ylim(-5, 115)
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "06_yearly_success_trend.png"))
plt.close()

# ==========================================
# FIGURE 7: Plotly Dash Equivalents (Pie & Scatter)
# ==========================================
# Pie Chart 1: Success by Site (ALL)
plt.figure(figsize=(10, 6), dpi=300)
site_success = df_dash[df_dash['class'] == 1]['Launch Site'].value_counts()
colors = ['#2ecc71', '#3498db', '#f1c40f', '#e67e22']
plt.pie(site_success, labels=site_success.index, autopct='%1.1f%%', startangle=140, colors=colors,
        explode=[0.05]*len(site_success), shadow=True, textprops={'fontsize': 11, 'fontweight': 'bold'})
plt.title("Total Successful Launches by Launch Site (All Sites)", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "07_dash_pie_all_sites.png"))
plt.close()

# Pie Chart 2: Success vs Failure for KSC LC-39A
plt.figure(figsize=(8, 6), dpi=300)
ksc_data = df_dash[df_dash['Launch Site'] == 'KSC LC-39A']['class'].value_counts()
plt.pie(ksc_data, labels=['Success (1)', 'Failure (0)'], autopct='%1.1f%%', startangle=90,
        colors=['#2ecc71', '#e74c3c'], explode=[0.05, 0], shadow=True, textprops={'fontsize': 11, 'fontweight': 'bold'})
plt.title("Launch Outcome Breakdown for KSC LC-39A (Success Rate: 76.9%)", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "08_dash_pie_ksc.png"))
plt.close()

# Scatter Plot: Payload vs Class colored by Booster Version Category
plt.figure(figsize=(12, 6), dpi=300)
sns.scatterplot(
    data=df_dash, x="Payload Mass (kg)", y="class", hue="Booster Version Category",
    s=120, alpha=0.9, edgecolor='black', linewidth=0.8, style="Booster Version Category"
)
plt.title("Correlation Between Payload Mass (kg) and Success for All Sites", fontsize=14, fontweight='bold')
plt.xlabel("Payload Mass (kg)", fontsize=12, fontweight='bold')
plt.ylabel("Class (0: Failure, 1: Success)", fontsize=12, fontweight='bold')
plt.yticks([0, 1], ["Failure (0)", "Success (1)"])
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', frameon=True)
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "09_dash_scatter_payload.png"))
plt.close()

print("Visualizations generated successfully.")

# ==========================================
# 2. SQL QUERIES & EXECUTION
# ==========================================
conn = sqlite3.connect(os.path.join(data_dir, "my_data1.db"))
# Clean column names in Spacex.csv
df_sql.columns = [c.strip().replace(' ', '_').replace('(', '').replace(')', '').replace('-', '_') for c in df_sql.columns]
df_sql.to_sql("SPACEXTBL", conn, if_exists="replace", index=False)

queries = {
    "Task 1: Unique Launch Sites":
        "SELECT DISTINCT Launch_Site FROM SPACEXTBL;",
    
    "Task 2: Launch Sites Beginning with 'CCA'":
        "SELECT Launch_Site FROM SPACEXTBL WHERE Launch_Site LIKE 'CCA%' LIMIT 5;",
    
    "Task 3: Total Payload Mass Carried by NASA (CRS)":
        "SELECT SUM(PAYLOAD_MASS__KG_) AS Total_Payload_Mass_KG FROM SPACEXTBL WHERE Customer = 'NASA (CRS)';",
    
    "Task 4: Average Payload Mass for Booster Version F9 v1.1":
        "SELECT AVG(PAYLOAD_MASS__KG_) AS Average_Payload_Mass_KG FROM SPACEXTBL WHERE Booster_Version LIKE 'F9 v1.1%';",
    
    "Task 5: Date of First Successful Ground Pad Landing":
        "SELECT MIN(Date) AS First_Successful_Ground_Pad_Landing_Date FROM SPACEXTBL WHERE Landing_Outcome = 'Success (ground pad)';",
    
    "Task 6: Drone Ship Boosters with Payload between 4000 and 6000 kg":
        "SELECT Booster_Version, PAYLOAD_MASS__KG_ FROM SPACEXTBL WHERE Landing_Outcome = 'Success (drone ship)' AND PAYLOAD_MASS__KG_ BETWEEN 4000 AND 6000;",
    
    "Task 7: Total Successful and Failure Mission Outcomes":
        "SELECT Mission_Outcome, COUNT(*) AS Total_Count FROM SPACEXTBL GROUP BY Mission_Outcome;",
    
    "Task 8: Boosters Carrying Maximum Payload Mass":
        "SELECT Booster_Version, PAYLOAD_MASS__KG_ FROM SPACEXTBL WHERE PAYLOAD_MASS__KG_ = (SELECT MAX(PAYLOAD_MASS__KG_) FROM SPACEXTBL);",
    
    "Task 9: Drone Ship Failures in 2015":
        "SELECT Booster_Version, Launch_Site, Landing_Outcome, Date FROM SPACEXTBL WHERE Landing_Outcome = 'Failure (drone ship)' AND Date LIKE '%2015%';",
    
    "Task 10: Rank Count of Landing Outcomes (2010-06-04 to 2017-03-20)":
        "SELECT Landing_Outcome, COUNT(*) AS Outcome_Count FROM SPACEXTBL WHERE Date BETWEEN '2010-06-04' AND '2017-03-20' GROUP BY Landing_Outcome ORDER BY Outcome_Count DESC;"
}

sql_results_text = []
for name, q in queries.items():
    res = pd.read_sql(q, conn)
    sql_results_text.append(f"### {name}\n**Query:**\n```sql\n{q}\n```\n**Result:**\n{res.to_markdown(index=False)}\n")

with open(os.path.join(fig_dir, "sql_query_results.md"), "w") as f:
    f.write("\n".join(sql_results_text))

print("SQL Queries executed and saved.")

# ==========================================
# 3. MACHINE LEARNING MODEL EVALUATION
# ==========================================
X = df3.copy()
Y = df2['Class'].to_numpy()

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, Y_train, Y_test = train_test_split(X_scaled, Y, test_size=0.2, random_state=2)

# 1. Logistic Regression
lr_params = {'C': [0.01, 0.1, 1], 'penalty': ['l2'], 'solver': ['lbfgs']}
lr = LogisticRegression(random_state=2)
lr_cv = GridSearchCV(lr, lr_params, cv=10)
lr_cv.fit(X_train, Y_train)
lr_test_acc = lr_cv.score(X_test, Y_test)

# 2. Support Vector Machine
svm_params = {'kernel': ('linear', 'rbf', 'poly', 'sigmoid'), 'C': np.logspace(-3, 3, 5), 'gamma': np.logspace(-3, 3, 5)}
svm = SVC(random_state=2)
svm_cv = GridSearchCV(svm, svm_params, cv=10)
svm_cv.fit(X_train, Y_train)
svm_test_acc = svm_cv.score(X_test, Y_test)

# 3. Decision Tree
tree_params = {
    'criterion': ['gini', 'entropy'],
    'splitter': ['best', 'random'],
    'max_depth': [2*n for n in range(1, 10)],
    'max_features': ['sqrt', 'log2', None],
    'min_samples_leaf': [1, 2, 4],
    'min_samples_split': [2, 5, 10]
}
tree = DecisionTreeClassifier(random_state=2)
tree_cv = GridSearchCV(tree, tree_params, cv=10)
tree_cv.fit(X_train, Y_train)
tree_test_acc = tree_cv.score(X_test, Y_test)

# 4. K-Nearest Neighbors
knn_params = {'n_neighbors': list(range(1, 11)), 'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'], 'p': [1, 2]}
knn = KNeighborsClassifier()
knn_cv = GridSearchCV(knn, knn_params, cv=10)
knn_cv.fit(X_train, Y_train)
knn_test_acc = knn_cv.score(X_test, Y_test)

models_summary = pd.DataFrame({
    'Model': ['Logistic Regression', 'Support Vector Machine', 'Decision Tree', 'K-Nearest Neighbors'],
    'Best CV Training Accuracy': [lr_cv.best_score_, svm_cv.best_score_, tree_cv.best_score_, knn_cv.best_score_],
    'Test Accuracy': [lr_test_acc, svm_test_acc, tree_test_acc, knn_test_acc],
    'Best Hyperparameters': [str(lr_cv.best_params_), str(svm_cv.best_params_), str(tree_cv.best_params_), str(knn_cv.best_params_)]
})

print(models_summary.to_string())

# ==========================================
# FIGURE 10: Model Accuracy Comparison Bar Chart
# ==========================================
plt.figure(figsize=(10, 6), dpi=300)
x_pos = np.arange(len(models_summary['Model']))
width = 0.35

plt.bar(x_pos - width/2, models_summary['Best CV Training Accuracy'] * 100, width, label='Train (CV) Accuracy', color='#3498db', edgecolor='#2980b9')
plt.bar(x_pos + width/2, models_summary['Test Accuracy'] * 100, width, label='Test Accuracy', color='#2ecc71', edgecolor='#27ae60')

for i in range(len(x_pos)):
    plt.text(x_pos[i] - width/2, models_summary['Best CV Training Accuracy'][i] * 100 + 1.5, f"{models_summary['Best CV Training Accuracy'][i]*100:.2f}%", ha='center', fontsize=10, fontweight='bold')
    plt.text(x_pos[i] + width/2, models_summary['Test Accuracy'][i] * 100 + 1.5, f"{models_summary['Test Accuracy'][i]*100:.2f}%", ha='center', fontsize=10, fontweight='bold')

plt.xlabel('Classification Algorithm', fontsize=12, fontweight='bold')
plt.ylabel('Accuracy (%)', fontsize=12, fontweight='bold')
plt.title('Comparison of Machine Learning Classification Models', fontsize=14, fontweight='bold', pad=15)
plt.xticks(x_pos, models_summary['Model'], fontsize=11)
plt.ylim(0, 115)
plt.legend(loc='lower right', frameon=True)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "10_model_accuracy_comparison.png"))
plt.close()

# ==========================================
# FIGURE 11: Confusion Matrix for Best Model (Decision Tree & Logistic Regression)
# ==========================================
yhat = tree_cv.predict(X_test)
cm = confusion_matrix(Y_test, yhat)

plt.figure(figsize=(8, 6), dpi=300)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False,
            annot_kws={'size': 16, 'fontweight': 'bold'},
            xticklabels=['Predicted Fail (0)', 'Predicted Success (1)'],
            yticklabels=['Actual Fail (0)', 'Actual Success (1)'])
plt.title('Confusion Matrix - Best Classification Model (Accuracy: 83.33%)', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Predicted Label', fontsize=12, fontweight='bold')
plt.ylabel('True Label', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "11_confusion_matrix.png"))
plt.close()

print("All ML evaluation complete.")
