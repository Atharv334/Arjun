
import streamlit as st
from moviepy.editor import ImageClip, concatenate_videoclips, TextClip, CompositeVideoClip, CompositeAudioClip, AudioFileClip
from gtts import gTTS
from PIL import Image
import numpy as np
import os

st.title("Auto Multi-Scene Video Generator (Hindi Voiceover + Subtitles)")

script = st.text_area("Enter your multi-line script (1 line = 1 scene)", "Safalta ek safar hai.\nMehnat kabhi bekaar nahi jaati.\nHar din naye mauke laaye.")

if st.button("Generate Video"):
    lines = [line.strip() for line in script.split("\n") if line.strip() != ""]
    
    if not lines:
        st.error("Please enter at least one valid line!")
    else:
        clips = []
        for i, line in enumerate(lines):
            # Generate voiceover for each line
            tts = gTTS(text=line, lang='hi')
            audio_path = f"audio_{i}.mp3"
            tts.save(audio_path)
            audio_clip = AudioFileClip(audio_path)

            # Placeholder static background
            img = Image.new('RGB', (1280, 720), color=(50, 50, 50))
            img_path = f"bg_{i}.jpg"
            img.save(img_path)
            img_clip = ImageClip(img_path).set_duration(audio_clip.duration)
            
            # Add subtitles (captions)
            caption = TextClip(line, fontsize=40, color='white', bg_color='black', size=img_clip.size, method='caption')
            caption = caption.set_duration(audio_clip.duration).set_position('bottom')
            
            # Merge image + subtitles
            scene = CompositeVideoClip([img_clip, caption]).set_audio(audio_clip)
            clips.append(scene)
        
        # Concatenate all scenes
        final_video = concatenate_videoclips(clips, method="compose")
        final_video.write_videofile("final_output.mp4", fps=24)

        # Show download button
        with open("final_output.mp4", "rb") as video_file:
            st.video("final_output.mp4")
            st.download_button("Download Video", video_file, file_name="final_output.mp4")

        # Cleanup temp files
        for i in range(len(lines)):
            os.remove(f"audio_{i}.mp3")
            os.remove(f"bg_{i}.jpg")
