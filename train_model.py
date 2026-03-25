import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier

# LOAD DATA
df = pd.read_csv("PCOS_data.csv")

# CLEAN COLUMN NAMES
df.columns = df.columns.str.strip()
df.columns = df.columns.str.replace(r'\s+', ' ', regex=True)

# DROP USELESS COLUMNS
df = df.drop(columns=["Sl. No", "Patient File No.", "Unnamed: 44"])

# HANDLE MISSING VALUES
df["Fast food (Y/N)"] = df["Fast food (Y/N)"].fillna(df["Fast food (Y/N)"].mode()[0])
df["Marraige Status (Yrs)"] = df["Marraige Status (Yrs)"].fillna(df["Marraige Status (Yrs)"].mean())

# TYPE CONVERSION
df["Fast food (Y/N)"] = df["Fast food (Y/N)"].astype(int)
df["Reg.Exercise(Y/N)"] = df["Reg.Exercise(Y/N)"].astype(int)

# CLEAN NUMERIC COLUMNS
df["II beta-HCG(mIU/mL)"] = df["II beta-HCG(mIU/mL)"].astype(str).str.replace(r'\.$', '', regex=True)
df["AMH(ng/mL)"] = df["AMH(ng/mL)"].astype(str).str.replace(r'\.$', '', regex=True)

df["II beta-HCG(mIU/mL)"] = pd.to_numeric(df["II beta-HCG(mIU/mL)"], errors='coerce')
df["AMH(ng/mL)"] = pd.to_numeric(df["AMH(ng/mL)"], errors='coerce')

# FILL REMAINING MISSING VALUES
df = df.fillna(df.mean())

# SELECT FEATURES
basic_features = [
    "Age (yrs)", "Weight (Kg)", "BMI", "Cycle(R/I)",
    "Cycle length(days)", "Weight gain(Y/N)",
    "hair growth(Y/N)", "Skin darkening (Y/N)", "Hip(inch)"
]

X = df[basic_features]
y = df["PCOS (Y/N)"]

# TRAIN MODEL
model = RandomForestClassifier(random_state=42)
model.fit(X, y)

# SAVE MODEL
pickle.dump(model, open("basic_model.pkl", "wb"))

print("Model trained and saved!")

# ================= ADVANCED MODEL =================

adv_features = [
    "Follicle No. (R)",
    "Follicle No. (L)",
    "Skin darkening (Y/N)",
    "hair growth(Y/N)",
    "Weight gain(Y/N)",
    "AMH(ng/mL)",
    "Cycle length(days)",
    "Cycle(R/I)",
    "Weight (Kg)",
    "Age (yrs)",
    "FSH/LH",
    "BMI",
    "LH(mIU/mL)",
    "Hip(inch)",
    "TSH (mIU/L)"
]

X_adv = df[adv_features]
y = df["PCOS (Y/N)"]

adv_model = RandomForestClassifier(random_state=42)
adv_model.fit(X_adv, y)

pickle.dump(adv_model, open("adv_model.pkl", "wb"))

print("Advanced model trained and saved!")