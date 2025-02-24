import os
import json
from moviepy.editor import TextClip, concatenate_videoclips
from openai import OpenAI

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "default-key")
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_trailer_script(movie_description):
    """Generate a movie trailer script using GPT-4o."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": """Create a movie trailer script with the following elements:
                    1. Opening hook (5-10 words)
                    2. Plot setup (20-30 words)
                    3. Key scenes (3-5 scenes, each 10-15 words)
                    4. Climactic moment (10-15 words)
                    5. Tagline (5-10 words)
                    Return as JSON with these exact keys."""
                },
                {"role": "user", "content": movie_description}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {
            "error": f"Failed to generate script: {str(e)}",
            "opening_hook": "In a world...",
            "plot_setup": "A story unfolds...",
            "key_scenes": ["Scene 1", "Scene 2", "Scene 3"],
            "climax": "Everything changes...",
            "tagline": "Coming soon..."
        }

def create_text_clip(text, duration=3, fontsize=70, color='white', size=(800, 100)):
    """Create a text clip with fade effects."""
    try:
        txt_clip = TextClip(
            text,
            fontsize=fontsize,
            color=color,
            bg_color='rgba(0,0,0,0.5)',
            font="Arial-Bold",
            size=size,
            method='caption'
        ).set_position('center')

        return txt_clip.set_duration(duration).crossfadein(0.5).crossfadeout(0.5)
    except Exception as e:
        print(f"Text clip creation error: {e}")
        return None

def generate_trailer(movie_description, duration=30):
    """Generate a complete movie trailer."""
    try:
        # Ensure temp directory exists
        os.makedirs("temp", exist_ok=True)

        # Generate script
        script = generate_trailer_script(movie_description)
        if "error" in script:
            return {"error": script["error"]}

        clips = []
        total_duration = 0

        # Opening hook with larger text
        clip = create_text_clip(
            script["opening_hook"],
            duration=4,
            fontsize=80,
            color='#FFD700',  # Gold color
            size=(900, 200)
        )
        if clip:
            clips.append(clip)
            total_duration += 4

        # Plot setup
        clip = create_text_clip(
            script["plot_setup"],
            duration=5,
            size=(900, 150)
        )
        if clip:
            clips.append(clip)
            total_duration += 5

        # Key scenes
        for scene in script["key_scenes"]:
            clip = create_text_clip(scene, duration=3)
            if clip:
                clips.append(clip)
                total_duration += 3

        # Climax with dramatic color
        clip = create_text_clip(
            script["climax"],
            duration=4,
            color='#FF4444',  # Red color
            fontsize=75
        )
        if clip:
            clips.append(clip)
            total_duration += 4

        # Tagline with special styling
        clip = create_text_clip(
            script["tagline"],
            duration=4,
            fontsize=90,
            color='#FFD700',  # Gold color
            size=(900, 200)
        )
        if clip:
            clips.append(clip)
            total_duration += 4

        if not clips:
            return {"error": "Failed to create video clips"}

        # Combine clips
        final_clip = concatenate_videoclips(clips, method="compose")

        # Export with progress_bar=False to avoid terminal output
        output_path = "temp/generated_trailer.mp4"
        final_clip.write_videofile(
            output_path,
            fps=24,
            codec='libx264',
            audio=False,
            progress_bar=False
        )

        # Clean up clips
        for clip in clips:
            clip.close()

        return {
            "success": True,
            "path": output_path,
            "script": script,
            "duration": total_duration
        }

    except Exception as e:
        return {"error": f"Failed to generate trailer: {str(e)}"}

def cleanup_temp_files():
    """Clean up temporary files."""
    try:
        import shutil
        if os.path.exists("temp"):
            shutil.rmtree("temp")
    except Exception as e:
        print(f"Cleanup error: {e}")