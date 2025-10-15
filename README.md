# 🧠 MinuteMe

**MinuteMe** is an **AI-powered meeting assistant** that automates transcription, agenda planning, action item tracking, and meeting minutes generation — helping teams save time, stay organized, and boost productivity.

---

## 🌟 Overview

In many organizations, meetings often lead to scattered notes and lost action items. **MinuteMe** simplifies this by:
- Automatically transcribing meetings from audio/video.  
- Generating structured, professional meeting minutes.  
- Tracking action items and upcoming agendas in one dashboard.  

---

## 🚀 Features

- 🎙 **Transcription Agent** – Converts meeting audio/video into text transcripts using **Google Gemini API**.  
- 🧾 **Minutes Generator** – Summarizes transcripts and generates formatted meeting minutes.  
- 🗓 **Agenda Planner** – Create and manage meeting agendas easily.  
- ✅ **Action Item Tracker** – Extracts, assigns, and manages tasks from meeting discussions.  
- 📊 **User Dashboard** – View transcripts, minutes, and tasks in one place.  
- 🔐 **Admin Panel** – Manage users, meetings, and automation quotas.

---

## 🧩 Technologies Used

### **Backend**
- 🐍 Python, FastAPI  
- ☁️ Google Generative AI (Gemini)  
- 🍃 MongoDB Atlas  
- 🎥 ffmpeg, moviepy  

### **Frontend**
- ⚛️ React + Vite  
- 🔐 Clerk Authentication  
- 🌐 Axios  

### **AI / NLP**
- 🧠 NLTK  
- 🤖 scikit-learn  
- 🧩 Transformers  
- 🔥 PyTorch  

---

## ⚙️ System Requirements

| Requirement | Minimum Version |
|--------------|------------------|
| **Node.js** | 18+ |
| **Python** | 3.10+ |
| **MongoDB Atlas** | Account with connection string |
| **Google API Key** | Gemini enabled |
| **Clerk Account** | For authentication |

---

## 🏗️ Project Architecture

```bash
MinuteMe/
├── backend/
│   ├── agents/
│   │   ├── transcription_agent/   → Handles speech-to-text conversion
│   │   ├── minutes_generator/     → Summarizes transcripts into minutes
│   │   ├── action_tracker/        → Detects and stores actionable tasks
│   │   └── agenda_planner/        → Manages meeting agenda entries
│   ├── db/                        → MongoDB connection & data handlers
│   ├── api.py                     → FastAPI entry point
│   ├── requirements.txt
│   ├── .env
│   └── ...
│
├── frontend/
│   ├── src/
│   │   ├── components/            → UI components (Dashboard, Minutes View, etc.)
│   │   ├── pages/                 → React route pages
│   │   ├── services/              → Axios API calls
│   │   └── ...
│   ├── .env
│   ├── package.json
│   └── vite.config.js
│
└── README.md

```

### 🧭 Workflow Diagram

User Uploads Audio/Video
↓
🎙 Transcription Agent (Gemini)
↓
🧾 Minutes Generator
↓
✅ Action Tracker
↓
🗓 Agenda Planner
↓
📊 Dashboard (React + Clerk)


Each module communicates via RESTful APIs built using **FastAPI** and stored in **MongoDB**, providing a smooth and scalable backend pipeline.

---

## 🧰 Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/MinuteMe.git
cd MinuteMe
```

### 2️⃣ Backend Setup
🔹 Create and Activate Virtual Environment
```bash
cd backend
python -m venv .venv
```
Activate it:
Windows:
```bash
.venv\Scripts\activate
```
Mac/Linux:
```bash
source .venv/bin/activate
```
🔹 Install Dependencies
```bash
pip install -r requirements.txt

```

Create .env File in backend/

```bash
GOOGLE_API_KEY=AIzaSyBypfmnJgLv7c8zmd7d5_VLkvL-0_t3mpM
OPENAI_API_KEY= ADD your api key
MONGO_URI= ADD your database mongodb url
MONGO_DB=minuteme

# Clerk Authentication
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_dG9nZXRoZXItaGlwcG8tOTIuY2xlcmsuYWNjb3VudHMuZGV2JA
CLERK_SECRET_KEY=sk_test_vRxL7jClTj6ikqHoioLOfl42ZVJDAHdITmEeGsZZBq
```
Start Backend Server
```bash
uvicorn api:app --reload
```
Backend will run at 👉 http://127.0.0.1:8000

### 3️⃣ Frontend Setup

```bash
cd ../frontend
npm install
```
🔹 Create .env File in frontend/
```bash
VITE_CLERK_PUBLISHABLE_KEY=pk_test_dG9nZXRoZXItaGlwcG8tOTIuY2xlcmsuYWNjb3VudHMuZGV2JA
```

🔹 Run Frontend
```bash
npm run dev
```

Frontend will be available at 👉 http://localhost:5173


### 🧑‍💻 Usage

Upload your meeting audio/video file.

The Transcription Agent converts it to text.

The Minutes Generator produces professional summaries.

The Action Tracker highlights and assigns key tasks.

Manage everything from the dashboard — download, edit, or share minutes.

### 🧱 API Endpoints (Sample)
| Endpoint            | Method | Description                            |
| ------------------- | ------ | -------------------------------------- |
| `/transcribe`       | POST   | Upload and convert meeting audio/video |
| `/generate_minutes` | POST   | Generate structured meeting minutes    |
| `/get_minutes`      | GET    | Retrieve all saved meeting minutes     |
| `/agenda`           | POST   | Create or edit meeting agendas         |
| `/action-items`     | GET    | Get extracted actionable tasks         |



### 🧠 AI Workflow Summary

| Stage | Agent               | Description                              |
| ----- | ------------------- | ---------------------------------------- |
| 1     | Transcription Agent | Converts audio/video → text (Gemini API) |
| 2     | Minutes Generator   | Summarizes transcript → minutes          |
| 3     | Action Tracker      | Detects to-dos → stores tasks            |
| 4     | Agenda Planner      | Schedules agenda + reminders             |
| 5     | Dashboard           | Displays data visually (React + Clerk)   |



### 🌍 Acknowledgements

Google Gemini API

FastAPI

MongoDB Atlas

Clerk Authentication

React.js





