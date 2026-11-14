import os
import glob
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip


def stitch_and_add_voice(input_folder, input_audio, output_filename):
    print(f"Scanning for MP4 files in '{input_folder}'...")

    # 1. Find all .mp4 files (handles both .mp4 and .MP4)
    search_path = os.path.join(input_folder, "*.[mM][pP]4")
    video_files = glob.glob(search_path)
    video_files.sort()

    if not video_files:
        print("No videos found! Check your folder path.")
        return

    clips = []
    for file in video_files:
        print(f"Loading {file} and removing its audio...")
        # 2. Load each video and remove its original audio
        clip = VideoFileClip(file).without_audio()
        clips.append(clip)

    print(f"Stitching {len(clips)} clips together...")
    # 3. Combine them sequentially into one silent video
    final_video = concatenate_videoclips(clips)

    print(f"Loading voiceover: {input_audio}...")
    # 4. Load your custom audio file
    voice_clip = AudioFileClip(input_audio)

    # Trim the voiceover if it is longer than the combined video length
    if voice_clip.duration > final_video.duration:
        voice_clip = voice_clip.subclip(0, final_video.duration)

    print("Attaching voiceover to the final video...")
    # 5. Attach your own voice to the combined video
    final_video = final_video.set_audio(voice_clip)

    # 6. Make sure the output folder exists
    output_dir = os.path.dirname(output_filename)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    print(f"Exporting to {output_filename}...")
    # 7. Render the final output
    final_video.write_videofile(
        output_filename,
        codec="libx264",
        audio_codec="aac",
        threads=4
    )
    print("Done!")


# --- Run the Script ---
if __name__ == "__main__":
    stitch_and_add_voice(
        input_folder="video_batch",
        input_audio="./mike_voices/my_voice.m4a",
        output_filename="output_videos/batch_with_my_voice.mp4"
    )