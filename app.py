import os
import gradio as gr
import openai
import json
import random
from dotenv import load_dotenv
import gc
from openai import OpenAI
from flask import Flask, request, jsonify
app = Flask(__name__)

# Load environment variables from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Full Study Guide Content
STUDY_GUIDE = {
    "Imperative": {
        "title": "Formas Imperativas (Command Forms)",
        "explanation": """
El imperativo se usa para dar órdenes, hacer peticiones o consejos.

**Formación del imperativo afirmativo:**
- Para tú: usa la 3ª persona singular del presente de indicativo
  - hablar → habla
  - comer → come
  - vivir → vive
- Excepciones: ir (ve), ser (sé), tener (ten), venir (ven), decir (di), hacer (haz), poner (pon), salir (sal)

**Formación del imperativo negativo:**
- Para todas las personas: usa el presente de subjuntivo
  - No hables tan alto
  - No comáis ahora
        """,
        "examples": [
            "Habla más despacio. (Talk slower.)",
            "No abras la ventana. (Don't open the window.)",
            "Venid aquí, chicos. (Come here, guys.)",
            "No salgas ahora. (Don't go out now.)"
        ],
        "practice": [
            {"question": "Transforma a imperativo afirmativo (tú): Necesitas estudiar más.", "answer": "Estudia más."},
            {"question": "Transforma a imperativo negativo (vosotros): Debéis llegar tarde.", "answer": "No lleguéis tarde."},
            {"question": "¿Cuál es el imperativo de 'ser' (tú)?", "answer": "sé"}
        ]
    },
    "Subjunctive": {
        "title": "Subjuntivo vs. Indicativo",
        "explanation": """
**Indicativo:** Se usa para expresar hechos, certezas y realidades.
**Subjuntivo:** Se usa para expresar deseos, dudas, posibilidades y subjetividad.

**Situaciones que requieren subjuntivo:**
1. Después de expresiones de deseo: querer que, esperar que, preferir que
2. Después de expresiones de duda: no creer que, dudar que, no estar seguro de que
3. Después de expresiones de emoción: alegrarse de que, sentir que, temer que
4. En cláusulas que expresan finalidad con "para que"
5. Con expresiones impersonales: es importante que, es necesario que
        """,
        "examples": [
            "Indicativo: Creo que tiene razón. (I think he's right.)",
            "Subjuntivo: No creo que tenga razón. (I don't think he's right.)",
            "Indicativo: Sé que viene mañana. (I know he's coming tomorrow.)",
            "Subjuntivo: Espero que venga mañana. (I hope he comes tomorrow.)"
        ],
        "practice": [
            {"question": "Completa con indicativo o subjuntivo: Pienso que _____ (ser) una buena idea.", "answer": "es (indicativo)"},
            {"question": "Completa con indicativo o subjuntivo: Dudo que él _____ (poder) hacerlo.", "answer": "pueda (subjuntivo)"},
            {"question": "Completa con indicativo o subjuntivo: Es importante que nosotros _____ (estudiar) para el examen.", "answer": "estudiemos (subjuntivo)"}
        ]
    },
    "PorVsPara": {
        "title": "Por vs. Para",
        "explanation": """
**Por** se usa para:
1. Causa o motivo: "Lo hice por ti"
2. Duración de tiempo: "Trabajé por tres horas"
3. Movimiento a través de un lugar: "Caminamos por el parque"
4. Intercambio: "Te cambio esto por aquello"
5. Medio o modo: "Te envié el mensaje por WhatsApp"

**Para** se usa para:
1. Propósito o finalidad: "Estudio para aprobar"
2. Destinatario: "Este regalo es para ti"
3. Dirección: "Salgo para Madrid"
4. Plazo o límite de tiempo: "Necesito el informe para mañana"
5. Comparación: "Para su edad, habla muy bien"
        """,
        "examples": [
            "Trabajo por dinero. (I work for money - cause)",
            "Trabajo para vivir mejor. (I work to live better - purpose)",
            "Pasé por tu casa. (I passed by your house - through)",
            "Esto es para ti. (This is for you - recipient)"
        ],
        "practice": [
            {"question": "Completa: Estudio español _____ trabajo.", "options": ["por", "para"], "answer": "para"},
            {"question": "Completa: Lo hago _____ ti.", "options": ["por", "para"], "answer": "por"},
            {"question": "Completa: Este regalo es _____ tu madre.", "options": ["por", "para"], "answer": "para"}
        ]
    },
    "Conditionals": {
        "title": "Oraciones Condicionales",
        "explanation": """
**Condicionales Tipo 1 (Real o Probable):**
- Si + presente de indicativo + presente/futuro/imperativo
- Ejemplo: "Si estudias, aprobarás el examen."

**Condicionales Tipo 2 (Hipotético presente):**
- Si + imperfecto de subjuntivo + condicional simple
- Ejemplo: "Si tuviera dinero, compraría una casa."

**Condicionales Tipo 3 (Hipotético pasado - imposible):**
- Si + pluscuamperfecto de subjuntivo + condicional compuesto
- Ejemplo: "Si hubiera estudiado, habría aprobado el examen."
        """,
        "examples": [
            "Si llueve mañana, llevaré paraguas. (Tipo 1)",
            "Si fuera rico, viajaría por todo el mundo. (Tipo 2)",
            "Si hubieras venido, lo habrías pasado bien. (Tipo 3)"
        ],
        "practice": [
            {"question": "Completa con la forma correcta: Si _____ (tener) tiempo, te ayudaré. (Tipo 1)", "answer": "tienes"},
            {"question": "Completa con la forma correcta: Si _____ (ser) tú, no lo haría. (Tipo 2)", "answer": "fuera"},
            {"question": "Completa con la forma correcta: Si _____ (estudiar) más, habrías aprobado. (Tipo 3)", "answer": "hubieras estudiado"}
        ]
    },
    "Preterites": {
        "title": "Pretérito Indefinido vs. Imperfecto",
        "explanation": """
**Pretérito Indefinido (Simple Past):**
- Acciones completas y terminadas en el pasado
- Acciones puntuales
- Acciones en secuencia
- Verbos como: nacer, morir, empezar, terminar, etc.

**Pretérito Imperfecto (Imperfect):**
- Descripción de situaciones o escenarios en el pasado
- Acciones habituales en el pasado
- Expresar edad, hora, clima en el pasado
- Acciones en progreso que fueron interrumpidas
        """,
        "examples": [
            "Indefinido: Ayer vi una película. (Yesterday I saw a movie.)",
            "Imperfecto: Cuando era niño, jugaba al fútbol. (When I was a child, I used to play soccer.)",
            "Indefinido: Juan llegó a las 8. (Juan arrived at 8.)",
            "Imperfecto: Eran las 8 cuando Juan llegó. (It was 8 when Juan arrived.)"
        ],
        "practice": [
            {"question": "Elige entre indefinido o imperfecto: Yo _____ (estar) en casa cuando me _____ (llamar).", "answer": "estaba (imperfecto), llamó (indefinido)"},
            {"question": "Elige entre indefinido o imperfecto: Cuando _____ (ser) joven, _____ (vivir) en Madrid.", "answer": "era (imperfecto), vivía (imperfecto)"},
            {"question": "Elige entre indefinido o imperfecto: Ayer _____ (ir) al cine y _____ (ver) una película interesante.", "answer": "fui (indefinido), vi (indefinido)"}
        ]
    },
    "SER_ESTAR": {
        "title": "Ser vs. Estar",
        "explanation": """
**Ser** se usa para:
1. Identidad: "Soy Pedro"
2. Características esenciales/permanentes: "Es inteligente"
3. Posesión: "El libro es de Juan"
4. Tiempo: "Es lunes" / "Son las tres"
5. Origen: "Soy de España"
6. Materia: "La mesa es de madera"
7. Voz pasiva de acción: "El libro fue escrito por Cervantes"

**Estar** se usa para:
1. Ubicación: "Estoy en Madrid"
2. Estados temporales: "Estamos cansados"
3. Resultados de cambios: "La sopa está caliente"
4. Voz pasiva de estado: "La puerta está cerrada"
5. Con gerundio (acción continua): "Estoy estudiando"
        """,
        "examples": [
            "Ser: Él es alto. (He is tall - permanent characteristic)",
            "Estar: Él está feliz. (He is happy - temporary state)",
            "Ser: La película es buena. (The movie is good - quality)",
            "Estar: La película está en inglés. (The movie is in English - state)"
        ],
        "practice": [
            {"question": "Completa: Mi hermano _____ muy inteligente.", "options": ["es", "está"], "answer": "es"},
            {"question": "Completa: El café _____ frío.", "options": ["es", "está"], "answer": "está"},
            {"question": "Completa: La reunión _____ a las 10.", "options": ["es", "está"], "answer": "es"}
        ]
    },
    "Orthography": {
        "title": "Reglas de Acentuación",
        "explanation": """
**Reglas básicas de acentuación:**

1. **Palabras agudas:** Llevan acento gráfico cuando terminan en vocal, n o s.
   - Ejemplos: café, canción, compás

2. **Palabras llanas:** Llevan acento gráfico cuando NO terminan en vocal, n o s.
   - Ejemplos: árbol, lápiz, cárcel

3. **Palabras esdrújulas:** SIEMPRE llevan acento gráfico.
   - Ejemplos: lámpara, médico, teléfono

4. **Palabras sobreesdrújulas:** SIEMPRE llevan acento gráfico.
   - Ejemplos: cómetelo, explícaselo

**Otras reglas:**
- Hiatos con vocal cerrada tónica: baúl, país, oír
- Palabras interrogativas y exclamativas: qué, cómo, dónde, cuándo
        """,
        "examples": [
            "Aguda con acento: canción, café, japonés",
            "Llana con acento: árbol, cárcel, fácil",
            "Esdrújula: médico, pájaro, teléfono",
            "Sobreesdrújula: cuéntaselo, explícamelo"
        ],
        "practice": [
            {"question": "¿Dónde va el acento en la palabra 'examen'?", "answer": "Es llana y no lleva acento gráfico"},
            {"question": "¿Dónde va el acento en la palabra 'musica'?", "answer": "música (esdrújula)"},
            {"question": "¿Dónde va el acento en la palabra 'cafe'?", "answer": "café (aguda terminada en vocal)"}
        ]
    }
}

