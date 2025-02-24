import streamlit as st
import os
from utils.trailer_generator import generate_trailer, cleanup_temp_files

st.set_page_config(page_title="AI Trailer Generator", page_icon="🎬")

def main():
    st.title("🎬 AI Movie Trailer Generator")

    # Introduction
    st.markdown("""
    This AI-powered tool generates movie trailers based on your description.
    It uses:
    - GPT-4o for script generation
    - DALL-E 3 for scene visualization
    - Advanced video processing for trailer creation
    """)

    try:
        # Movie description input
        movie_description = st.text_area(
            "Describe your movie:",
            height=150,
            placeholder="Enter a detailed description of your movie, including genre, plot, main characters, and key scenes..."
        )

        # Generation controls
        col1, col2 = st.columns(2)
        with col1:
            duration = st.slider(
                "Trailer Duration (seconds)",
                min_value=15,
                max_value=60,
                value=30,
                step=5
            )

        with col2:
            generate_button = st.button("Generate Trailer", type="primary")

        if generate_button and movie_description:
            with st.spinner("🎬 Generating your movie trailer... This may take a few minutes."):
                # Create temporary directory if it doesn't exist
                os.makedirs("temp", exist_ok=True)

                # Generate the trailer
                result = generate_trailer(movie_description, duration)

                if "error" in result:
                    st.error(f"Failed to generate trailer: {result['error']}")
                else:
                    # Display success message
                    st.success("🎉 Trailer generated successfully!")

                    # Display the script
                    st.subheader("Generated Script")
                    script = result["script"]
                    st.write("🎭 Opening Hook:", script["opening_hook"])
                    st.write("📝 Plot Setup:", script["plot_setup"])
                    st.write("🎬 Key Scenes:")
                    for scene in script["key_scenes"]:
                        st.write(f"• {scene}")
                    st.write("💥 Climax:", script["climax"])
                    st.write("✨ Tagline:", script["tagline"])

                    # Display the video
                    if os.path.exists(result["path"]):
                        st.subheader("Your Generated Trailer")
                        st.video(result["path"])

                        # Download button
                        with open(result["path"], "rb") as file:
                            st.download_button(
                                label="Download Trailer",
                                data=file,
                                file_name="movie_trailer.mp4",
                                mime="video/mp4"
                            )
                    else:
                        st.error("Generated video file not found.")

                    # Cleanup
                    cleanup_temp_files()
        elif generate_button:
            st.warning("Please enter a movie description first.")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please try again or contact support if the issue persists.")
        cleanup_temp_files()

if __name__ == "__main__":
    main()