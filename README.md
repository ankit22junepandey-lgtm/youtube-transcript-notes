# YouTube Transcript → Detailed Notes Converter

🔗 **Live app:** https://youtube-transcript-notes-56ekkdpnkwhpsp7xct5cf7.streamlit.app/

Paste any YouTube URL, get AI-generated structured notes.

## Tech
- Streamlit
- Google Gemini API (google-genai)
- youtube-transcript-api
- python-dotenv

## Run locally
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
# Add GOOGLE_API_KEY to a .env file
streamlit run app.py
