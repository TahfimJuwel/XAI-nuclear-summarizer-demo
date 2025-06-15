# app.py - FINAL, CORRECTED VERSION

import streamlit as st
import nltk
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from rouge_score import rouge_scorer
import os

# --- ADD THIS BLOCK TO SOLVE THE NLTK LOOKUPERROR ---
# Point NLTK to a local data folder to make the app self-contained.
# This requires you to first run `python -m nltk.downloader -d ./nltk_data punkt` in your terminal.
nltk.data.path.append('./nltk_data')
# ----------------------------------------------------


# --- 1. SETUP AND MODEL LOADING (Cached for performance) ---

@st.cache_resource
def load_model():
    """
    Loads the DistilBART model and tokenizer from a local path.
    """
    # This path MUST match the folder name you created for the model files.
    model_path = "distilbart-cnn-6-6"

    # Check if the model directory exists before trying to load
    if not os.path.exists(model_path):
        st.error(f"Model directory not found. Please ensure the model files are in a folder named '{model_path}'.")
        return None

    try:
        # Load the model and tokenizer from the local folder
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
        summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)
        return summarizer
    except Exception as e:
        st.error(f"An error occurred while loading the model: {e}")
        return None

# --- 2. HELPER FUNCTIONS FOR XAI ---

def summarize_and_explain(text_to_summarize, summarizer_pipeline):
    """Generates a summary and provides an explanation for a BART-style model."""
    # A. Generate Summary
    # NOTE: BART models do NOT need a "summarize: " prefix like T5 models.
    # We pass the text directly.
    summary_result = summarizer_pipeline(text_to_summarize, max_length=120, min_length=40, do_sample=False)
    generated_summary = summary_result[0]['summary_text']

    # B. Implement Explainability
    # The NLTK data path is now set globally at the top of the script,
    # so we can remove the problematic download line from here.
    sentences = nltk.sent_tokenize(text_to_summarize)
    
    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
    sentence_scores = []
    for sentence in sentences:
        if len(sentence.strip()) > 20:
            score = scorer.score(generated_summary, sentence)
            sentence_scores.append((sentence, score['rougeL'].fmeasure))

    sorted_sentences = sorted(sentence_scores, key=lambda x: x[1], reverse=True)
    top_sentences = [s[0] for s in sorted_sentences[:3]]

    highlighted_text = text_to_summarize
    for sentence in top_sentences:
        highlighted_text = highlighted_text.replace(sentence, f"<mark>{sentence}</mark>")
    
    return generated_summary, highlighted_text, top_sentences


# --- 3. STREAMLIT USER INTERFACE (Identical to before) ---

st.set_page_config(page_title="XAI Nuclear Summarizer", layout="wide")
st.title("🔬 XAI-Powered Summarizer for Nuclear Incident Reports")
st.write("""
This demo showcases how an LLM can summarize technical documents with an added layer of **Explainable AI (XAI)**. 
Enter an incident report below, and the tool will generate a summary and highlight the key sentences from the original text that most influenced the output.
""")

# Load the model and display a status message
with st.spinner("Loading the summarization model..."):
    summarizer = load_model()

# If the model loaded successfully, show the main part of the app
if summarizer:
    st.success("Model loaded successfully!")
    
    sample_report_text = """
    EVENT NOTIFICATION: 45738
    LICENSEE: XYZ ENERGY
    SITE: OAK CREEK NUCLEAR PLANT
    DOCKET: 05000400
    EVENT DATE: 03-15-2024

    EVENT DESCRIPTION:
    At 14:22 EST, an automatic reactor trip occurred on Unit 1 from 100% power. The trip was initiated by a main turbine trip signal. The turbine trip was caused by a loss of the 'A' Main Feedwater Pump (MFP) due to a failure of its associated electrical breaker. All control rods fully inserted as designed, and the reactor was successfully shut down.

    Following the trip, the Auxiliary Feedwater (AFW) system automatically initiated to provide cooling to the steam generators, as is the standard procedure. However, the 'B' train of the AFW system failed to start. The 'A' and 'C' trains of the AFW system started successfully and are providing adequate decay heat removal. The 'B' AFW pump is currently under investigation by maintenance personnel. Plant operators responded appropriately and stabilized the plant in a hot shutdown condition.

    SAFETY ASSESSMENT:
    There was no release of radioactive material to the environment. All safety systems responded as expected, with the exception of the 'B' AFW pump. The redundant 'A' and 'C' AFW trains are fully functional and sufficient for maintaining the plant in a safe state. The event is classified as a Non-Emergency event under the NRC's emergency classification system. The health and safety of the public were not affected. The licensee will conduct a full root cause analysis for both the MFP breaker failure and the AFW pump failure.
    """

    st.subheader("Enter Incident Report Text:")
    user_input = st.text_area("You can use the sample text or paste your own.", sample_report_text, height=300)

    if st.button("Generate Summary and Explanation", type="primary"):
        if not user_input.strip():
            st.warning("Please enter some text to summarize.")
        else:
            with st.spinner("Analyzing text and generating explanation..."):
                summary, highlighted_explanation, top_sentences_list = summarize_and_explain(user_input, summarizer)
                
                st.subheader("📝 Generated Summary")
                st.success(summary)

                st.subheader("🔍 Explainability: Visual Highlight")
                st.write("Below is the original text with the most influential sentences highlighted.")
                st.markdown(f'<div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; line-height: 1.6;">{highlighted_explanation}</div>', unsafe_allow_html=True)
                
                st.subheader("📄 Explainability: Key Sentences")
                st.write("The summary was primarily derived from these top 3 sentences:")
                for i, sentence in enumerate(top_sentences_list):
                    st.info(f"{i+1}. {sentence.strip()}")