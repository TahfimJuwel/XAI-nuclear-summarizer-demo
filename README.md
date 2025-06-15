# XAI Nuclear Incident Summarizer - MVP Demo

### 1. Project Overview

This project is a rapid prototype (MVP) of an **Explainable AI (XAI) Text Summarizer** designed for the nuclear industry. It was developed as part of a 2-day implementation challenge to demonstrate the feasibility of creating valuable AI tools for regulated sectors using open-source components.

The application summarizes technical texts, such as nuclear incident reports, and provides a crucial layer of explainability by highlighting the specific sentences in the original text that most influenced the generated summary.

This proof-of-concept is directly inspired by the **CurieLM** model (from Task 1), which emphasizes the need for domain-adapted LLMs with explainability features to build trust and ensure auditability in high-stakes regulatory environments. While this demo uses a general-purpose model, it establishes the core workflow and user experience for a more advanced, fine-tuned system.

### 2. Key Features

*   **Text Summarization:** Ingests long incident reports and generates a concise, coherent summary.
*   **Explainable AI (XAI):**
    *   **Visual Highlighting:** The original text is displayed with the most influential sentences marked, showing users *why* the model generated its summary.
    *   **Key Sentence Extraction:** The top 3 sentences that contributed most to the summary are listed for clarity and quick review.
*   **Interactive UI:** A simple and intuitive web interface built with Streamlit.
*   **Offline First:** The model runs entirely locally, ensuring data privacy and security, which is a critical requirement for the nuclear industry.

### 3. Demo Walkthrough

**Screenshot 1: Initial Application Interface**
*The user pastes or uses the sample incident report text.*

 <!-- Replace with your screenshot URL -->

**Screenshot 2: Generated Summary and Explanation**
*After clicking the button, the app displays the summary and the highlighted source text, providing a clear explanation.*

 <!-- Replace with your screenshot URL -->


### 4. Technology Stack

*   **Model:** `sshleifer/distilbart-cnn-6-6` - A distilled version of the BART model, chosen for its small footprint and strong performance on general summarization tasks.
*   **Framework:** Streamlit
*   **Core Libraries:**
    *   `transformers` (Hugging Face) for model loading and pipeline creation.
    *   `torch` as the backend deep learning framework.
    *   `nltk` for sentence tokenization.
    *   `rouge_score` for calculating sentence relevance for the XAI feature.

### 5. How to Run the Demo

**Prerequisites:**
*   Python 3.9+
*   Git (for cloning the repository)
*   The `distilbart-cnn-6-6` model files (these must be downloaded separately).

**Setup Instructions:**

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2.  **Download the Model:**
    *   Go to the model page on Hugging Face: [sshleifer/distilbart-cnn-6-6](https://huggingface.co/sshleifer/distilbart-cnn-6-6/tree/main)
    *   Click on "Files and versions".
    *   Download all the relevant files (especially `pytorch_model.bin`, `config.json`, `vocab.json`, and `merges.txt`).
    *   Create a folder named `distilbart-cnn-6-6` inside the project's root directory and place all the downloaded model files inside it. The `app.py` script is coded to look for this exact folder name.

3.  **Create and activate a virtual environment:**
    ```bash
    # Create the environment
    python -m venv venv

    # Activate on Windows
    .\venv\Scripts\Activate.ps1

    # Activate on macOS/Linux
    source venv/bin/activate
    ```

4.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```

6.  Open the local URL provided in the terminal (e.g., `http://localhost:8501`) in your web browser.

---

### 6. Reflection and Lessons Learned

#### What Worked Well

*   **Rapid Prototyping with Streamlit and Hugging Face:** The combination of these two tools was incredibly effective for meeting the 48-hour deadline. Streamlit allowed for a polished UI with minimal code, and the Hugging Face `pipeline` API made it trivial to deploy a powerful summarization model locally.
*   **Proxy-Based XAI is Feasible and Effective:** Using ROUGE scores as a proxy for "influence" was simple to implement yet provided a clear and intuitive explanation for the user. It effectively demonstrates the *principle* of explainability without requiring deep model surgery.

#### What Was Challenging

*   **Model Specificity vs. Generalization:** The biggest challenge was using a **general-purpose model** (trained on news) for a **highly specific domain** (nuclear reports). The summary quality is decent but lacks a true understanding of industry-specific terminology.
*   **Dependency and Environment Setup:** The initial setup, especially downloading large libraries like `torch` and troubleshooting network errors, consumed a non-trivial portion of the development time.

#### Future Improvements

*   **Fine-Tune a Domain-Specific Model:** The single most important improvement would be to **fine-tune a base LLM (like Mistral or Llama 3) on a dedicated nuclear corpus** (e.g., from the NRC's ADAMS library). This would dramatically improve the model's accuracy, relevance, and understanding of industry jargon.
*   **Advanced XAI with Source Attribution:** Instead of just highlighting, each sentence in the generated summary could be hyperlinked back to the specific source sentences it was derived from. This creates a directly auditable trail essential for regulatory compliance.
*   **Hallucination Detection:** An additional module could be built to flag any statements in the summary that cannot be substantiated by the original report, preventing the spread of misinformation in a safety-critical context.