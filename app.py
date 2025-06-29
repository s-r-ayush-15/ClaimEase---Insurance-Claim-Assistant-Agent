import streamlit as st
from claim_agent import generate_claim_summary, get_required_documents_explained, explain_unclear_fields
# from pdf_generator import create_claim_pdf
import PyPDF2
from model_utils import is_insurance_document


# App Configuration
st.set_page_config(page_title="ClaimEase - Insurance Claim Assistant", layout="centered")
st.title("🤖 ClaimEase")

# Feature Selection
feature = st.selectbox(
    "What would you like help with?",
    [
        "📄 Smart Form Helper (Understand Claim Form)",
        "🗞️ Step-by-Step Claim Assistant"
    ]
)

# ---------------- SMART FORM HELPER ------------------
if feature == "📄 Smart Form Helper (Understand Claim Form)":
    st.subheader("📄 Upload Insurance Claim Form (PDF)")
    st.write("I’ll review your form and explain only the confusing fields.")

    uploaded_form = st.file_uploader("📎 Upload your form", type="pdf")

    if uploaded_form:
        reader = PyPDF2.PdfReader(uploaded_form)
        all_text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])


        # Step 1: Validate the document using local LLM

        with st.spinner("🔍 Checking if this is a valid insurance form..."):
            is_valid = is_insurance_document(all_text)

        if not is_valid:
            st.error("⚠️ This does not appear to be an insurance claim form. Please upload the correct document.")
            st.stop()

        def clean_text_lines(lines):
            cleaned = []
            for line in lines:
                line = line.strip()
                line = " ".join(line.split())  # fix weird spacing like “A ccount”
                cleaned.append(line)
            return cleaned
        raw_lines = [line.strip() for line in all_text.split("\n") if line.strip()]
        form_lines = clean_text_lines(raw_lines)

        with st.spinner("🧠 Reviewing your form..."):
            explanations = explain_unclear_fields(form_lines)

        st.success("Here are the fields that may need guidance:")
        for item in explanations:
            st.markdown(f"🔸 **{item['field']}**: {item['explanation']}")

            # ---------------- FORM HELPER BOT (Q&A) ------------------

        st.markdown("## 🤖 Need Help with the Form?")

    import time  # Optional: Simulated delay for realism

    st.markdown("---")
    st.subheader("💬 Ask a Question About This Form")
    st.write("Have a doubt about how to fill something? Just ask!")

    if "bot_history" not in st.session_state:
        st.session_state.bot_history = []

    if "clear_chat" not in st.session_state:
        st.session_state.clear_chat = False

    # --- Form bot input ---
    with st.form("form_bot_form"):
        user_question = st.text_input("Your Question:", key="form_bot_input")
        ask = st.form_submit_button("🧠 Ask Bot")
        clear = st.form_submit_button("🔁 Clear Chat")

    # --- Clear chat button logic ---
    if clear:
        st.session_state.bot_history = []
        st.session_state.clear_chat = True

    # --- Gemini-powered QA function ---
    from claim_agent import ask_form_bot  # New function for Q&A

    if ask and user_question.strip():
        with st.spinner("🤖 Thinking..."):
            time.sleep(1)  # Simulated delay
            bot_answer = ask_form_bot(user_question.strip())
            st.session_state.bot_history.append((user_question.strip(), bot_answer))

    # --- Display Q&A chat ---
    if st.session_state.bot_history:
        st.markdown("### 🧠 Assistant Chat")
        for i, (q, a) in enumerate(reversed(st.session_state.bot_history), 1):
            with st.container():
                st.markdown(
                    f"<div style='background-color:#2c3e50;color:#ffffff;padding:10px;border-radius:10px'><b>🧑‍💬 You:</b> {q}</div>",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"<div style='background-color:#fef9e7;color:#000000;padding:10px;border-radius:10px;margin-top:5px'><b>🤖 Bot:</b> {a}</div>",
                    unsafe_allow_html=True
                )
                st.code(a, language="markdown")  # copyable
                st.markdown("---")


