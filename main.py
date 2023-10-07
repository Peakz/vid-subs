import os
import streamlit as st
from tempfile import NamedTemporaryFile
from transcriber import Transcriber
from subtitle_generator import SubtitleGenerator
from moviepy.editor import VideoFileClip

# TODO Dictionary of languages (ISO 639-1 codes) mapped to their full names
languages = {
    "af": "Afrikaans", "sq": "Albanian", "am": "Amharic", "ar": "Arabic", "hy": "Armenian", "az": "Azerbaijani", "eu": "Basque", "be": "Belarusian", "bn": "Bengali", "bs": "Bosnian", "bg": "Bulgarian", "ca": "Catalan", "ceb": "Cebuano", "ny": "Chichewa", "zh-cn": "Chinese (Simplified)", "zh-tw": "Chinese (Traditional)", "co": "Corsican", "hr": "Croatian", "cs": "Czech", "da": "Danish", "nl": "Dutch", "en": "English", "eo": "Esperanto", "et": "Estonian", "tl": "Filipino", "fi": "Finnish", "fr": "French", "fy": "Frisian", "gl": "Galician", "ka": "Georgian", "de": "German", "el": "Greek", "gu": "Gujarati", "ht": "Haitian Creole", "ha": "Hausa", "haw": "Hawaiian", "iw": "Hebrew", "hi": "Hindi", "hmn": "Hmong", "hu": "Hungarian", "is": "Icelandic", "ig": "Igbo", "id": "Indonesian", "ga": "Irish", "it": "Italian", "ja": "Japanese", "jw": "Javanese", "kn": "Kannada", "kk": "Kazakh", "km": "Khmer", "ko": "Korean", "ku": "Kurdish (Kurmanji)", "ky": "Kyrgyz", "lo": "Lao", "la": "Latin", "lv": "Latvian", "lt": "Lithuanian", "lb": "Luxembourgish", "mk": "Macedonian", "mg": "Malagasy", "ms": "Malay", "ml": "Malayalam", "mt": "Maltese", "mi": "Maori", "mr": "Marathi", "mn": "Mongolian", "my": "Burmese", "ne": "Nepali", "no": "Norwegian", "or": "Odia", "ps": "Pashto", "fa": "Persian", "pl": "Polish", "pt": "Portuguese", "pa": "Punjabi", "ro": "Romanian", "ru": "Russian", "sm": "Samoan", "gd": "Scots Gaelic", "sr": "Serbian", "st": "Sesotho", "sn": "Shona", "sd": "Sindhi", "si": "Sinhala", "sk": "Slovak", "sl": "Slovenian", "so": "Somali", "es": "Spanish", "su": "Sundanese", "sw": "Swahili", "sv": "Swedish", "tg": "Tajik", "ta": "Tamil", "te": "Telugu", "th": "Thai", "tr": "Turkish", "uk": "Ukrainian", "ur": "Urdu", "ug": "Uyghur", "uz": "Uzbek", "vi": "Vietnamese", "cy": "Welsh", "xh": "Xhosa", "yi": "Yiddish", "zu": "Zulu"
}

if "api_key" not in st.session_state:
    st.session_state["api_key"] = ""

def get_latest_file_number(directory):
    files = os.listdir(directory)
    max_number = 0
    for file in files:
        try:
            number = int(file.split('_')[-1].split('.')[0])
            if number > max_number:
                max_number = number
        except ValueError:
            continue
    return max_number

def main():
    st.title("Peak's VALORANT transcriber")
    st.write("This is a work in progress to help creators lower their costs to produce quality content. I will continue to improve the app as a side-project over time. At the moment we're limited to 25mb files until I've built a splitter for longer clips. The audio of a 10min vid should be around 25mb.")
    
    api_key_input = st.sidebar.text_input("Enter your OpenAI API key", type="password")
    update_button = st.sidebar.button("Update API Key")
    
    st.sidebar.divider()
    
    faq = st.sidebar.selectbox(
        'Frequently Asked Questions',
        ['How to use this app?', 'What file formats are supported?', 'How to get OpenAI API key?', 'What are custom terms?', 'What do I do with the output?', 'What if the output is incorrect?', 'How much $$$ does the API cost?']
    )
    
    if faq == 'How to use this app?':
        st.sidebar.info('Enter your OpenAI API key, upload your audio or video file and click Transcribe.')
    elif faq == 'What file formats are supported?':
        st.sidebar.info('Currently, only supporting mp3 and mp4 formats.')
    elif faq == 'How to get OpenAI API key?':
        st.sidebar.info('You can get your OpenAI API key from the OpenAI website after creating an account.')
    elif faq == 'What are custom terms?':
        st.sidebar.info('Custom terms are words you want to be emphasized in the transcription. They may or may not improve the output')
    elif faq == 'What do I do with the output?':
        st.sidebar.info('If the output seems good to you, you can copy it to a text file and upload it as subtitle to youtube for example.')
    elif faq == 'What if the output is incorrect?':
        st.sidebar.info('Try adding custom words for the words that seem incorrect. It is a simple app, so there might be some errors but if nothing works, shoot me a dm on Twitter (@Gosupeak) or Discord (Gosupeak) with the clip and the output. I will take a look at it when I have time.')
    elif faq == 'How much $$$ does the API cost?':
        st.sidebar.info('Up to date pricing for the whisper model used here: https://openai.com/pricing#audio-models')



    st.sidebar.divider()
    
    custom_terms = st.sidebar.text_input(label="Enter custom words to improve the transcript accuracy, separate with comma. I.e agent names or hard to hear words")
    
    if update_button:
        st.session_state["api_key"] = api_key_input
    
    if st.session_state["api_key"] == "":
        st.warning("Please enter your OpenAI API key to continue")
        st.stop()
    
    uploaded_file = st.file_uploader("Choose a file. OpenAI limits to 25mb file size", type=["mp3", "mp4"])
    
    # TODO lang = st.sidebar.selectbox('Select a language', list(languages.keys()), format_func=lambda x: languages[x])
    
    if uploaded_file is not None:
        transcribe_button = st.button("Transcribe")
        if transcribe_button:
            try:
                file_number = get_latest_file_number('.') + 1
                with NamedTemporaryFile(delete=False, suffix=f"_{file_number}.mp4") as f:
                    f.write(uploaded_file.getbuffer())
                    video_file = f.name

                audio_file = f"audio_{file_number}.mp3"
                transcript_file = f"transcript_{file_number}.txt"

                # Extract audio using moviepy
                video = VideoFileClip(video_file)
                audio = video.audio
                audio.write_audiofile(audio_file)

                # Close the video and audio clips after using them
                video.close()
                audio.close()
                
                transcriber = Transcriber(st.session_state["api_key"])

                transcription = transcriber.transcribe(audio_file, custom_terms)

                generator = SubtitleGenerator()
                generator.generate(transcription, transcript_file)

                col1, col2 = st.columns(2)
                with col1:
                    st.video(video_file)
                
                with col2:
                    with st.container():
                        st.text(open(transcript_file).read())
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
            
            files_to_remove = [video_file, audio_file, transcript_file, uploaded_file.name]

            for file in files_to_remove:
                if os.path.exists(file):
                    os.remove(file)


if __name__ == "__main__":
    main()
