import gradio as gr
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi  # Fixed case sensitivity
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable

# Function to extract transcript from Youtube video
def get_transcript(video_url):
    video_id = video_url.split("v=")[1].split("&")[0]
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en", "tr"])  # Fixed case sensitivity
    raw_text = " ".join([entry["text"] for entry in transcript])
    return raw_text

# Function to summarize or translate the transcript
def fn_sum_text(transkript_text, word_count, model_sel, lang_sel, action_sel, GEMINI_API_KEY):
    genai.configure(api_key=GEMINI_API_KEY) # Initializing Gemini AI API with the provided key

    model = genai.GenerativeModel(model_sel) # Creating a model instance based on selected model

    # Creating the prompt for AI processing
    prompt = f"{transkript_text} metni {word_count} sayıda kelimeyle {lang_sel} dilinde {action_sel}"

    response = model.generate_content(
        contents=[prompt] # Sending the prompt to the AI model
    )

    return response.text # Returning the generated response

# Creating the Gradio UI
demo = gr.Blocks(theme=gr.themes.Citrus()) # Initializing Gradio Blocks with Citrus theme
with demo:
    gr.Markdown("## Youtube Video Url Çeviri-Özet Gemini API") # Title for UI

    with gr.Row(): # Creating a row layout
        with gr.Column(): # Left column for input fields
            video_url = gr.Textbox(placeholder="Youtube Video URL") # Input field for video URL
            trs_btn = gr.Button("Transkripti Al") # Button to fetch transcript
            GEMINI_API_KEY = gr.Textbox(placeholder="GEMINI_API_KEY", type="password", show_label=False) # API key input

            word_count = gr.Slider(minimum=50, maximum=1000, value=200, step=10, label="Kelime Sayısı Seçimi") # Word count Selection

            model_sel = gr.Dropdown(
                choices=["gemini-2.0-flash", "gemini-2.0-flash-lite", "gemini-1.5-pro"],
                value="gemini-2.0-flash",
                label="Model Seçimi"
            ) # Dropdown for selecting AI model

            lang_sel = gr.Dropdown(
                choices=['Türkçe', 'İngilizce', 'Almanca', 'Rusça', 'İspanyolca'],
                value="Türkçe",
                label="Dil Seçimi"
            ) # Dropdown for language selection

            action_sel = gr.Dropdown(
                choices=["Özetle", "Tam çeviri yap."],
                value="Özetle",
                label="İşlem"
            ) # Dropdown to choose between summary and full translation

            sum_btn = gr.Button("Özetle") # Button to generate summary

        with gr.Column(): # Right column for output fields
            transkript_text = gr.Textbox(label="Transkripti", lines=5) # Textbox to display transcript
            sum_text = gr.Textbox(label="Özet", lines=5) # Textbox to display summary or translation

    trs_btn.click(
        fn=get_transcript, # Function to get transcript
        inputs=video_url, # Input : Youtube URL
        outputs=transkript_text # Output : Transcript Text
    )

    sum_btn.click(
        fn=fn_sum_text, # Function to summarize/translate transcript
        inputs=[transkript_text, word_count, model_sel, lang_sel, action_sel, GEMINI_API_KEY], # Inputs
        outputs=sum_text # Output: Summary/translated text

    )

demo.launch() # Launching Gradio app






