# WasteLink AI – Autonomous Industrial Symbiosis Network

**One-Line Pitch:** WasteLink AI is an intelligent platform that uses Generative AI and Agentic AI to automatically discover and coordinate waste-to-resource exchanges between industries, transforming industrial waste into valuable resources.

---

## 📺 Demo Video

https://github.com/AnnavarapuGanesh/AI-Industrial-Symbiosis-Network/raw/master/AI-Industrial-Symbiosis-Network.mp4

---

## 🚀 Overview
WasteLink AI simulates an industrial ecosystem where waste producers (e.g., steel plants, food processors) and resource consumers (e.g., greenhouses, biofuel plants) are matched in real-time. The system uses a multi-agent architectural pipeline to interpret raw waste events, find semantic matches, optimize logistics, and draft mutual resource agreements.

## ✨ Key Features
- **Autonomous Interpreter Agent:** Converts raw, unstructured waste reports into structured data.
- **Semantic Matching:** Utilizes **ChromaDB** and **Sentence Transformers** to match waste streams with industrial demands.
- **Logistics Optimization:** Automatically calculates distances and feasibility for waste transport.
- **Autonomous Negotiator:** Drafts simulated legal and resource exchange agreements.
- **Sustainability Evaluator:** Generates ESG pitches and CO2 impact metrics for every match.
- **Live Agent Console:** A real-time "thought stream" showing the decision-making process of the AI agents.
- **Interactive Map:** Geospatial visualization of the industrial symbiosis network.

---

## 🛠️ Technology Stack

### Backend
- **Framework:** FastAPI (Python)
- **Database:** SQLite + SQLAlchemy
- **Vector DB:** ChromaDB (for semantic similarity search)
- **AI Agents:** LangChain with OpenAI/Groq integration
- **Embeddings:** Sentence Transformers (`all-MiniLM-L6-v2`)

### Frontend
- **Framework:** Next.js 14 (React)
- **Styling:** Tailwind CSS
- **Visualization:** React-Leaflet (Maps) & Lucide React (Icons)
- **Real-time:** WebSockets for live agent thought streaming

---

## 📁 Project Structure

```text
WasteLink/
├── backend/            # FastAPI Application
│   ├── agents.py       # LLM Agent logic
│   ├── main.py         # API & WebSockets
│   ├── vector_db.py    # ChromaDB integration
│   ├── workflow.py     # Agent Orchestration
│   └── seed_data.py    # Industrial data generator
├── frontend/           # Next.js Application
│   ├── src/app/        # Pages & Layouts
│   └── src/components/ # Dashboard & Map components
└── start_demo.bat      # One-click startup script
```

---

## 🏃 Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- (Optional) OpenAI or Groq API Key in `backend/.env`

### Installation
1. **Clone the repository** (or navigate to the folder).
2. **Setup Backend:**
   ```bash
   cd backend
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   python seed_data.py
   ```
3. **Setup Frontend:**
   ```bash
   cd ../frontend
   npm install
   ```

---

## 🕹️ Running the Demo

The easiest way to run the project is using the provided batch script:

1. Double-click the **`start_demo.bat`** file in the root directory.
2. It will launch the **Backend (Port 8000)** and the **Frontend (Port 3000)** in separate windows.
3. Your browser will automatically open to `http://localhost:3000`.
4. Click the **"SIMULATE EVENT"** button to trigger the agentic pipeline and watch the live symbiosis in action!

---

## 🧠 System Workflow
1. **Raw Waste Event** → **Interpreter Agent** (LLM parsed JSON)
2. **Embeddings** → **ChromaDB** (Semantic Search)
3. **Matcher Agent** → **Logistics Filter** (Distance calculation)
4. **Negotiator Agent** → **Mutual Agreement** (LLM generated)
5. **Evaluator Agent** → **Sustainability Pitch** (ESG metrics)
6. **Live Broadcast** → **Next.js UI** (WebSocket update)

---

## 🛡️ License
Built for Hackathon MVP Demonstration purposes.
