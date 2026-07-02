# Master Thesis — UXDM

**Effect of AV Driving Behavior Customization UI on User Acceptance and Trust**

MSc thesis by Muhammed Maral (User Experience Design & Management).

## Study overview

- **Design:** N=27, within-subjects, 3 conditions — A: Functional UI, B: No UI, C: Placebo UI
- **Personality groups:** Big Five — High Openness vs. High Neuroticism
- **Measures:** UEQ-s (8-item), de Waard Acceptance Scale, slider interaction logs
- **Key finding:** The Functional UI significantly outperforms No UI on acceptance; the Placebo UI is not significantly different from the Functional UI, suggesting a possible placebo effect.

## Repository structure

| Folder | Contents |
|---|---|
| `CarMakerUI/` | Experiment UI (customtkinter, Tesla-style) controlling CarMaker via DVA. `src/ControlUI.py` (functional), `src/ControlUI_placebo.py` (placebo), `src/logger.py` (CSV event logger) |
| `collected_data/` | 34 participant session CSVs (Conditions A + B, personality-encoded) |
| `notebooks/` | Analysis notebooks (see below) |
| `scripts/` | Data preparation utilities |
| `survey_data/` | Raw survey responses (Acceptance–Trust Scale, UEQ-s) |
| `figures/` | Thesis figures and visualizations (PNG) |
| `SPSS/` | SPSS outputs (Acceptance Trust, Trust, UEQ-s) |
| `thesis/` | Thesis PDFs |

## Notebooks

- `Classification_Thesis_ML.ipynb` — ML pipeline classifying personality group (High Neuroticism–Low Openness vs. High Openness–Low Neuroticism) from slider interaction behavior. Feature engineering per slider (mean, std, min, max, range, change count), 5 models (RF, SVM, LogReg, KNN, Gradient Boosting), Leave-One-Out CV.
- `data_analysis_master_Acceptance.ipynb` — Acceptance scale analysis (written for Google Colab; paths may need adjusting)
- `data_analysis_master_UEQ.ipynb` — UEQ-s analysis (written for Google Colab; paths may need adjusting)
- `SPSS_acceptance.ipynb` — Exports acceptance results to Excel for SPSS

Run notebooks from the `notebooks/` directory; data is loaded via the relative path `../collected_data`.

## Running the experiment UI

```bash
cd CarMakerUI
pip install -r requirements.txt
python src/ControlUI.py          # functional condition
python src/ControlUI_placebo.py  # placebo condition
```

Requires a running IPG CarMaker instance (connection via [pycarmaker](https://github.com/gmnvh/pycarmaker)).

## Notes

- `scripts/interactionScore.py` and `scripts/statisticalCalculator.py` contain hardcoded/placeholder data paths — update them before running.
