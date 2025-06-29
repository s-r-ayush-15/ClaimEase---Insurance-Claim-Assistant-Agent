# 🧠 ClaimEase – GenAI-Powered Insurance Claim Assistant

ClaimEase is a GenAI-powered multi-agent assistant built specifically for the Insurance domain. It helps users verify claim forms, explains complex fields, answers insurance claim-related questions, and generates structured claim summaries with PDF export. Built using Google Gemini API and Streamlit.

🔗 [Click here to try the hosted app](https://claimease-insurance-claim-assistant-agent.streamlit.app/)

> Replace the above link with your actual Streamlit Cloud URL

---

## 📌 Use Case

The assistant supports:

- Clients uploading claim forms and validating them using AI
- Claimants getting help on confusing form fields (like MICR, IFSC, PIR)
- Users generating professional insurance claim summaries
- Insurance agents creating client-ready documentation
- Businesses building claim automation flows using GenAI

---

## 🧩 Key Modules

### 1. 📝 Smart Claim Form Validator
- Upload any PDF claim form
- Uses a local LLM (DistilBART) to check if the document is a valid insurance claim form
- Rejects invalid uploads (like PAN card or bank forms)

---

### 2. 💬 Claim Form Assistant (Q&A)
- Built with Gemini 2.0 Flash
- Answers only insurance-claim-specific questions
- Auto-detects the insurance type from the uploaded document
- Refuses unrelated questions (like policy suggestions or investments)

---

### 3. 🔍 Field Explainer
- Scans uploaded form and extracts key fields
- Explains non-obvious fields (e.g., MICR, IFSC, Repatriation, Disability Cover)
- Skips obvious fields like Name, Gender, Phone

---

### 4. 🧾 Structured Claim Summary Generator
- Accepts short user-provided incident description
- Auto-generates:
  - Claimant info
  - Incident summary
  - Required documents
  - Actionable next steps

---

### 5. 📄 PDF Export
- Instantly downloads the generated summary as a formal PDF
- Ready for submission to insurance companies or storage

---

## 🧠 AI Models

- **Gemini 2.0 Flash** – for Q&A, field explanation, and summary generation  
- **DistilBART MNLI (local)** – for zero-shot document classification

> This hybrid LLM setup optimizes cost, latency, and offline reliability

---

🔄 Example Use Flow
Upload an insurance claim form (PDF)

System validates document type

AI explains confusing fields

User asks questions (Gemini-powered)

Enter incident details

Summary is generated and available as PDF

🧠 Future Enhancements
Add OCR to read scanned policy forms

Email integration for submitting PDFs

Multi-language support for clients and agents

Role-specific dashboards (Agent, User, Admin)

👨‍💻 Contributing
Want to contribute or improve the assistant?
Fork this repo, make changes, and create a pull request!
Your improvements are welcome.

📜 License
MIT License.
Use, share, or extend this project freely with attribution.
Built for the GenAI Agent Hackathon 2025 – BFSI Innovation Track.

🤝 Acknowledgements
Streamlit

Google Gemini

Hugging Face

DSW GenAI Hackathon 2025 Organizers

Everyone pushing innovation in BFSI + GenAI