# Function to generate conversation summary
def generate_conversation_summary(history):
    try:
        messages = [
            {"role": "system", "content": """You are a helpful assistant that summarizes Spanish grammar learning sessions. 
            Create a concise summary of what the student has learned so far, what topics they've explored, 
            and what they might want to focus on next. Keep it under 150 words."""},
            {"role": "user", "content": f"Here's the conversation history between a student and the Spanish grammar tutor: {history}"}
        ]
        
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            max_tokens=250
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating summary: {str(e)}"

# Function to get personalized practice exercises
def generate_personalized_exercises(topic, difficulty):
    try:
        messages = [
            {"role": "system", "content": f"""You are a Spanish grammar tutor specializing in {topic}. 
            Create {3} personalized practice exercises at {difficulty} difficulty level. 
            Format the response as a JSON array with 'question' and 'answer' keys."""},
            {"role": "user", "content": f"Generate {difficulty} level exercises for {topic}"}
        ]
        
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            max_tokens=500
        )
        
        content = response.choices[0].message.content
        
        # Extract the JSON part from the response
        import re
        json_match = re.search(r'\[.*\]', content, re.DOTALL)
        if json_match:
            content = json_match.group(0)
        
        exercises = json.loads(content)
        return exercises
    except Exception as e:
        return [{"question": f"Error generating exercises: {str(e)}", "answer": "N/A"}]

