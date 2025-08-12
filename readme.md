
# MediSense - AI-powered Symptom Checker & Medical Assistant

![MediSense Logo](https://huggingface.co/mohsinnyz/Disease-Guider/raw/main/logo.png)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/downloads/)

## Overview

**MediSense** is an AI-powered medical assistant that helps users identify potential health conditions based on reported symptoms. Built with Streamlit, this web application uses machine learning to predict diseases and provides detailed information using the Google Gemini API. The application is designed with a clean, responsive interface that works across all devices.

## Features

- Select 3 to 5 symptoms from a comprehensive list.
- Predict disease based on symptoms using a pre-trained ML model.
- Displays prediction confidence.
- Provides detailed disease information using the Google Gemini API.
- Clean and responsive UI with custom styling.
- Informative disclaimers for medical advice.

---

## Demo

Access the live app here:  
[https://your-streamlit-app-url](https://your-streamlit-app-url)  
*(Replace with your deployed app URL)*

---

## Demo Pictures

### Main Interface
![Main Interface](demo/main_interface.png)
*The main interface where users can select their symptoms from the dropdown menu.*

### Symptom Selection
![Symptom Selection](demo/symptom_selection.png)
*Users can select 3-5 symptoms from the comprehensive list.*

### Prediction Results
![Prediction Results](demo/prediction_results.png)
*The app displays the predicted disease along with confidence level and detailed information.*

### Mobile Responsive
![Mobile View](demo/mobile_view.png)
*The app is fully responsive and works well on mobile devices.*

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/medi-sense.git
   cd medi-sense
````

2. **Create and activate a virtual environment (recommended)**

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Linux/macOS
   .\venv\Scripts\activate    # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Streamlit secrets**

   Create a `secrets.toml` file in `.streamlit` directory with the following content to add your Gemini API key (optional):

   ```toml
   GEMINI_API_KEY = "your-google-gemini-api-key"
   ```

   If you don't have a Gemini API key, the app will still work but without detailed disease descriptions.

---

## Usage

Run the Streamlit app locally with:

```bash
streamlit run app.py
```

* Select 3 to 5 symptoms from the dropdown list.
* Click the **Predict Disease** button.
* View the predicted disease and confidence.
* If configured, read detailed disease info powered by Google Gemini API.

---

## File Structure

```
.
├── app.py            
├── requirements.txt      
├── README.md              
└── .streamlit/            
```

> Note: The ML models and encoders are loaded dynamically from the Hugging Face repo:
> `https://huggingface.co/mohsinnyz/Disease-Guider`

---

## Technologies Used

* Python 3.x
* Streamlit
* Scikit-learn (joblib for loading models)
* NumPy
* Requests
* Google Gemini API (optional)
* Hugging Face (for model hosting)

---

## Disclaimer

⚠️ **This tool is for informational purposes only.**
**It is NOT a substitute for professional medical advice, diagnosis, or treatment.**
**Always consult a licensed medical professional for any health concerns.**

---

## Contact

Created by Mohsin Nyz
GitHub: [https://github.com/mohsinnyz](https://github.com/mohsinnyz)
Hugging Face: [https://huggingface.co/mohsinnyz](https://huggingface.co/mohsinnyz)

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```

Let me know if you want me to generate the `requirements.txt` or any other files!
```
