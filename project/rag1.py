import os
import json
import chromadb
import google.generativeai as genai

# 🔹 ADDED IMPORTS (ONLY FOR CONFIDENCE)
from bert_score import score as bert_score
from rouge_score import rouge_scorer

# --- CONFIGURATION ---
api_key = os.getenv("GEMINI_KEY") 
genai.configure(api_key=api_key)
MODEL_NAME = "gemini-2.5-flash"

# Setup Chroma
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_DIR = os.path.join(BASE_DIR, "chroma_db")
client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = client.get_or_create_collection(name="swiftvisa_embeddings")

# 🔹 ADDED: RULE + BERT + ROUGE CONFIDENCE
def calculate_confidence(context, explanation, satisfied, unsatisfied):
    # Rule matching (50%)
    total = len(satisfied) + len(unsatisfied)
    rule_score = (len(satisfied) / total) if total > 0 else 0.5

    # BERT F1 (30%)
    if explanation.strip():
        _, _, bert_f1 = bert_score(
            [explanation],
            [context],
            lang="en",
            verbose=False
        )
        bert_f1 = float(bert_f1.mean())
    else:
        bert_f1 = 0.0

    # ROUGE-L F1 (20%)
    rouge = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)
    rouge_l = rouge.score(context, explanation)["rougeL"].fmeasure

    confidence = (
        0.70 * rule_score +
        0.15 * bert_f1 +
        0.15 * rouge_l
    ) * 100

    return min(round(confidence), 95)


def run_rag_pipeline(user_profile: dict):
    # 1. Retrieval
    visa_type = user_profile.get("Profile", {}).get("visa_type", "UK Visa")
    query = f"UK {visa_type} visa eligibility criteria, mandatory documents, financial requirements, process steps, conditions of stay."
    
    results = collection.query(query_texts=[query], n_results=5)
    context = "\n\n".join(results["documents"][0])

    # 2. Decision Prompt (UNCHANGED)
    prompt = f"""
    You are a robotic logic engine for UK Visa processing.

    POLICY CONTEXT (The Rules):
    {context}

    APPLICANT DATA (The Facts):
    {json.dumps(user_profile, indent=2)}

    *** CRITICAL INSTRUCTIONS ***
    1. **ELIGIBILITY VERDICT (STRICT):**
       - Determine "ELIGIBLE" or "NOT ELIGIBLE" based *ONLY* on the specific Yes/No/Value answers provided in APPLICANT DATA.
       - If a requirement (e.g., "TB Test") is NOT mentioned in APPLICANT DATA, **DO NOT** let it affect the verdict.

    

    2. **GUIDANCE (MAXIMUM DETAIL):**
       - Document Checklist
       - Next Steps
       - Dos / Don'ts after going to UK , what they can and cannot do after arriving in the UK
       - Future Options
    3. **NEUTRALITY RULE (MANDATORY):**
       - **NEVER** assume the applicant gender based on their name.
       - **ALWAYS** use "The applicant" or "They/Their" in your reasoning and explanation.
    - Use policy terminology exactly as in the context
    - Avoid vague language


    OUTPUT FORMAT (JSON ONLY):
    {{
        "verdict": "ELIGIBLE" or "NOT ELIGIBLE",
        "confidence_score": 0-95,
        "explanation": "...",
        "satisfied_requirements": [],
        "unsatisfied_requirements": [],
        "checklist": [],
        "next_steps": [],
        "dos": [],
        "donts": [],
        "future_options": [],
        "remedy": "or null"
    }}
    """

    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(
        prompt, 
        generation_config={"temperature": 0.1, "response_mime_type": "application/json"}
    )
    
    try:
        result = json.loads(response.text)

        # 🔹 OVERRIDE confidence_score (ONLY CHANGE)
        result["confidence_score"] = calculate_confidence(
            context=context,
            explanation=result.get("explanation", ""),
            satisfied=result.get("satisfied_requirements", []),
            unsatisfied=result.get("unsatisfied_requirements", [])
        )

        return result

    except json.JSONDecodeError:
        return {
            "verdict": "ERROR", 
            "explanation": "Technical error in analysis.",
            "confidence_score": 0,
            "checklist": [],
            "next_steps": []
        }
