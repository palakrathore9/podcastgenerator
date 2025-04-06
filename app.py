import os
import streamlit as st
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from elevenlabs.client import ElevenLabs
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
from pydub import AudioSegment
import uuid
from elevenlabs import VoiceSettings

load_dotenv()

google_api_key = os.getenv("GEMINI_API_KEY")
elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")

if not google_api_key or not elevenlabs_api_key:
    st.error("Missing API keys. Please check .env file.")
    st.stop()

client = ElevenLabs(api_key=elevenlabs_api_key)

llm = LLM(
    model="gemini/gemini-2.0-flash",
    verbose=True,
    temperature=0.7,
    google_api_key=google_api_key
)


BOOKS = {
    "Class 12 Physics Part 2": "NCERT Class 12 Physics Part 2 ( PDFDrive ).pdf",
    "Class 12 Chemistry Part 1": "NCERT-Class-12-Chemistry-Part-1.pdf",
    "class 12 chemistry Part 2": "NCERT-Class-12-Chemistry-Part-2.pdf",

}

st.title("🎙️ Science Snipetts")

with st.form("student_form"):
    student_name = st.text_input("Student Name")
    student_age = st.number_input("Age", min_value=5, max_value=18, value=16)
    grade = st.selectbox("Grade", ["6th", "7th", "8th", "9th", "10th", "11th", "12th"])
    self_rating = st.selectbox("Self-Rating Understanding", [
        "No idea", "Know a little", "Understand some parts", "Know a lot"
    ])
    preferred_explanation_style = st.selectbox("Preferred Explanation Style", ["Fun", "Detailed", "Step-by-Step"])
    podcast_type = st.selectbox("Podcast Type", ["Deep Dive", "Rapid Answers"])

    selected_books = st.multiselect("Select Books", list(BOOKS.keys()))

    questions = st.text_area("Enter Questions (one per line)").strip().split("\n")

    submitted = st.form_submit_button("Generate Podcast")

