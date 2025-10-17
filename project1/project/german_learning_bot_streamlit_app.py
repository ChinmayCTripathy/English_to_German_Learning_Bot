import streamlit as st
import google.generativeai as genai
from elevenlabs.client import ElevenLabs
import base64
import random

# Configure page
st.set_page_config(
    page_title="🇩🇪 German Learning Bot",
    page_icon="🇩🇪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configure APIs (replace with your keys or env vars)
genai.configure(api_key="AIzaSyBfSvYFOjwFYrX_zGbiuA3Ll9TZVaDuK58")

client = ElevenLabs(
    api_key="sk_4cb7e1f08d18994115ba660ea2fa2829bf0b9a042b5d5c56"
)


class GermanLearningBotWeb:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        # German ElevenLabs voice id
        self.german_voice_id = "nzeAacJi50IvxcyDnMXa"

        if 'user_progress' not in st.session_state:
            st.session_state.user_progress = {
                "level": "beginner",
                "vocabulary_learned": [],
                "lessons_completed": [],
                "session_count": 0,
                "current_score": 0
            }

        if 'conversation_memory' not in st.session_state:
            st.session_state.conversation_memory = []

        if 'current_page' not in st.session_state:
            st.session_state.current_page = "Home"

        self.vocabulary_sets = {
            "beginner": [
                {"german": "Hallo", "english": "Hello", "pronunciation": "hah-lo"},
                {"german": "Danke", "english": "Thank you", "pronunciation": "dahn-keh"},
                {"german": "Tschüss", "english": "Goodbye", "pronunciation": "chooss"},
                {"german": "Ja", "english": "Yes", "pronunciation": "yah"},
                {"german": "Nein", "english": "No", "pronunciation": "nine"},
                {"german": "Bitte", "english": "Please/You're welcome", "pronunciation": "bit-teh"},
                {"german": "Entschuldigung", "english": "Excuse me/Sorry", "pronunciation": "ent-shool-dee-goong"},
                {"german": "Ich heiße", "english": "My name is", "pronunciation": "ikh hye-seh"},
                {"german": "Wie geht's?", "english": "How are you?", "pronunciation": "vee gates"},
                {"german": "Gut", "english": "Good", "pronunciation": "goot"}
            ],
            "intermediate": [
                {"german": "Wo ist die Bibliothek?", "english": "Where is the library?", "pronunciation": "vo ist dee bib-lee-oh-tek"},
                {"german": "Wieviel kostet das?", "english": "How much does it cost?", "pronunciation": "vee-feel kos-tet duss"},
                {"german": "Ich möchte", "english": "I would like", "pronunciation": "ikh merkh-teh"},
                {"german": "Können Sie mir helfen?", "english": "Can you help me?", "pronunciation": "ker-nen zee meer hel-fen"},
                {"german": "Ich verstehe nicht", "english": "I don't understand", "pronunciation": "ikh fer-shteh-heh nikht"}
            ]
        }

    def ask_gemini(self, prompt, system_prompt=""):
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        response = self.model.generate_content(full_prompt)
        return response.text

    def speak_german(self, text):
        try:
            audio = client.text_to_speech.convert(
                text=text,
                voice_id=self.german_voice_id,
                model_id="eleven_multilingual_v2",
                output_format="mp3_44100_128",
            )
            audio_base64 = base64.b64encode(audio).decode()
            audio_html = f"""
            <audio autoplay controls style="width: 100%;">
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                Your browser does not support the audio element.
            </audio>
            """
            return audio_html
        except Exception as e:
            st.error(f"❌ Audio error: {e}")
            return None

    def display_progress_sidebar(self):
        with st.sidebar:
            st.header("📊 Your Progress")
            progress = st.session_state.user_progress
            level_emoji = "🟢" if progress["level"] == "beginner" else "🟡" if progress["level"] == "intermediate" else "🔴"
            st.markdown(f"**{level_emoji} Level:** {progress['level'].title()}")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("📚 Vocabulary", len(progress["vocabulary_learned"]))
            with col2:
                st.metric("📖 Lessons", len(progress["lessons_completed"]))
            vocab_target = 10 if progress["level"] == "beginner" else 20
            vocab_progress = min(len(progress["vocabulary_learned"]) / vocab_target, 1.0)
            st.progress(vocab_progress)
            st.caption(f"Progress to next level: {len(progress['vocabulary_learned'])}/{vocab_target}")
            if progress["vocabulary_learned"]:
                st.subheader("🎯 Recent Words")
                for word in progress["vocabulary_learned"][-3:]:
                    st.write(f"• {word}")

    def home_page(self):
        st.title("🇩🇪 German Learning Bot")
        st.subheader("Willkommen! Start your interactive German learning journey!")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
            ### 🎯 What you'll learn:
            - **📚 Interactive Lessons** - Structured German lessons with explanations
            - **📝 Vocabulary Practice** - Essential German words with pronunciation
            - **🗣️ Pronunciation Training** - Practice speaking German phrases
            - **💬 Conversation Simulation** - Real German conversations
            - **🎯 Quiz Challenges** - Test your knowledge
            - **❓ Ask Questions** - Get answers about German language and culture
            """)
        with col2:
            st.image("https://via.placeholder.com/300x200/000000/FFFFFF?text=🇩🇪+Deutsch",
                    caption="Start your German journey!", use_container_width=True)
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🎓 Current Level", st.session_state.user_progress["level"].title())
        with col2:
            st.metric("📚 Vocabulary Learned", len(st.session_state.user_progress["vocabulary_learned"]))
        with col3:
            st.metric("📖 Lessons Completed", len(st.session_state.user_progress["lessons_completed"]))
        with col4:
            st.metric("🔄 Sessions", st.session_state.user_progress["session_count"])
        st.markdown("---")
        st.subheader("🚀 Ready to start learning?")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📚 Start Interactive Lesson", type="primary", use_container_width=True):
                st.session_state.current_page = "Interactive Lesson"
                st.rerun()
        with col2:
            if st.button("📝 Practice Vocabulary", use_container_width=True):
                st.session_state.current_page = "Vocabulary Practice"
                st.rerun()
        with col3:
            if st.button("🗣️ Pronunciation Practice", use_container_width=True):
                st.session_state.current_page = "Pronunciation Practice"
                st.rerun()

    def interactive_lesson_page(self):
        st.title("📚 Interactive German Lesson")
        level = st.session_state.user_progress["level"]
        if st.button("🏠 Back to Home"):
            st.session_state.current_page = "Home"
            st.rerun()
        st.markdown(f"**Level:** {level.title()}")
        if st.button("🎓 Generate New Lesson", type="primary"):
            with st.spinner("Creating your German lesson..."):
                lesson_prompt = f"""
                You are a German teacher. Create a short, engaging German lesson for a {level} student.
                Include:
                1. A brief explanation of a German concept (grammar, culture, or usage)
                2. 2-3 example sentences in German with English translations
                3. A simple exercise for the student to try
                Keep it conversational and encouraging. End with asking the student to try the exercise.
                """
                lesson = self.ask_gemini("Create a German lesson", lesson_prompt)
                st.session_state.current_lesson = lesson
        if hasattr(st.session_state, 'current_lesson'):
            st.markdown("### 📖 Your Lesson:")
            st.write(st.session_state.current_lesson)
            st.markdown("### 🔊 Listen:")
            audio_html = self.speak_german("Hier ist deine Deutschstunde!")
            if audio_html:
                st.markdown(audio_html, unsafe_allow_html=True)
            st.markdown("### 💡 Your Turn:")
            user_answer = st.text_area("Write your answer to the exercise above:",
                                     placeholder="Type your response here...")
            if st.button("✅ Submit Answer") and user_answer:
                with st.spinner("Getting feedback..."):
                    feedback_prompt = f"""
                    The student attempted this exercise: {user_answer}
                    Provide encouraging feedback and gentle corrections if needed.
                    Always be positive and motivating.
                    """
                    feedback = self.ask_gemini(feedback_prompt)
                    st.success("📝 Teacher Feedback:")
                    st.write(feedback)
                    lesson_id = f"Lesson_{len(st.session_state.user_progress['lessons_completed'])+1}"
                    if lesson_id not in st.session_state.user_progress['lessons_completed']:
                        st.session_state.user_progress['lessons_completed'].append(lesson_id)

    def vocabulary_practice_page(self):
        st.title("📝 Vocabulary Practice")
        if st.button("🏠 Back to Home"):
            st.session_state.current_page = "Home"
            st.rerun()
        level = st.session_state.user_progress["level"]
        vocab_set = self.vocabulary_sets.get(level, self.vocabulary_sets['beginner'])
        st.markdown(f"**Level:** {level.title()}")
        st.markdown("Practice essential German vocabulary with pronunciation!")
        if 'vocab_index' not in st.session_state:
            st.session_state.vocab_index = 0
        if 'vocab_score' not in st.session_state:
            st.session_state.vocab_score = 0
        word_data = vocab_set[st.session_state.vocab_index % len(vocab_set)]
        st.markdown("---")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"### 🇩🇪 {word_data['german']}")
            st.markdown(f"**📝 Pronunciation:** _{word_data['pronunciation']}_")
            audio_html = self.speak_german(word_data['german'])
            if audio_html:
                st.markdown(audio_html, unsafe_allow_html=True)
        with col2:
            st.metric("Current Score", st.session_state.vocab_score)
            st.metric("Word", f"{st.session_state.vocab_index + 1}/{len(vocab_set)}")
        st.markdown("### 🤔 What does this mean in English?")
        user_guess = st.text_input("Your answer:", key=f"guess_{st.session_state.vocab_index}")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("✅ Check Answer", type="primary"):
                if user_guess.lower().strip() == word_data['english'].lower().strip():
                    st.success("🎉 Correct! Excellent!")
                    st.session_state.vocab_score += 1
                    if word_data['german'] not in st.session_state.user_progress['vocabulary_learned']:
                        st.session_state.user_progress['vocabulary_learned'].append(word_data['german'])
                else:
                    st.error(f"❌ Not quite. The correct answer is: **{word_data['english']}**")
                st.markdown(f"**📖 Meaning:** {word_data['english']}")
        with col2:
            if st.button("➡️ Next Word"):
                st.session_state.vocab_index += 1
                st.rerun()
        with col3:
            if st.button("🔀 Random Word"):
                st.session_state.vocab_index = random.randint(0, len(vocab_set) - 1)
                st.rerun()

    def pronunciation_practice_page(self):
        st.title("🗣️ Pronunciation Practice")
        if st.button("🏠 Back to Home"):
            st.session_state.current_page = "Home"
            st.rerun()
        phrases = [
            {"german": "Ich bin glücklich", "english": "I am happy"},
            {"german": "Schönen Tag noch", "english": "Have a good day"},
            {"german": "Wie heißen Sie?", "english": "What is your name?"},
            {"german": "Ich lerne gerne Deutsch", "english": "I love learning German"},
            {"german": "Wo ist der Bahnhof?", "english": "Where is the train station?"},
            {"german": "Können Sie das wiederholen?", "english": "Can you repeat?"}
        ]
        if 'current_phrase' not in st.session_state:
            st.session_state.current_phrase = random.choice(phrases)
        phrase = st.session_state.current_phrase
        st.markdown("### 🎯 Practice this phrase:")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"### 🇩🇪 {phrase['german']}")
            st.markdown(f"**🇺🇸 English:** {phrase['english']}")
        with col2:
            if st.button("🔀 New Phrase"):
                st.session_state.current_phrase = random.choice(phrases)
                st.rerun()
        st.markdown("### 🔊 Listen carefully:")
        audio_html = self.speak_german(phrase['german'])
        if audio_html:
            st.markdown(audio_html, unsafe_allow_html=True)
        st.markdown("### 🎤 Now you try!")
        st.info("💡 Tip: Use your browser's voice recording or speak the phrase out loud, then type what you said below.")
        user_pronunciation = st.text_area("Type what you said (or your attempt):",
                                        placeholder="Type your pronunciation attempt here...")
        if st.button("📝 Get Pronunciation Feedback") and user_pronunciation:
            with st.spinner("Analyzing your pronunciation..."):
                feedback_prompt = f"""
                The student is practicing German pronunciation.
                They attempted to say: "{phrase['german']}"
                They typed: "{user_pronunciation}"
                Provide encouraging feedback about their pronunciation attempt.
                Give tips for improvement if needed. Be positive and motivating.
                """
                feedback = self.ask_gemini(feedback_prompt)
                st.success("👨‍🏫 Pronunciation Feedback:")
                st.write(feedback)

    def conversation_practice_page(self):
        st.title("💬 Conversation Practice")
        if st.button("🏠 Back to Home"):
            st.session_state.current_page = "Home"
            st.rerun()
        st.markdown("🤖 I'll play a German character. Try to respond in German!")
        if 'conversation_started' not in st.session_state:
            st.session_state.conversation_started = False
        if 'conversation_history' not in st.session_state:
            st.session_state.conversation_history = []
        if not st.session_state.conversation_started:
            if st.button("🗣️ Start Conversation", type="primary"):
                level = st.session_state.user_progress["level"]
                conversation_prompt = f"""
                You are a friendly German person having a casual conversation with a {level} German learner.
                Start a simple conversation in German. Include the English translation in parentheses.
                Keep sentences simple and encourage the learner.
                Ask questions that prompt responses.
                """
                with st.spinner("Starting conversation..."):
                    greeting = self.ask_gemini("Start a friendly German conversation", conversation_prompt)
                    st.session_state.conversation_history.append(("🇩🇪 German Friend", greeting))
                    st.session_state.conversation_started = True
                    st.rerun()
        if st.session_state.conversation_history:
            st.markdown("### 💭 Conversation:")
            for speaker, message in st.session_state.conversation_history:
                if speaker == "🇩🇪 German Friend":
                    st.markdown(f"**{speaker}:** {message}")
                    german_part = message.split('(')[0].strip()
                    audio_html = self.speak_german(german_part)
                    if audio_html:
                        st.markdown(audio_html, unsafe_allow_html=True)
                else:
                    st.markdown(f"**{speaker}:** {message}")
                st.markdown("---")
        if st.session_state.conversation_started:
            st.markdown("### 🗣️ Your Response:")
            user_response = st.text_area("Respond in German:",
                                       placeholder="Type your response in German here...")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💬 Send Response") and user_response:
                    st.session_state.conversation_history.append(("🗣️ You", user_response))
                    with st.spinner("Thinking of response..."):
                        response_prompt = f"""
                        Continue the German conversation. The learner said: "{user_response}"
                        Respond naturally in German with English translation in parentheses.
                        Give gentle corrections if needed.
                        Ask a follow-up question to continue the conversation.
                        """
                        conversation_prompt = f"""
                        You are a friendly German person having a casual conversation with a {st.session_state.user_progress['level']} German learner.
                        """
                        ai_response = self.ask_gemini(response_prompt, conversation_prompt)
                        st.session_state.conversation_history.append(("🇩🇪 German Friend", ai_response))
                        st.rerun()
            with col2:
                if st.button("❓ Need Help?"):
                    help_prompt = "Suggest a simple German response for a beginner in this conversation context."
                    help_response = self.ask_gemini(help_prompt)
                    st.info(f"💡 Suggestion: {help_response}")
            if st.button("🔄 Start New Conversation"):
                st.session_state.conversation_started = False
                st.session_state.conversation_history = []
                st.rerun()

    def quiz_page(self):
        st.title("🎯 German Quiz")
        if st.button("🏠 Back to Home"):
            st.session_state.current_page = "Home"
            st.rerun()
        if 'quiz_started' not in st.session_state:
            st.session_state.quiz_started = False
        if 'quiz_score' not in st.session_state:
            st.session_state.quiz_score = 0
        if 'quiz_question_count' not in st.session_state:
            st.session_state.quiz_question_count = 0
        total_questions = 5
        if not st.session_state.quiz_started:
            st.markdown("### 🧠 Test your German knowledge!")
            st.markdown(f"**Quiz:** {total_questions} questions")
            st.markdown(f"**Level:** {st.session_state.user_progress['level'].title()}")
            if st.button("🚀 Start Quiz", type="primary"):
                st.session_state.quiz_started = True
                st.session_state.quiz_score = 0
                st.session_state.quiz_question_count = 0
                st.rerun()
        else:
            if st.session_state.quiz_question_count < total_questions:
                if 'current_question' not in st.session_state:
                    level = st.session_state.user_progress["level"]
                    quiz_prompt = f"""
                    Create a German quiz question for a {level} student.
                    Types of questions you can ask:
                    - Translate German to English
                    - Translate English to German
                    - Fill in the blank
                    - Multiple choice
                    Provide the question and the correct answer clearly.
                    """
                    question = self.ask_gemini("Generate a German quiz question", quiz_prompt)
                    st.session_state.current_question = question
                st.markdown(f"### Question {st.session_state.quiz_question_count + 1}/{total_questions}")
                st.write(st.session_state.current_question)
                user_answer = st.text_input("Your answer:", key=f"quiz_answer_{st.session_state.quiz_question_count}")
                if st.button("✅ Submit Answer") and user_answer:
                    check_prompt = f"""
                    Question: {st.session_state.current_question}
                    Student answered: {user_answer}
                    Is this correct? Respond with either "CORRECT" or "INCORRECT" followed by the explanation.
                    """
                    result = self.ask_gemini(check_prompt)
                    if "CORRECT" in result.upper():
                        st.success("🎉 Correct! Well done!")
                        st.session_state.quiz_score += 1
                    else:
                        st.error(f"❌ {result}")
                    st.session_state.quiz_question_count += 1
                    del st.session_state.current_question
                    if st.session_state.quiz_question_count < total_questions:
                        if st.button("➡️ Next Question"):
                            st.rerun()
                    else:
                        st.rerun()
            else:
                st.markdown("### 🏆 Quiz Complete!")
                score = st.session_state.quiz_score
                col1, col2, col3 = st.columns(3)
                with col2:
                    st.metric("Final Score", f"{score}/{total_questions}")
                if score == total_questions:
                    st.balloons()
                    st.success("🌟 Perfect score! Excellent work!")
                    audio_html = self.speak_german("Herzlichen Glückwunsch! Großartige Arbeit!")
                    if audio_html:
                        st.markdown(audio_html, unsafe_allow_html=True)
                elif score >= total_questions // 2:
                    st.success("👍 Good job! Keep practicing!")
                    audio_html = self.speak_german("Gute Arbeit!")
                    if audio_html:
                        st.markdown(audio_html, unsafe_allow_html=True)
                else:
                    st.info("📚 Keep studying! You'll improve!")
                    audio_html = self.speak_german("Weiter so mit dem Lernen!")
                    if audio_html:
                        st.markdown(audio_html, unsafe_allow_html=True)
                if st.button("🔄 Take Another Quiz"):
                    st.session_state.quiz_started = False
                    st.session_state.quiz_score = 0
                    st.session_state.quiz_question_count = 0
                    st.rerun()

    def ask_questions_page(self):
        st.title("❓ Ask German Questions")
        if st.button("🏠 Back to Home"):
            st.session_state.current_page = "Home"
            st.rerun()
        st.markdown("### 🧑‍🏫 Ask me anything about German!")
        st.markdown("**Examples:** 'How do you say...', 'What's the difference between...', 'German culture question'")
        if 'qa_history' not in st.session_state:
            st.session_state.qa_history = []
        user_question = st.text_area("Your question:",
                                   placeholder="Ask your German question here...")
        if st.button("🤔 Ask Question", type="primary") and user_question:
            with st.spinner("Thinking..."):
                german_expert_prompt = f"""
                You are an expert German teacher and cultural guide.
                Answer this question about German language, culture, or learning:
                {user_question}
                Provide a clear, helpful answer with examples if relevant.
                If it's about pronunciation, include phonetic guidance.
                If it's about culture, be informative and interesting.
                """
                answer = self.ask_gemini(user_question, german_expert_prompt)
                st.session_state.qa_history.append((user_question, answer))
                st.rerun()
        if st.session_state.qa_history:
            st.markdown("### 💭 Q&A History:")
            for i, (question, answer) in enumerate(reversed(st.session_state.qa_history)):
                with st.expander(f"Q{len(st.session_state.qa_history)-i}: {question[:50]}..."):
                    st.markdown(f"**❓ Question:** {question}")
                    st.markdown(f"**🧑‍🏫 Answer:** {answer}")
                    if any(char in answer for char in 'äöüßÄÖÜ') or 'deutsch' in answer.lower():
                        german_text = st.text_input(f"Type German text to pronounce:",
                                                   key=f"pronounce_{i}")
                        if st.button(f"🔊 Pronounce", key=f"btn_{i}") and german_text:
                            audio_html = self.speak_german(german_text)
                            if audio_html:
                                st.markdown(audio_html, unsafe_allow_html=True)


def main():
    bot = GermanLearningBotWeb()
    bot.display_progress_sidebar()
    with st.sidebar:
        st.markdown("---")
        st.header("🧭 Navigation")
        nav_options = [
            "Home",
            "Interactive Lesson",
            "Vocabulary Practice",
            "Pronunciation Practice",
            "Conversation Practice",
            "Quiz",
            "Ask Questions"
        ]
        selected_page = st.selectbox("Choose a page:", nav_options,
                                   index=nav_options.index(st.session_state.current_page))
        if selected_page != st.session_state.current_page:
            st.session_state.current_page = selected_page
            st.rerun()
    if st.session_state.current_page == "Home":
        bot.home_page()
    elif st.session_state.current_page == "Interactive Lesson":
        bot.interactive_lesson_page()
    elif st.session_state.current_page == "Vocabulary Practice":
        bot.vocabulary_practice_page()
    elif st.session_state.current_page == "Pronunciation Practice":
        bot.pronunciation_practice_page()
    elif st.session_state.current_page == "Conversation Practice":
        bot.conversation_practice_page()
    elif st.session_state.current_page == "Quiz":
        bot.quiz_page()
    elif st.session_state.current_page == "Ask Questions":
        bot.ask_questions_page()
    st.markdown("---")
    st.markdown("🇩🇪 **German Learning Bot** - Made with ❤️ using Streamlit, Gemini AI, and ElevenLabs")


if __name__ == "__main__":
    main()


