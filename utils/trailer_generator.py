import os
import json
from moviepy.editor import TextClip, concatenate_videoclips
from openai import OpenAI
from PIL import Image
import requests
from io import BytesIO

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

def generate_scene_images(scene_description):
    """Generate an image for a scene using DALL-E 3."""
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=f"Movie scene: {scene_description}. Cinematic, dramatic lighting, high quality",
            n=1,
            size="1024x1024"
        )

        # Download the generated image
        image_url = response.data[0].url
        image_response = requests.get(image_url)
        image = Image.open(BytesIO(image_response.content))

        # Save temporarily
        os.makedirs("temp", exist_ok=True)
        temp_path = f"temp/scene_{hash(scene_description)}.png"
        image.save(temp_path)
        return temp_path
    except Exception as e:
        print(f"Image generation error: {e}")
        return None

def create_text_clip(text, duration=3, fontsize=70, color='white'):
    """Create a text clip with fade effects."""
    try:
        txt_clip = TextClip(
            text,
            fontsize=fontsize,
            color=color,
            bg_color='rgba(0,0,0,0.5)',
            font="Arial",
            size=(1024, 100)
        )
        return txt_clip.set_duration(duration).crossfadein(0.5).crossfadeout(0.5)
    except Exception as e:
        print(f"Text clip creation error: {e}")
        return None

def generate_trailer(movie_description, duration=30):
    """Generate a complete movie trailer."""
    try:
        # Create output directory if it doesn't exist
        os.makedirs("temp", exist_ok=True)

        # Generate script
        script = generate_trailer_script(movie_description)
        if "error" in script:
            return {"error": script["error"]}

        clips = []

        # Create opening
        opening_text = create_text_clip(script["opening_hook"])
        if opening_text:
            clips.append(opening_text)

        # Add plot setup
        setup_text = create_text_clip(script["plot_setup"], duration=4)
        if setup_text:
            clips.append(setup_text)

        # Add key scenes
        for scene in script["key_scenes"]:
            scene_text = create_text_clip(scene)
            if scene_text:
                clips.append(scene_text)

        # Add climax
        climax_text = create_text_clip(script["climax"])
        if climax_text:
            clips.append(climax_text)

        # Add tagline
        tagline_text = create_text_clip(
            script["tagline"],
            duration=4,
            fontsize=90,
            color='yellow'
        )
        if tagline_text:
            clips.append(tagline_text)

        if not clips:
            return {"error": "Failed to create any video clips"}

        # Combine all clips
        final_clip = concatenate_videoclips(clips)

        # Export
        output_path = "temp/generated_trailer.mp4"
        final_clip.write_videofile(
            output_path,
            fps=24,
            codec='libx264',
            audio=False
        )

        # Cleanup clips
        for clip in clips:
            clip.close()

        return {
            "success": True,
            "path": output_path,
            "script": script
        }
    except Exception as e:
        return {
            "error": f"Failed to generate trailer: {str(e)}"
        }

def cleanup_temp_files():
    """Clean up any temporary files created during generation."""
    try:
        import glob
        import shutil

        # Remove temporary directory and all its contents
        if os.path.exists("temp"):
            shutil.rmtree("temp")

    except Exception as e:
        print(f"Cleanup error: {e}")