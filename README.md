# SwiftVisa – LLM-Powered RAG-Based Visa Eligibility Assistant

## Project Overview
**SwiftVisa** is an **LLM-powered, Retrieval-Augmented Generation (RAG) system** that helps users determine their eligibility for various UK visa types.  
It provides **policy-grounded, point-wise eligibility responses** based entirely on official government documents, without relying on rule-based systems, scraping, or translation APIs.  

The system combines **PDF document processing, vector embeddings, RAG-based retrieval, and a Streamlit interface** to guide users through visa eligibility assessment.

---

## Supported UK Visa Types
SwiftVisa currently supports five UK visa categories:  
1. **Student Visa**  
2. **Graduate Visa**  
3. **Health and Care Worker Visa**  
4. **Skilled Worker Visa**  
5. **Standard Visitor Visa**

---

## Project Workflow
1. **Policy Document Collection:**  
   - Collected official UK visa eligibility documents from gov.uk.  

2. **Text Extraction:**  
   - Extracted text from PDFs using **PDFPlumber**.  

3. **Text Cleaning & Formatting:**  
   - Removed unnecessary characters, merged lines, and structured headings.  

4. **Embedding Generation:**  
   - Converted cleaned text into **vector embeddings** using **SentenceTransformers**.  
   - Stored embeddings in **ChromaDB** for fast retrieval.

5. **RAG Query Test:**  
   - User queries are converted into embeddings.  
   - Relevant document chunks are retrieved from the vector store.  
   - Answers are generated using an **LLM**, grounded in retrieved policy documents.

6. **Streamlit Application:**
   Initially user is asked to select their desired visa type.
   - **Stage 1:** Collect visa type and personal, contact, and passport details.  
   - **Stage 2:** Collect user journey details.  
   - **Stage 3:** Collect visa-specific eligibility details.  
   - **Stage 4:** Review and edit details before submission.  
   - **Eligibility Result:**  
     - **Eligible:** Badge, confidence score, detailed explanation, document checklist, next steps, dos and don’ts, future visa options.  
     - **Not Eligible:** Badge, confidence score, explanation of unmet requirements, guidance on how to meet requirements.

---

## Features
- **LLM-powered reasoning:** Answers generated dynamically, not rule-based.  
- **Policy-grounded responses:** All eligibility outputs are based on official documents.  
- **RAG-based retrieval:** Retrieves relevant content from ChromaDB embeddings.  
- **Interactive Streamlit UI:** Guided multi-stage form for structured user input.  
- **Confidence scoring:** Shows how confident the system is about the eligibility decision.  
- **Detailed guidance:** Provides actionable next steps, required documents, and tips.

---

## Tech Stack
| Component         | Tools / Libraries                       |
|------------------|----------------------------------------- |
| Frontend         | Streamlit                                |
| Backend          | Python, custom RAG pipeline              |
| LLM              | Gemini 2.5, GPT-4, or OpenAI models      |
| Vector Store     | ChromaDB                                 |
| Embeddings       | SentenceTransformers                     |
| PDF Processing   | PDFPlumber                               |
| Deployment       | Streamlit Cloud                          |

---

## Screenshots
<img width="846" height="593" alt="image" src="https://github.com/user-attachments/assets/08309d8a-0862-4066-8c2a-64c6a5d50dff" />
<img width="520" height="605" alt="image" src="https://github.com/user-attachments/assets/30e11d4b-72b5-48fa-bfb7-258d61e69744" />
<img width="595" height="549" alt="image" src="https://github.com/user-attachments/assets/ff241b1a-5b1a-4aa1-bbbd-27e85ffc9b9c" />
<img width="749" height="407" alt="image" src="https://github.com/user-attachments/assets/ad3527d5-5d55-490a-a5c1-2e7673ac11ec" />
<img width="370" height="463" alt="image" src="https://github.com/user-attachments/assets/e45e00d1-9b81-4d10-92fc-b831ead00a09" />
<img width="393" height="655" alt="image" src="https://github.com/user-attachments/assets/92b758fe-c91c-49c1-9b8c-e82d58aedd46" />






