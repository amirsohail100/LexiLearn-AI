import streamlit as st
from backend import respone  # तुम्हारे बैकएंड फंक्शन को इम्पोर्ट किया

def render_ui():
    st.set_page_config(page_title="LingoBot-AI", page_icon="🤖", layout="wide")
    
    st.title("🤖 LingoBot-AI: Your Personal Language Tutor")
    st.markdown("Learn a new language interactively with AI, just like Duolingo!")
    st.write("---")

    # 1. SIDEBAR - सेटिंग्स और कंट्रोल्स
    with st.sidebar:
        st.header("⚙️ Learning Settings")
        
        # 10 भाषाओं का ड्रॉपडाउन ऑप्शन
        languages = [
            "English", "Spanish", "French", "German", "Italian", 
            "Japanese", "Korean", "Mandarin", "Arabic", "Hindi"
        ]
        target_language = st.selectbox(
            "Which language do you want to learn?", 
            options=languages, 
            index=0
        )
        
        # डिफिकल्टी लेवल्स के लिए रेडियो बटन्स
        level = st.radio(
            "Select Difficulty Level:",
            options=["Easy", "Medium", "Hard"],
            index=0
        )
        
        st.write("---")
        # चैट रीसेट करने का बटन
        if st.button("🔄 Reset Conversation", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

    # 2. SESSION STATE - चैट हिस्ट्री मैनेजमेंट
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # 3. CHAT INTERFACE - पुराने मैसेजेस स्क्रीन पर दिखाना
    # यहाँ हम लैंगचेन के संदेशों (AIMessage/HumanMessage) के हिसाब से आइकन सेट कर रहे हैं
    for message in st.session_state.chat_history:
        # सिस्टम मैसेज को स्क्रीन पर नहीं दिखाना है, सिर्फ AI और Human को दिखाना है
        if message.__class__.__name__ == "HumanMessage":
            with st.chat_message("user"):
                st.write(message.content)
        elif message.__class__.__name__ == "AIMessage":
            with st.chat_message("assistant", avatar="🤖"):
                st.write(message.content)

    # 4. CHAT INPUT - यूज़र का इनपुट बॉक्स
    if user_input := st.chat_input(f"Type your response or say hello in {target_language}..."):
        
        # यूज़र का मैसेज स्क्रीन पर तुरंत दिखाओ
        with st.chat_message("user"):
            st.write(user_input)
            
        # बैकएंड से रिस्पॉन्स लाने के लिए स्पिनर (लोडिंग) चलाओ
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Tutor is thinking..."):
                # तुम्हारे बैकएंड फंक्शन को कॉल किया
                ai_response = respone(
                    user_input=user_input,
                    chat_hist=st.session_state.chat_history,
                    level=level,
                    target_language=target_language
                )
                st.write(ai_response)

        # स्क्रीन को रिफ्रेश करें ताकि चैट हिस्ट्री अपडेट हो जाए
        st.rerun()