# Function to get AI grammar tutor response
def ai_grammar_tutor(question, history):
    try:
        # Format the history for context
        formatted_history = []
        for entry in history:
            formatted_history.append({"role": "user", "content": entry[0]})
            if entry[1]:  # Check if there's a response
                formatted_history.append({"role": "assistant", "content": entry[1]})
        
        messages = [
            {"role": "system", "content": """You are a helpful, patient Spanish grammar tutor. 
            Explain concepts clearly with examples. When appropriate, include:
            1. Clear explanations of the grammar rule
            2. Several practical examples
            3. Common mistakes to avoid
            4. A simple practice exercise
            Keep your tone encouraging and your explanations concise."""}
        ] + formatted_history + [
            {"role": "user", "content": question}
        ]
        
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            max_tokens=800
        )
        
        content = response.choices[0].message.content
        
        return content
    except Exception as e:
        return f"Error with AI tutor: {str(e)}"

# Function to analyze student errors
def analyze_errors(student_text):
    try:
        messages = [
            {"role": "system", "content": """You are a Spanish grammar checker. 
            Analyze the provided text for grammar, spelling, and usage errors. 
            Provide corrections and brief explanations for each error found.
            Format your response with clear sections for each type of error."""},
            {"role": "user", "content": f"Please check this Spanish text for errors: {student_text}"}
        ]
        
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            max_tokens=500
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error analyzing text: {str(e)}"

