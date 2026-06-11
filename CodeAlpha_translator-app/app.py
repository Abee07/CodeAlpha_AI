import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import io
import base64

# Page configuration
st.set_page_config(
    page_title="Language Translator",
    page_icon="🌐",
    layout="wide"
)

# Title and description
st.title("🌐 Language Translator")
st.markdown("Translate text between different languages using Google Translate API")

# Language options
languages = GoogleTranslator().get_supported_languages()
language_dict = GoogleTranslator().get_supported_languages(as_dict=True)

# Create columns for layout
col1, col2 = st.columns([1, 1])

with col1:
    source_lang = st.selectbox(
        "Source Language",
        options=list(language_dict.keys()),
        index=list(language_dict.keys()).index("english"),
        key="source_lang"
    )

with col2:
    target_lang = st.selectbox(
        "Target Language",
        options=list(language_dict.keys()),
        index=list(language_dict.keys()).index("spanish"),
        key="target_lang"
    )

# Clear translation if languages have changed
if st.session_state.get("last_source_lang_widget") != source_lang or st.session_state.get("last_target_lang_widget") != target_lang:
    st.session_state.translated_text = ""
    st.session_state.translation_done = False
    st.session_state.last_source_lang_widget = source_lang
    st.session_state.last_target_lang_widget = target_lang

# Text input
st.subheader("Enter Text to Translate")
input_text = st.text_area(
    "Input Text",
    placeholder="Type or paste the text you want to translate here...",
    height=150,
    key="input_text"
)

# Translate button
if st.button("Translate", type="primary", use_container_width=True):
    if input_text.strip():
        try:
            with st.spinner("Translating..."):
                # Get language codes
                source_code = language_dict[source_lang.lower()]
                target_code = language_dict[target_lang.lower()]
                
                # Perform translation
                translator = GoogleTranslator(source=source_code, target=target_code)
                translated_text = translator.translate(input_text)
                
                # Store in session state for button functionality
                st.session_state.translated_text = translated_text
                st.session_state.target_code = target_code
                st.session_state.source_code = source_code
                st.session_state.stored_source_lang = source_lang
                st.session_state.stored_target_lang = target_lang
                st.session_state.translation_done = True
                
        except Exception as e:
            st.error(f"Translation failed: {str(e)}")
            st.session_state.translation_done = False
    else:
        st.warning("Please enter some text to translate")
        st.session_state.translation_done = False

# Display translation result if available
if st.session_state.get("translation_done", False) and st.session_state.get("translated_text"):
    st.success("Translation Complete!")
    st.caption(f"Translated from {st.session_state.get('stored_source_lang', 'unknown')} to {st.session_state.get('stored_target_lang', 'unknown')}")
    st.subheader("Translated Text")
    
    # Text area for translated text
    translated_output = st.text_area(
        "Translation",
        value=st.session_state.translated_text,
        height=150,
        key="translated_text_display",
        disabled=False
    )
    
    # Action buttons for translation
    col_a, col_b = st.columns(2)
    
    with col_a:
        if st.button("📋 Copy Translation", key="copy_btn", use_container_width=True):
            # Use JavaScript to copy to clipboard
            st.code(st.session_state.translated_text, language=None)
            st.success("Text displayed above - select and copy it (Ctrl+C)")
            st.toast("Select the text above and press Ctrl+C to copy", icon="📋")
    
    with col_b:
        if st.button("🔊 Listen to Translation", key="listen_btn", use_container_width=True):
            try:
                # Generate audio
                tts = gTTS(text=st.session_state.translated_text, lang=st.session_state.target_code, slow=False)
                audio_buffer = io.BytesIO()
                tts.write_to_fp(audio_buffer)
                audio_buffer.seek(0)
                
                # Display audio player
                st.audio(audio_buffer, format='audio/mp3')
                st.success("Audio generated!")
            except Exception as audio_error:
                st.warning(f"Audio generation not available for this language: {str(audio_error)}")
    
    # Display code block for easy copying
    with st.expander("📋 Quick Copy"):
        st.code(st.session_state.translated_text, language=None)
        st.caption("Select the text above to copy it")

# Additional features section
st.divider()
st.subheader("Additional Features")

col3, col4 = st.columns(2)

with col3:
    if st.button("Clear All", use_container_width=True):
        st.session_state.input_text = ""
        st.session_state.translated_text = ""
        st.session_state.translation_done = False
        st.rerun()

with col4:
    st.info("📝 Supported languages: " + str(len(languages)) + " languages available")

# Footer
st.markdown("---")
st.markdown("Built with Streamlit and deep-translator")
