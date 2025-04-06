# 🎙️ Science Snippets: AI-Powered Science Podcast Generator

This is an interactive **Streamlit** app that generates **customized science podcasts** for students based on selected NCERT textbooks. Leveraging **Gemini Pro**, **CrewAI agents**, and **ElevenLabs TTS**, this app creates high-quality, age-appropriate, conversational podcast scripts and converts them to audio in minutes.

---

## ✨ Features

- 📚 Ingests and understands NCERT PDFs.
- 🧠 Uses LLM agents to answer questions and generate structured scripts.
- 🎤 Converts Host-Expert format scripts into professional-sounding podcasts.
- 🎧 Age-specific and style-tailored audio output (Fun, Detailed, or Step-by-Step).
- 🚀 Choose between **Deep Dive** or **Rapid Answers** podcast types.

---

## 📁 Directory Structure

```
├── .env
├── app.py                # Streamlit application
├── output/
│   ├── answers.txt
│   ├── script.txt
│   └── refine_script.txt
├── knowledge/             # Place your NCERT PDFs here
│   ├── NCERT-Class-12-Chemistry-Part-1.pdf
│   ├── NCERT-Class-12-Chemistry-Part-2.pdf
│   └── NCERT Class 12 Physics Part 2 ( PDFDrive ).pdf
```

---

## 🧪 Tech Stack

- **Streamlit** for UI  
- **CrewAI** for multi-agent workflows  
- **Gemini Pro Flash** via Google API for question answering and script generation  
- **ElevenLabs** for voice generation  
- **pydub** for combining audio segments  
- **dotenv** for managing API secrets  

---

## 🚀 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/palakrathore9/podcastgenerator
cd podcastgenerator
```

### 2. Set up Python environment

```bash
python -m venv venv
source venv/bin/activate   # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

### 3. Add your `.env` file

Create a `.env` file in the root directory and add the following:

```env
GEMINI_API_KEY=your_google_gemini_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
```

### 4. Add PDFs

Place your NCERT PDFs in a directory named `knowledge/`. Example filenames:

```
knowledge/
├── NCERT-Class-12-Chemistry-Part-1.pdf
├── NCERT-Class-12-Chemistry-Part-2.pdf
└── NCERT Class 12 Physics Part 2 ( PDFDrive ).pdf
```

You can modify the dictionary in `BOOKS` inside `main.py` to include more PDFs as needed.

---

## 🎮 How to Use

1. Run the app:

```bash
streamlit run main.py
```

2. Fill the form:
   - Student name, age, grade, and self-rating.
   - Choose preferred explanation style: Fun, Detailed, Step-by-Step.
   - Choose Podcast Type: Deep Dive or Rapid Answers.
   - Select relevant NCERT books.
   - Enter one or more science questions.

3. Click **"Generate Podcast"** to:
   - Create answers from PDFs.
   - Convert them to a podcast script.
   - Refine it into a Host-Expert format.
   - Synthesize and play the final audio!

---

## 📌 Notes

- ElevenLabs API is used to create two distinct voices (Host + Expert).
- Gemini's `text-embedding-004` is used for document embeddings.
- Uses `CrewAI`'s PDFKnowledgeSource to dynamically process book content.
- The app stores intermediate outputs (`answers.txt`, `script.txt`, etc.) in the `output/` folder.
- The final MP3 is generated and streamed in-app.

---

## 🤖 Coming Soon

- Upload custom textbooks or notes.
- Support for younger grades with simplified language.
- Save and share podcast episodes.
- UI enhancement and theming.

---

## 💬 Example Output

```
Host: Welcome to Science Snippets! Today we have some exciting questions from Riya, a 12th grader curious about nuclear fusion.  
Expert: That's right! Nuclear fusion is the process where two light atomic nuclei combine to form a heavier nucleus...
```

---


