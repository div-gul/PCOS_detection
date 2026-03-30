import React, { useState } from "react";
import "../styles/Input.css";

const Input = () => {
  const [formData, setFormData] = useState({
    gender: "",
    Pregnancies: "",
    Glucose: "",
    BloodPressure: "",
    SkinThickness: "",
    Insulin: "",
    BMI: "",
    DPF: "",
    Age: "",

    folR: "",
    folL: "",
    skin: "",
    hair: "",
    weight: "",
    amh: "",
    cycle: "",
    ratio: "",
    lh: "",
    fastfood: "",

    TSH: "",
    TT4: "",
    T4U: "",
    FTI: ""
  });
  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.id]: e.target.value });
  };

  const handleSubmit = async (e) => {
  e.preventDefault();

  try {
    let output = {};

    // Diabetes
    const d_res = await fetch("http://127.0.0.1:5000/predict_diabetes", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        Pregnancies: +formData.Pregnancies,
        Glucose: +formData.Glucose,
        BloodPressure: +formData.BloodPressure,
        SkinThickness: +formData.SkinThickness,
        Insulin: +formData.Insulin,
        BMI: +formData.BMI,
        DiabetesPedigreeFunction: +formData.DPF,
        Age: +formData.Age
      })
    });

    const d_json = await d_res.json();
    output.diabetes = d_json.risk_percentage;

    // PCOS
    if (formData.gender === "female") {
      const p_res = await fetch("http://127.0.0.1:5000/predict_pcos", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
          "Follicle No. (R)": +formData.folR,
          "Follicle No. (L)": +formData.folL,
          "Skin darkening (Y/N)": +formData.skin,
          "hair growth(Y/N)": +formData.hair,
          "Weight gain(Y/N)": +formData.weight,
          "AMH(ng/mL)": +formData.amh,
          "Cycle(R/I)": +formData.cycle,
          "FSH/LH": +formData.ratio,
          "LH(mIU/mL)": +formData.lh,
          "Fast food (Y/N)": +formData.fastfood
        })
      });

      const p_json = await p_res.json();
      output.pcos = p_json.risk_percentage;
    }

    // Thyroid
    const t_res = await fetch("http://127.0.0.1:5000/predict_thyroid", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        age: +formData.Age,
        sex: formData.gender === "male" ? 1 : 0,
        TSH: +formData.TSH,
        TT4: +formData.TT4,
        T4U: +formData.T4U,
        FTI: +formData.FTI
      })
    });

    const t_json = await t_res.json();
    output.thyroid = t_json.confidence;

    setResult(output);

  } catch (err) {
    alert("Server error!");
  }
};

  return (
    <div className="input-container">
      <div className="form-card">
        <h1 className="title">Hormonal Health Risk Predictor</h1>

        <form onSubmit={handleSubmit}>

          {/* Gender */}
          <div className="section">
            <h3>Basic Info</h3>
            <div className="field">
              <label>Gender</label>
              <select id="gender" onChange={handleChange}>
                <option value="">Select</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
              </select>
            </div>
          </div>

          {/* Diabetes */}
          <div className="section">
            <h3>Diabetes Inputs</h3>
            <div className="grid">

              <div className="field">
                <label>Pregnancies</label>
                <select id="Pregnancies" onChange={handleChange}>
                <option value="">Select</option>
                {[...Array(16).keys()].map((num) => (
                    <option key={num} value={num}>{num}</option>
                ))}
                </select>
              </div>

              <div className="field">
                <label>Glucose</label>
                <input type="number" id="Glucose" placeholder="70 – 140 mg/dL" onChange={handleChange}/>
              </div>

              <div className="field">
                <label>Blood Pressure</label>
                <input type="number" id="BloodPressure" placeholder="60 – 140 mmHg" onChange={handleChange}/>
              </div>

              <div className="field">
                <label>Skin Thickness</label>
                <input type="number" id="SkinThickness" placeholder="10 – 50" onChange={handleChange}/>
              </div>

              <div className="field">
                <label>Insulin</label>
                <input type="number" id="Insulin" placeholder="15 – 276" onChange={handleChange}/>
              </div>

              <div className="field">
                <label>BMI</label>
                <input type="number" id="BMI" placeholder="18.5 – 24.9" onChange={handleChange}/>
              </div>

              <div className="field">
                <label>Diabetes Pedigree</label>
                <input type="number" id="DPF" placeholder="0.1 – 2.5" onChange={handleChange}/>
              </div>

              <div className="field">
                <label>Age</label>
                <input type="number" id="Age" placeholder="10 – 100" onChange={handleChange}/>
              </div>

            </div>
          </div>

          {/* PCOS */}
          {formData.gender === "female" && (
            <div className="section">
              <h3>PCOS Inputs</h3>
              <div className="grid">

                <div className="field">
                  <label>Follicle (R)</label>
                  <input type="number" id="folR" placeholder="0 – 30" onChange={handleChange}/>
                </div>

                <div className="field">
                  <label>Follicle (L)</label>
                  <input type="number" id="folL" placeholder="0 – 30" onChange={handleChange}/>
                </div>

                <div className="field">
                  <label>Skin Darkening</label>
                  <select id="skin" onChange={handleChange}>
                    <option value="">Select</option>
                    <option value="1">Yes</option>
                    <option value="0">No</option>
                  </select>
                </div>

                <div className="field">
                  <label>Hair Growth</label>
                  <select id="hair" onChange={handleChange}>
                    <option value="">Select</option>
                    <option value="1">Yes</option>
                    <option value="0">No</option>
                  </select>
                </div>

                <div className="field">
                  <label>Weight Gain</label>
                  <select id="weight" onChange={handleChange}>
                    <option value="">Select</option>
                    <option value="1">Yes</option>
                    <option value="0">No</option>
                  </select>
                </div>

                <div className="field">
                  <label>AMH</label>
                  <input type="number" id="amh" placeholder="1 – 10" onChange={handleChange}/>
                </div>

                <div className="field">
                  <label>Cycle</label>
                  <select id="cycle" onChange={handleChange}>
                    <option value="">Select</option>
                    <option value="0">Regular</option>
                    <option value="1">Irregular</option>
                  </select>
                </div>

                <div className="field">
                  <label>FSH/LH Ratio</label>
                  <input type="number" id="ratio" placeholder="1 – 3" onChange={handleChange}/>
                </div>

                <div className="field">
                  <label>LH</label>
                  <input type="number" id="lh" placeholder="1 – 20" onChange={handleChange}/>
                </div>

                <div className="field">
                  <label>Fast Food</label>
                  <select id="fastfood" onChange={handleChange}>
                    <option value="">Select</option>
                    <option value="1">Yes</option>
                    <option value="0">No</option>
                  </select>
                </div>

              </div>
            </div>
          )}

          {/* Thyroid */}
          <div className="section">
            <h3>Thyroid Inputs</h3>
            <div className="grid">

              <div className="field">
                <label>TSH</label>
                <input type="number" id="TSH" placeholder="0.4 – 4.0" onChange={handleChange}/>
              </div>

              <div className="field">
                <label>TT4</label>
                <input type="number" id="TT4" placeholder="5 – 12" onChange={handleChange}/>
              </div>

              <div className="field">
                <label>T4U</label>
                <input type="number" id="T4U" placeholder="0.8 – 1.8" onChange={handleChange}/>
              </div>

              <div className="field">
                <label>FTI</label>
                <input type="number" id="FTI" placeholder="1 – 4" onChange={handleChange}/>
              </div>

            </div>
          </div>

          <button type="submit" className="submit-btn">
            Predict
          </button>

        </form>

        {result && (
  <div className="result-container">

    {/* Diabetes */}
    <div className="result-card">
      <h3>🩺 Diabetes</h3>
      <div className="progress-bar">
        <div
          className="progress"
          style={{ width: `${result.diabetes}%` }}
        ></div>
      </div>
      <p>{result.diabetes}% Risk</p>
    </div>

    {/* PCOS */}
    {result.pcos && (
      <div className="result-card">
        <h3>🌸 PCOS</h3>
        <p className="percentage">{result.pcos}%</p>
      </div>
    )}

    {/* Thyroid */}
    <div className="result-card">
      <h3>🧠 Thyroid</h3>
      <p className="badge">{result.thyroid}</p>
    </div>

  </div>
)}
      </div>
    </div>
  );
};

export default Input;