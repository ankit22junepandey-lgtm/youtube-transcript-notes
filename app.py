import streamlit as st
from dotenv import load_dotenv

load_dotenv()
import os
from google import genai
from youtube_transcript_api import YouTubeTranscriptApi


def get_video_id(url):
    if "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    elif "watch?v=" in url:
        return url.split("watch?v=")[1].split("&")[0]
    return url

try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except Exception:
    api_key = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=api_key)

prompt = """You are a YouTube video summarizer. You will take the transcript text
and summarize the entire video, providing the important summary in points
within 250 words. Please provide the summary of the text given here:  """


def extract_transcript_details(youtube_video_url):
    try:
        video_id = get_video_id(youtube_video_url)
        ytt_api = YouTubeTranscriptApi()

        try:
            fetched = ytt_api.fetch(video_id, languages=['en'])
        except Exception:
            try:
                fetched = ytt_api.fetch(video_id, languages=['hi'])
            except Exception:
                transcript_list = ytt_api.list(video_id)
                first = next(iter(transcript_list))
                fetched = first.fetch()

        transcript = " ".join([snippet.text for snippet in fetched])
        return transcript
    except Exception as e:
        st.error(f"⚠️ Could not fetch transcript: {e}")
        st.info("This video may have no captions at all, or may be restricted. Try another video.")
        return None


def generate_gemini_content(transcript_text, prompt):
    models_to_try = ["gemini-3.8-flash", "gemini-2.5-flash", "gemini-3.5-flash"]
    last_error = None
    for model_name in models_to_try:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt + transcript_text,
            )
            return response.text
        except Exception as e:
            last_error = e
            print(f"[{model_name}] failed: {e}")
            continue
    st.error(f"⚠️ All Gemini models failed. Try again in a minute.\n\nLast error: {last_error}")
    return None


st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = get_video_id(youtube_link)
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)

if st.button("Get Detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        if summary:
            st.markdown("## Detailed Notes:")
            st.write(summary)