# Function to translate text
def translate_text(text, direction):
    try:
        if direction == "en_to_es":
            source = "English"
            target = "Spanish"
            system_prompt = "You are a translator from English to Spanish."
        else:
            source = "Spanish"
            target = "English"
            system_prompt = "You are a translator from Spanish to English."
            
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Translate this {source} text to {target}: {text}"}
        ]
        
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            max_tokens=500
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error translating text: {str(e)}"

# Function to get a random quiz question
def get_random_quiz(topic):
    if topic in STUDY_GUIDE:
        practice_items = STUDY_GUIDE[topic].get("practice", [])
        if practice_items:
            return random.choice(practice_items)
    return {"question": "No quizzes available for this topic.", "answer": ""}

# Memory optimization function
def optimize_memory():
    gc.collect()
    return True

# Main Gradio interface
with gr.Blocks(theme=gr.themes.Soft()) as interface:
    # Session state for conversation history
    conversation_history = gr.State([])
    
    # Header
    gr.Markdown("# 🇪🇸 Spanish Grammar AI Tutor 📚")
    gr.Markdown("### Learn Spanish grammar interactively with AI assistance!")
    
    with gr.Tabs():
        # Study Guide Tab
        with gr.Tab("📖 Study Guide"):
            with gr.Row():
                topic_dropdown = gr.Dropdown(
                    choices=list(STUDY_GUIDE.keys()), 
                    label="Select a Grammar Topic",
                    value="Imperative"
                )
            
            with gr.Row():
                with gr.Column(scale=2):
                    title_output = gr.Markdown("## Topic Title")
                    explanation_output = gr.Markdown("Explanation will appear here...")
                
                with gr.Column(scale=1):
                    examples_output = gr.Markdown("### Examples")
            
            with gr.Row():
                practice_output = gr.JSON(label="Practice Exercises")
                
            with gr.Row():
                practice_level = gr.Radio(
                    ["Beginner", "Intermediate", "Advanced"], 
                    label="Practice Level",
                    value="Beginner"
                )
                generate_practice_btn = gr.Button("📝 Generate Custom Practice")
            
            with gr.Row():
                custom_practice_output = gr.JSON(label="Custom Practice Exercises")
        
        # Interactive Practice Tab
        with gr.Tab("🎯 Practice & Quiz"):
            with gr.Row():
                quiz_topic = gr.Dropdown(
                    choices=list(STUDY_GUIDE.keys()), 
                    label="Select Topic for Quiz",
                    value="Imperative"
                )
                quiz_btn = gr.Button("Get New Question")
            
            with gr.Row():
                quiz_question = gr.Markdown("### Question will appear here...")
            
            with gr.Row():
                quiz_answer_input = gr.Textbox(label="Your Answer")
                check_answer_btn = gr.Button("Check Answer")
            
            with gr.Row():
                quiz_feedback = gr.Markdown("Feedback will appear here...")
                
            with gr.Accordion("Grammar Challenge", open=False):
                challenge_description = gr.Markdown("""
                # 🏆 Weekly Grammar Challenge
                Complete these exercises to test your understanding of Spanish grammar concepts.
                """)
                challenge_questions = gr.JSON({
                    "questions": [
                        {"id": 1, "text": "Completa con la forma correcta del verbo: Yo _____ (hablar) español todos los días."},
                        {"id": 2, "text": "Elige la opción correcta: El libro está ____ la mesa. (a) en (b) sobre (c) de"},
                        {"id": 3, "text": "Traduce: 'I would go if I had time.'"}
                    ]
                })
                challenge_submit_btn = gr.Button("Submit Challenge Answers")
        
        # AI Tutor Tab
        with gr.Tab("🤖 AI Tutor"):
            with gr.Row():
                with gr.Column(scale=3):
                    chatbot = gr.Chatbot(label="Conversation with Spanish Tutor")
                
                with gr.Column(scale=1):
                    session_info = gr.Markdown("""
                    ### Session Info
                    - Current level: Beginner
                    - Topics covered: 0
                    - Questions asked: 0
                    """)
                    
                    summary_btn = gr.Button("📊 Generate Session Summary")
                    session_summary = gr.Textbox(label="Session Summary", interactive=False)
            
            with gr.Row():
                user_input = gr.Textbox(label="Ask about Spanish grammar", placeholder="Type your question here...")
                submit_btn = gr.Button("Submit")
                clear_btn = gr.Button("Clear Conversation")
        
        # Tools Tab
        with gr.Tab("🔧 Tools"):
            with gr.Accordion("Text Correction", open=True):
                with gr.Row():
                    correction_input = gr.Textbox(
                        label="Enter Spanish text to check for errors",
                        placeholder="Mi amigo es estudiando español desde hace dos años.",
                        lines=5
                    )
                    correction_btn = gr.Button("Check Text")
                
                with gr.Row():
                    correction_output = gr.Markdown("Corrections will appear here...")
            
            with gr.Accordion("Translation Tool", open=False):
                with gr.Row():
                    translation_input = gr.Textbox(
                        label="Text to translate",
                        placeholder="Enter text to translate...",
                        lines=3
                    )
                    translation_direction = gr.Radio(
                        ["English to Spanish", "Spanish to English"],
                        label="Translation Direction",
                        value="English to Spanish"
                    )
                    translation_btn = gr.Button("Translate")
                
                with gr.Row():
                    translation_output = gr.Textbox(label="Translation", interactive=False)
            
            with gr.Accordion("Vocabulary Builder", open=False):
                with gr.Row():
                    vocab_topic = gr.Textbox(
                        label="Enter a topic for vocabulary", 
                        placeholder="e.g., food, travel, business"
                    )
                    vocab_level = gr.Radio(
                        ["Beginner", "Intermediate", "Advanced"], 
                        label="Vocabulary Level",
                        value="Beginner"
                    )
                    vocab_btn = gr.Button("Generate Vocabulary List")
                
                with gr.Row():
                    vocab_output = gr.Dataframe(
                        headers=["Spanish", "English", "Example Sentence"],
                        datatype=["str", "str", "str"],
                        label="Vocabulary List"
                    )
        
        # Resources Tab
        with gr.Tab("📚 Resources"):
            gr.Markdown("""
            # Additional Spanish Learning Resources
            
            ## Recommended Books
            - "Complete Spanish Grammar" by Practice Makes Perfect
            - "Madrigal's Magic Key to Spanish" by Margarita Madrigal
            - "Spanish Verbs Made Simple(r)" by David Brodsky
            
            ## Online Resources
            - SpanishDict.com - Dictionary and conjugation tables
            - StudySpanish.com - Free grammar lessons
            - Notes in Spanish - Podcast for learners
            - Language Transfer - Free audio course
            
            ## YouTube Channels
            - Butterfly Spanish
            - Why Not Spanish
            - Spanish with Vicente
            - Dreaming Spanish
            
            ## Practice Communities
            - r/Spanish subreddit
            - Tandem language exchange app
            - HelloTalk language exchange app
            """)
    
    # Event handlers
    def update_topic_info(topic):
        if topic in STUDY_GUIDE:
            title = f"## {STUDY_GUIDE[topic]['title']}"
            explanation = STUDY_GUIDE[topic]['explanation']
            examples = "### Examples\n" + "\n".join([f"- {ex}" for ex in STUDY_GUIDE[topic]['examples']])
            practice = STUDY_GUIDE[topic]['practice']
            return title, explanation, examples, practice
        return "## Topic Not Found", "Please select a valid topic.", "### No examples available", []
    
    def update_quiz_question(topic):
        quiz = get_random_quiz(topic)
        question_md = f"### {quiz['question']}"
        if "options" in quiz:
            options_text = "\n".join([f"- {opt}" for opt in quiz["options"]])
            question_md += f"\n\n{options_text}"
        return question_md, ""  # Reset feedback when getting new question
    
    def check_quiz_answer(topic, answer_input, question_md):
        # Extract just the question from the markdown
        import re
        question_text = re.sub(r'###\s+', '', question_md.split('\n')[0])
        
        # Find the matching practice item
        correct_answer = ""
        for practice_item in STUDY_GUIDE.get(topic, {}).get("practice", []):
            if practice_item["question"] in question_text:
                correct_answer = practice_item["answer"]
                break
        
        if not correct_answer:
            return "⚠️ Couldn't find the answer for this question."
        
        # Check if answer is correct (case insensitive)
        if answer_input.lower().strip() == correct_answer.lower().strip():
            return "✅ ¡Correcto! Your answer is correct."
        else:
            return f"❌ Not quite. The correct answer is: **{correct_answer}**"
    
    def handle_chat_submit(message, history, conv_history):
        # Add user message to history
        history.append((message, None))
        
        # Get AI response
        response = ai_grammar_tutor(message, conv_history)
        
        # Update history
        history[-1] = (message, response)
        conv_history.append((message, response))
        
        # Return updated history and empty the input
        return "", history, conv_history
    
    def get_session_summary(conv_history):
        return generate_conversation_summary(conv_history)
    
    def clear_chat_history():
        return [], []
    
    def handle_error_analysis(text):
        return analyze_errors(text)
    
    def handle_translation(text, direction):
        direction_key = "en_to_es" if direction == "English to Spanish" else "es_to_en"
        return translate_text(text, direction_key)
    
    def generate_vocabulary(topic, level):
        try:
            messages = [
                {"role": "system", "content": f"""You are a Spanish vocabulary builder. 
                Create a list of 10 useful {level} level Spanish vocabulary words related to '{topic}'.
                For each word, provide the Spanish term, English translation, and a simple example sentence in Spanish.
                Format as a JSON array with 'spanish', 'english', and 'example' keys."""},
                {"role": "user", "content": f"Generate {level} vocabulary list for the topic: {topic}"}
            ]
            
            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                max_tokens=800
            )
            
            content = response.choices[0].message.content
            
            # Extract the JSON part
            import re
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                content = json_match.group(0)
            
            vocab_list = json.loads(content)
            
            # Format for dataframe
            df_data = [[item["spanish"], item["english"], item["example"]] for item in vocab_list]
            return df_data
        except Exception as e:
            return [["Error", f"Error generating vocabulary: {str(e)}", ""]]
    
    def get_custom_exercises(topic, level):
        return generate_personalized_exercises(topic, level)
    
    # Connect event handlers
    topic_dropdown.change(update_topic_info, inputs=topic_dropdown, outputs=[title_output, explanation_output, examples_output, practice_output])
    
    quiz_topic.change(update_quiz_question, inputs=quiz_topic, outputs=[quiz_question, quiz_feedback])
    quiz_btn.click(update_quiz_question, inputs=quiz_topic, outputs=[quiz_question, quiz_feedback])
    check_answer_btn.click(check_quiz_answer, inputs=[quiz_topic, quiz_answer_input, quiz_question], outputs=quiz_feedback)
    
    submit_btn.click(handle_chat_submit, inputs=[user_input, chatbot, conversation_history], outputs=[user_input, chatbot, conversation_history])
    user_input.submit(handle_chat_submit, inputs=[user_input, chatbot, conversation_history], outputs=[user_input, chatbot, conversation_history])
    clear_btn.click(clear_chat_history, outputs=[chatbot, conversation_history])
    
    summary_btn.click(get_session_summary, inputs=conversation_history, outputs=session_summary)
    
    correction_btn.click(handle_error_analysis, inputs=correction_input, outputs=correction_output)
    
    translation_btn.click(handle_translation, inputs=[translation_input, translation_direction], outputs=translation_output)
    
    vocab_btn.click(generate_vocabulary, inputs=[vocab_topic, vocab_level], outputs=vocab_output)
    
    generate_practice_btn.click(get_custom_exercises, inputs=[topic_dropdown, practice_level], outputs=custom_practice_output)

# Launch the interface
interface.launch(share=True)

@app.route("/generate-custom-exercise", methods=["POST"])
def generate_custom_exercise():
    data = request.get_json()
    prompt = data.get("prompt", "Create a Spanish grammar exercise.")

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",  # Replace with "gpt-3.5-turbo" if needed
            messages=[
                {"role": "system", "content": "You are a Spanish grammar tutor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        reply = response.choices[0].message.content.strip()

        return jsonify({
            "question": prompt,
            "answer": reply
        })

    except Exception as e:
        return jsonify({
            "question": "Unexpected error occurred.",
            "answer": str(e)
        })