# ---------------- STEP-BY-STEP CLAIM ASSISTANT ------------------
elif feature == "🗞️ Step-by-Step Claim Assistant":
    CLAIM_DOCS = {
        "Health Insurance": ["aadhaar", "policy", "medical_bill"],
        "Vehicle Insurance": ["aadhaar", "policy", "fir", "repair_estimate"],
        "Life Insurance": ["aadhaar", "policy", "death_certificate"],
        "Travel Insurance": ["aadhaar", "policy", "travel_booking", "expense_invoice"],
        "Home Insurance": ["aadhaar", "policy", "property_damage_photos", "repair_estimate"],
        "Mobile Insurance": ["aadhaar", "policy", "purchase_invoice", "damage_photo"],
        "Accidental Insurance": ["aadhaar", "policy", "medical_report", "incident_report"]
    }

    DOC_LABELS = {
        "aadhaar": "Aadhaar or ID Proof",
        "policy": "Insurance Policy Document",
        "medical_bill": "Medical Bill or Hospital Invoice",
        "fir": "FIR or Police Report",
        "repair_estimate": "Repair Estimate / Garage Invoice",
        "death_certificate": "Death Certificate",
        "travel_booking": "Flight or Travel Booking Proof",
        "expense_invoice": "Claimed Expense Invoice",
        "property_damage_photos": "Photos of Damaged Property",
        "purchase_invoice": "Mobile Purchase Invoice",
        "damage_photo": "Photo of Damaged Mobile",
        "medical_report": "Medical Report or Prescription",
        "incident_report": "Accident Report or Case File"
    }

    INSURANCE_TYPES = list(CLAIM_DOCS.keys())

    if 'step' not in st.session_state:
        st.session_state.step = 1

    if st.session_state.step == 1:
        st.markdown("### 🔍 Step 1: Select Insurance Claim Type")
        claim_type = st.selectbox("What type of claim are you filing?", INSURANCE_TYPES)

        if st.button("Next ➔ Show Required Documents"):
            st.session_state.claim_type = claim_type
            st.session_state.step = 2

    elif st.session_state.step == 2:
        st.markdown(f"### 📄 Step 2: Required Documents for {st.session_state.claim_type}")
        st.info("Using AI to help you understand exactly what’s required for your claim.")

        with st.spinner("🧠 Thinking..."):
            doc_guide = get_required_documents_explained(st.session_state.claim_type)

        st.success("✅ Here's what you'll need:")
        st.markdown(doc_guide)

        if st.button("➔ Proceed to Claim Questions"):
            st.session_state.step = 3

    elif st.session_state.step == 3:
        st.markdown("### 🧠 Step 3: Tell Me What Happened")

        date_of_incident = st.date_input("📅 When did the incident occur?")
        description = st.text_area("📝 Briefly describe what happened")
        location = st.text_input("📍 Where did it happen? (Optional)")
        people_involved = st.radio("👥 Was anyone else involved?", ["Yes", "No"])

        if st.button("✅ Submit Incident Details"):
            if not description.strip():
                st.warning("Please provide a short description.")
            else:
                st.session_state.incident_date = str(date_of_incident)
                st.session_state.incident_description = description
                st.session_state.incident_location = location
                st.session_state.incident_people = people_involved
                st.session_state.step = 4

    elif st.session_state.step == 4:
        st.markdown("### 📄 Step 4: AI-Generated Claim Summary")

        name = "Ayush Sharma"
        claim_type = st.session_state.claim_type
        incident_date = st.session_state.incident_date
        description = st.session_state.incident_description
        location = st.session_state.incident_location or "Not specified"
        people = st.session_state.incident_people

        with st.spinner("🧠 Generating claim summary..."):
            summary = generate_claim_summary(
                name=name,
                claim_type=claim_type,
                date=incident_date,
                description=description + f"\nLocation: {location}\nOther people involved: {people}"
            )

        st.session_state.final_summary = summary

        st.success("✅ Here's your AI-generated summary:")
        st.markdown(summary)

        # pdf_data = create_claim_pdf(name, summary)
        # st.download_button(
        #     label="📅 Download Summary as PDF",
        #     data=pdf_data,
        #     file_name="claim_summary.pdf",
        #     mime="application/pdf"
        # )

        if st.button("➔ Final Review & Confirmation"):
            st.session_state.step = 5

    elif st.session_state.step == 5:
        st.markdown("### ✅ Claim Summary Review")

        claim_type = st.session_state.claim_type
        name = "Ayush Sharma"
        summary = st.session_state.final_summary
        required_docs = CLAIM_DOCS.get(claim_type, [])

        st.success(f"🎉 You're all set, {name}!")
        st.markdown(f"Your **{claim_type}** claim has been successfully summarized.")

        st.subheader("📄 Suggested Required Documents:")
        for doc in required_docs:
            label = DOC_LABELS.get(doc, doc.replace("_", " ").title())
            st.markdown(f"📌 {label}")

        st.subheader("🧾 Incident Summary Recap:")
        st.markdown(f"**Date:** {st.session_state.incident_date}")
        st.markdown(f"**Location:** {st.session_state.incident_location or 'Not provided'}")
        st.markdown(f"**Other People Involved:** {st.session_state.incident_people}")
        st.markdown(f"**Description:**\n{st.session_state.incident_description}")

        from pdf_generator import create_claim_pdf

        # Add download button
        pdf_data = create_claim_pdf(name, summary)
        st.download_button(
            label="📄 Download Claim Summary as PDF",
            data=pdf_data,
            file_name="claim_summary.pdf",
            mime="application/pdf"
        )


        st.markdown("---")
        st.info("Thank you for using ClaimEase. You can now submit this PDF along with your claim to the insurance provider.")
