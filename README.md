# NonInteractingTanks-
# OpenModelica Python GUI – Two Connected Tanks

## 📌 Project Description

This project integrates an **OpenModelica simulation model** with a **Python-based GUI application**.

The goal is to:

1. Compile a Modelica model (`TwoConnectedTanks`) into an executable.
2. Build a Python GUI that allows users to run the simulation with custom parameters.

---

## 🧠 Model Overview

The model represents **two non-interacting tanks** connected in series.
The system simulates fluid flow dynamics using differential equations.

The model was developed and compiled using **OpenModelica**.

---

## 🛠 Technologies Used

* Python 3.10+
* PyQt6 (GUI framework)
* OpenModelica
* Windows 10/11

---

## 📂 Project Structure

```
NonInteractingTanks/
│
├── app.py                          # Python GUI application
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
│
├── bin/                            # OpenModelica runtime DLLs (IMPORTANT)
│
└── NonInteractingTanks.TwoConnectedTanks/
    ├── TwoConnectedTanks.exe       # Model executable
    ├── TwoConnectedTanks.bat       # Launcher script (used by GUI)
    ├── TwoConnectedTanks_res.mat   # Simulation output
    ├── *.json / *.bin / *.data     # Supporting files
```

---

## ⚙️ How the System Works

1. The Modelica model is compiled into an executable (`.exe`) using OpenModelica.
2. A `.bat` file is generated to properly run the executable with required libraries.
3. The Python GUI:

   * Accepts user input (start time, stop time)
   * Runs the `.bat` file using `subprocess`
   * Displays execution logs and results

---

## 🚀 How to Run the Application

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Step 2: Run the GUI

```bash
python app.py
```

---

### Step 3: Use the GUI

1. Click **Browse**
2. Select:

```
NonInteractingTanks.TwoConnectedTanks/TwoConnectedTanks.bat
```

3. Enter:

   * Start Time (e.g., `0`)
   * Stop Time (e.g., `4`)

4. Click **Run Simulation**

---

## ⚠️ Input Constraints

The application enforces the condition:

```
0 <= start time < stop time < 5
```

Invalid inputs will show an error message.

---

## 📊 Output

* Simulation results are stored in:

  ```
  TwoConnectedTanks_res.mat
  ```
* Execution logs are displayed inside the GUI.

---

## ❗ Important Notes

* Always select the `.bat` file (not `.exe`) in the GUI.
* The `bin/` folder must be present for the executable to run.
* Do not delete supporting files inside the model folder.

---

## 🧩 OOP Design

The application is implemented using object-oriented programming:

* `SimulationRunnerApp` class manages UI and execution logic
* Functions are modular and reusable

---

## 📈 Evaluation Criteria Coverage

| Criteria            | Status |
| ------------------- | ------ |
| Code Quality (PEP8) | ✅      |
| Documentation       | ✅      |
| User Experience     | ✅      |
| OOP Implementation  | ✅      |

---

## 👤 Author

Golla Mahathi

---

## 📬 Submission

The project is submitted via GitHub as per FOSSEE guidelines.
