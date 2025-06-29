# claim_agent.py

import os
import google.generativeai as genai

# 🌍 For local development: load .env (safely ignored in Streamlit Cloud)
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass  # Skip silently if dotenv isn't available (e.g., in cloud)

# 🔐 Get API key (from .env or Streamlit Secrets)
api_key = os.getenv("GEMINI_API_KEY")

# ⚠️ Safe Gemini model configuration with fallback
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")
except Exception as e:
    print(f"[Gemini Init Error] {e}")
    model = None


# ✅ Structured Claim Summary Generator
def generate_claim_summary(name, claim_type, date, description):
    if not model:
        return "⚠️ Gemini model not available."

    prompt = f"""
You are an AI agent tasked with generating **structured insurance claim summaries** for formal documentation.

Generate a markdown-style summary using the following structure:

**Claimant Name**: {name}  
**Claim Type**: {claim_type}  
**Date of Incident**: {date}  

---

### 📝 Incident Summary
{description}

### 📄 Required Documents
List 3–5 documents commonly required for {claim_type}. Use short bullet points.

### 🔄 Next Steps
Suggest 2–3 action items to complete the claim process.

Use clear, professional, and helpful language.
"""
    response = model.generate_content(prompt)
    return response.text.strip()


# ✅ Required Document Explainer
def get_required_documents_explained(claim_type):
    if not model:
        return "⚠️ Gemini model not available."

    prompt = f"""
You're an insurance claims expert. A user is filing a {claim_type}.

List:
- Which documents are typically required
- Why each document is needed
- Any optional or alternative documents

Respond clearly in a friendly tone.
"""
    response = model.generate_content(prompt)
    return response.text.strip()


# ✅ Smart Field Explanation from PDF lines
def explain_unclear_fields(lines):
    if not model:
        return [{"field": "System", "explanation": "⚠️ Gemini model not available."}]

    prompt = f'''
You are an expert assistant helping someone fill out an insurance claim form.

Your task is to:
- Identify **only the confusing or non-obvious fields**.
- DO NOT return explanation for fields like name, gender, email, phone, DOB.
- Focus on technical, banking, legal, medical, insurance-specific terms.
- Especially explain if you see anything like:
  - Bank details (MICR, IFSC, account number)
  - Policy details
  - Repatriation / disability / burial costs
  - Supporting documents (PIR, medical certificate, etc.)

Example format:
Field: MICR No.
Explanation: This is a 9-digit code found on your cheque. It helps your bank identify the branch for payment.

Use the above format and return only 6–10 fields at most.

Lines:
{chr(10).join(lines)}
    '''
    response = model.generate_content(prompt)

    output = []
    for block in response.text.strip().split("Field:"):
        if block.strip():
            parts = block.strip().split("Explanation:")
            if len(parts) == 2:
                field = parts[0].strip()
                explanation = parts[1].strip()
                output.append({"field": field, "explanation": explanation})
    return output


# ✅ Claim-Form-Specific Bot (ignores off-topic questions)
def ask_form_bot(question, form_type="insurance claim"):
    if not model:
        return "⚠️ Gemini model not available."

    prompt = f"""
You are a specialized AI assistant that ONLY helps users with **{form_type} forms**.

✅ You may answer questions ONLY if they are about:
- Understanding confusing fields in the form
- Required documents for a claim
- Claim filing steps

🚫 If the question is unrelated (e.g., about policies, investment, coverage, buying insurance), respond with:
"I'm here to help only with insurance claim forms. Please ask a form-related question."

Question:
{question}

Your answer:
"""
    response = model.generate_content(prompt)
    return response.text.strip()
