# Language Translator App

A simple and elegant language translator built with Streamlit and the deep-translator library.

## Features

- **Multi-language Support**: Translate between 100+ languages
- **Easy-to-use Interface**: Clean and intuitive UI
- **Real-time Translation**: Fast translation using Google Translate API
- **Copy Functionality**: One-click copy button for translated text
- **Text-to-Speech**: Listen to the translated text with audio playback
- **Quick Copy**: Expandable section for easy text selection

## Installation

1. Install Python 3.8 or higher if not already installed

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Running the App

Run the Streamlit app with:
```bash
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`

## Usage

1. Select the source language from the dropdown
2. Select the target language from the dropdown
3. Enter or paste the text you want to translate
4. Click the "Translate" button
5. View the translated text
6. Use the "Copy Translation" button to copy text to clipboard
7. Use the "Listen to Translation" button to hear the pronunciation
8. Expand "Quick Copy" section for easy text selection

## Dependencies

- **streamlit**: Web framework for the UI
- **deep-translator**: Python library for translation using Google Translate API
- **gtts**: Google Text-to-Speech library for audio generation
- **pyttsx3**: Offline text-to-speech library (alternative option)

## Notes

- This app uses the free Google Translate API via deep-translator
- No API key is required for basic usage
- Internet connection is required for translation and text-to-speech to work
- Text-to-speech feature supports most major languages
