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
    - Advanced text animation effects
    - Professional video processing
    """)

    try:
        # Movie description input
        movie_description = st.text_area(
            "Describe your movie:",
            height=150,
            placeholder="Enter a detailed description of your movie, including genre, plot, main characters, and key scenes..."
        )

        # Generation controls
        generate_button = st.button("Generate Trailer", type="primary")

        if generate_button and movie_description:
            # Create progress placeholders
            script_progress = st.empty()
            video_progress = st.empty()
            result_container = st.empty()

            try:
                # Update progress for script generation
                with script_progress.container():
                    st.info("🤖 Generating trailer script...")

                # Generate the trailer
                with video_progress.container():
                    st.warning("🎬 Creating video... This may take a minute.")
                    result = generate_trailer(movie_description)

                if "error" in result:
                    result_container.error(f"❌ {result['error']}")
                else:
                    # Clear progress indicators
                    script_progress.empty()
                    video_progress.empty()

                    # Show success in result container
                    with result_container.container():
                        st.success("🎉 Trailer generated successfully!")

                        # Display the script
                        st.subheader("Generated Script")
                        script = result["script"]

                        # Create columns for different script elements
                        col1, col2 = st.columns(2)

                        with col1:
                            st.markdown("**🎭 Opening Hook**")
                            st.info(script["opening_hook"])

                            st.markdown("**📝 Plot Setup**")
                            st.info(script["plot_setup"])

                        with col2:
                            st.markdown("**💥 Climax**")
                            st.info(script["climax"])

                            st.markdown("**✨ Tagline**")
                            st.info(script["tagline"])

                        # Key scenes in a separate section
                        st.markdown("**🎬 Key Scenes**")
                        for i, scene in enumerate(script["key_scenes"], 1):
                            st.info(f"Scene {i}: {scene}")

                        # Display the video if it exists
                        if os.path.exists(result["path"]):
                            st.subheader("Your Generated Trailer")
                            st.video(result["path"])

                            # Download button
                            with open(result["path"], "rb") as file:
                                st.download_button(
                                    label="⬇️ Download Trailer",
                                    data=file,
                                    file_name="movie_trailer.mp4",
                                    mime="video/mp4"
                                )
                        else:
                            st.error("Generated video file not found.")

            except Exception as e:
                st.error(f"An error occurred during generation: {str(e)}")
            finally:
                # Cleanup
                cleanup_temp_files()

        elif generate_button:
            st.warning("⚠️ Please enter a movie description first.")

    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
        st.info("Please try again or contact support if the issue persists.")
        cleanup_temp_files()

if __name__ == "__main__":
    main()