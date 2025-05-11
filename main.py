import streamlit as sl
from few_shot import FewShotPosts
from post_generator import generate_post

language_options = ["English", "Hindi"]
length_options = ["Short", "Medium", "Long"]

def main():
    sl.markdown(
        """
        <h1 style='text-align: center; color: #4B8BBE; font-size: 3em;'>
            🚀 LinkedIn Post Generator
        </h1>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = sl.columns(3)
    fs = FewShotPosts()

    # Add default placeholders
    topics_options = ["Select a topic"] + list(fs.get_tags())
    length_options_full = ["Select length"] + length_options
    language_options_full = ["Select language"] + language_options

    with col1:
        selected_topic = sl.selectbox("Topics", options=topics_options, index=0)
    with col2:
        selected_length = sl.selectbox("Length", options=length_options_full, index=0)
    with col3:
        selected_language = sl.selectbox("Language", options=language_options_full, index=0)

    sl.markdown("---")

    if sl.button("✨ GENERATE POST ✨", use_container_width=True):
        if (selected_topic == "Select a topic" or
            selected_length == "Select length" or
            selected_language == "Select language"):
            sl.error("🚨 Please make sure to select a valid option in all dropdowns!")
        else:
            with sl.spinner("Generating your post... ✍️"):
                generated_post = generate_post(selected_topic, selected_length, selected_language)
            sl.success("✅ Post generated successfully!")
            sl.markdown(f"""
    <h3>Generated post for <em>{selected_topic}</em>, <em>{selected_length}</em>, <em>{selected_language}</em>:</h3>
    <p style="font-size: 1.2em; margin-top: 0.5em;">{generated_post}</p>
""", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