if submitted and questions and student_name and selected_books:
    st.write("### Generating your podcast...")

   
    pdf_sources = [PDFKnowledgeSource(file_paths=[BOOKS[book]]) for book in selected_books]


    book_agent = Agent(
        role="answer questions",
        goal="You know everything about the selected pdfs.",
        backstory="You are a master at understanding pdfs and their content.",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        knowledge_sources=pdf_sources,
        embedder={
            "provider": "google",
            "config": {
                "model": "models/text-embedding-004",
                "api_key": google_api_key,
            }}
    )

    script_generator = Agent(
        role="Podcast Script Generator",
        goal="Generate a conversational podcast script in the Host-Expert format using provided answers.",
        backstory="A skilled AI that crafts engaging and structured podcast scripts from scientific explanations.",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    script_cleaner = Agent(
        role="Script Cleaner",
        goal="Ensure the script is strictly in a Host-Expert conversation format.",
        backstory="A meticulous editor that refines scripts to keep them clean and professional.",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    
    student_info = {
        "name": student_name,
        "age": student_age,
        "grade": grade,
        "self_rating": self_rating,
        "preferred_explanation_style": preferred_explanation_style,
        "podcast_type": podcast_type,
        "questions": questions
    }

    questions_text = "\n".join([f"{i+1}. {q}" for i, q in enumerate(questions)])

    
    book_task = Task(
        description=f"""
            Provide **detailed, structured explanations** for the following questions:
            {questions_text}

            **Response Guidelines:**  
            ✅ **Definition & Core Concept**: Start with a clear, concise definition.   
            ✅ **Step-by-Step Breakdown**: Explain logically.  
            ✅ **Real-World Applications**: Show how this concept applies in daily life.  
            ✅ **Key Takeaways**: Summarize insights at the end.
        """,
        expected_output="A structured response containing answers for all the given questions.",
        agent=book_agent,
        output_file="output/answers.txt"
    )

    generate_script_task = Task(
            description=f"""
            You are an AI-powered podcast assistant for "Science Snippets," using the answers you have to create a student-friendly science podcast. Your task is to generate a **conversational and engaging podcast script** based on a student's questions and the answers provided.
            
            ### **Student Information:**
            - **Name:** {student_info["name"]}
            - **Age:** {student_info["age"]}
            - **Grade Level:** {student_info["grade"]}
            - **Self-Rating Understanding:** {student_info["self_rating"]} (1: No idea, 2: Know a little, 3: Understand some parts, 4: Know a lot)
            - **Preferred Explanation Style:** {student_info["preferred_explanation_style"]} (Fun, Detailed, Step-by-Step)
            - **Podcast Type:** {student_info["podcast_type"]} (Deep Dive, Rapid Answers)

            ### **Student's Questions:**
            {questions_text}
            
            ---
            
            ## **🎙️ Podcast Script Guidelines:**  
            ✅ **Conversational & Engaging:** Use a lively and enthusiastic tone to keep the student interested.  
            ✅ **Age-Appropriate Depth:** Tailor explanations based on the **student’s age, grade, and self-rated understanding** for clarity and engagement.  
            ✅ **Match Preferred Explanation Style:**  
            - **Step-by-Step:** Break concepts into clear, logical steps.  
            - **Fun:** Use exciting analogies, humor, and storytelling elements.  
            - **Detailed:** Provide deeper scientific insights with real-world examples.  
            ✅ **Dynamic Back-and-Forth:** Use a **Host and Expert** format with a natural conversational flow.  
            ✅ **Seamless Transitions:** If answering multiple questions, connect them smoothly within one continuous episode.  
            ✅ **No Direct Student Interaction:** The student should be acknowledged at the beginning but should not actively participate in the script.  
            ---

            ### **Podcast Type Guidelines:**
            🚀 **Deep Dive (In-Depth Explanations)**  
            - Provide **detailed, step-by-step** explanation for each question explain at least in 10 lines.  
            - Use **real-world examples, analogies, and historical/scientific references**.  
            - Offer **follow-up insights** (e.g., "Did you know?" facts).  
            - Ensure clarity by breaking down complex concepts in an **age-appropriate manner**.  

            ⚡ **Rapid Answers (Concise & Direct)**  
            - Keep answers **short, clear, and to the point**.  
            - Prioritize **quick explanations** without skipping key facts.  
            - Use **simple analogies** for faster understanding.  
            ---

            Now, generate a high-quality podcast script following this structure, ensuring the dialogue follows the **Host-Expert** format. Do not include things like intro/outro music or sound effects.
            """,
            expected_output="A podcast script in a natural conversation format.",
            agent=script_generator,
            output_file="output/script.txt",
            context=[book_task]
        )

    refine_script_task = Task(
        description="""
        Ensure the script is strictly in a Host-Expert conversation format, keeping the expert’s name within the conversation where appropriate but not as a role indicator.  
        The left side of the dialogue should only contain 'Host' and 'Expert'.  

        **Example Output Format:**

        Host:Welcome to Science Snippets! Today, we have some amazing questions from Alex, a 6th grader who wants to know all about volcanoes.  
        Expert:That’s right! Hi Alex! Great question—volcanoes erupt because of pressure buildup deep inside the Earth.  
        Host:That sounds intense! So, what causes all that pressure in the first place?  
        Expert:Well, inside the Earth, we have something called magma, which is molten rock. Over time, gases build up, and when the pressure is too high… boom! The volcano erupts.  
        Host:Wow! So, is every eruption the same?  
        Expert:Not at all! Some eruptions are explosive, while others are slow and steady. It depends on the type of volcano and the magma inside.  
        Host:That’s fascinating! Thanks for explaining.  

        **Key Refinements:**  
        ✅ Keep 'Host' and 'Expert' as role indicators.  
        ✅ The expert's name can be naturally mentioned within the dialogue, but not as a role indicator.  
        ✅ Remove any unnecessary sound effects, background cues, or extra role labels.  
        """,
        agent=script_cleaner,
        context=[generate_script_task],
        expected_output="A clean, structured script with only 'Host' and 'Expert' dialogue, ensuring smooth transitions.",
        output_file="output/refine_script.txt"
    )

    crew = Crew(
        agents=[book_agent, script_generator, script_cleaner],
        tasks=[book_task, generate_script_task, refine_script_task],
        process=Process.sequential
    )

    result_script = crew.kickoff()

    def text_to_speech_file(text, voice_id):
        response = client.text_to_speech.convert(
            voice_id=voice_id,
            output_format="mp3_22050_32",
            text=text,
            model_id="eleven_turbo_v2_5",
            voice_settings=VoiceSettings(
                stability=0.3,
                similarity_boost=1.0,
                style=0.0,
                use_speaker_boost=True,
            )
        )
        file_path = f"{uuid.uuid4()}.mp3"
        with open(file_path, "wb") as f:
            for chunk in response:
                f.write(chunk)
        return file_path

    def generate_podcast_audio(script_text):
        segments = script_text.split("\n")
        host_voice = "pNInz6obpgDQGcFmaJgB"
        expert_voice = "EXAVITQu4vr4xnSDxMaL"

        audio_files = []
        for line in segments:
            if line.startswith("Host:"):
                audio_file = text_to_speech_file(line.replace("Host:", ""), host_voice)
                audio_files.append(audio_file)
            elif line.startswith("Expert:"):
                audio_file = text_to_speech_file(line.replace("Expert:", ""), expert_voice)
                audio_files.append(audio_file)

        final_audio = AudioSegment.empty()
        for file in audio_files:
            final_audio += AudioSegment.from_file(file)

        podcast_file = "final_podcast4.mp3"
        final_audio.export(podcast_file, format="mp3")

        for file in audio_files:
            os.remove(file)

        return podcast_file

    podcast_file = generate_podcast_audio(str(result_script))
    st.success("✅ Podcast Generated Successfully!")

    st.audio(podcast_file, format="audio/mp3", start_time=0)

else:
    if submitted:
        st.warning("Please fill all details, select books, and enter questions.")

