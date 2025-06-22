"""
A Streamlit web application for the XAI Transparent Grading system.

To run:
streamlit run app.py
"""
import streamlit as st
from main import run_grading_pipeline

st.set_page_config(page_title="XAI Transparent Grading", layout="wide")

st.title("Explainable AI for Transparent Grading 🤖📝")
st.markdown("""
This tool uses AI to automatically grade student essays while providing clear justifications for the scores.
It leverages NLP and rubric-based evaluation to highlight strengths, weaknesses, and missing points.
""")

st.header("Submit an Essay for Grading")

# --- New Input Logic with File Upload ---

# 1. Add the file uploader widget
uploaded_file = st.file_uploader(
    "Option 1: Upload an essay file (.txt or .md)",
    type=["txt", "md"]
)

# 2. Determine the initial text for the text area
initial_text = ""
if uploaded_file is not None:
    # If a file is uploaded, use its content
    try:
        initial_text = uploaded_file.getvalue().decode("utf-8")
    except Exception as e:
        st.error(f"Error reading file: {e}")
else:
    # Otherwise, use a default sample essay as a placeholder
    initial_text = """One Piece: A Comprehensive Summary of Eiichiro Oda's Epic Adventure
One Piece is a globally acclaimed Japanese manga series written and illustrated by Eiichiro Oda. Since its serialization in Weekly Shōnen Jump in 1997, it has become the best-selling manga of all time, with over 516.6 million copies in circulation worldwide 1. The story follows Monkey D. Luffy, a young pirate with dreams of becoming the next "Pirate King," as he embarks on a grand adventure to find the legendary treasure known as the "One Piece," left behind by the executed Pirate King, Gol D. Roger 712.

The World of One Piece
The One Piece universe is vast and intricately designed, featuring a planet dominated by vast oceans divided by the Red Line and the Grand Line. The Grand Line is a treacherous sea where the most powerful pirates and mythical islands exist, while the Calm Belt—infested with monstrous Sea Kings—separates it from the four Blues (East, West, North, and South) 1. The World Government rules over this world, enforcing its will through the Marines and the secretive Cipher Pol agencies. Opposing them are pirates, revolutionaries, and other factions fighting for freedom 1.

A key element of the world is Devil Fruits, mysterious fruits that grant supernatural abilities at the cost of the user’s ability to swim. Luffy, for instance, ate the Gum-Gum Fruit, giving him a rubber-like body 7. Another power system, Haki, allows individuals to harness willpower for combat, observation, and even overpowering Devil Fruit users 1.

The Straw Hat Pirates
Luffy’s journey begins in the East Blue Saga, where he gradually assembles his crew, the Straw Hat Pirates:

Roronoa Zoro – A three-sword-wielding swordsman aiming to be the world’s greatest.

Nami – A brilliant navigator with a tragic past tied to the fish-man pirate Arlong.

Usopp – A sharpshooter and storyteller striving to become a brave warrior.

Sanji – A chivalrous chef and master kickboxer searching for the legendary All Blue sea.

Tony Tony Chopper – A reindeer doctor who ate the Human-Human Fruit.

Nico Robin – An archaeologist seeking the truth of the Void Century.

Franky – A cyborg shipwright who built their ship, the Thousand Sunny.

Brook – A living skeleton musician seeking to reunite with a whale named Laboon.

Jinbe – A fish-man and former Warlord who joins later, strengthening the crew’s bond 78.

Major Story Arcs and Sagas
The narrative is divided into sagas, each containing multiple arcs:

1. East Blue Saga
Luffy forms his crew, defeats local pirates like Buggy and Arlong, and enters the Grand Line 3.

2. Alabasta Saga
The crew aids Princess Vivi in stopping a civil war orchestrated by the warlord Crocodile, introducing the concept of Poneglyphs—ancient stones holding world secrets 38.

3. Sky Island Saga
The Straw Hats ascend to Skypiea, battling the self-proclaimed god Enel and uncovering ties to an ancient civilization 3.

4. Water 7 & Enies Lobby Saga
The crew faces betrayal, loses their ship, the Going Merry, and battles the World Government to rescue Robin, who is targeted for her knowledge of the Void Century 38.

5. Summit War Saga
Luffy’s brother, Portgas D. Ace, is captured, leading to a massive war at Marineford. Despite Luffy’s efforts, Ace dies, and the crew separates for two years to train 8.

6. Post-Timeskip Sagas
The reunited crew ventures into the New World, confronting powerful Yonko (Emperors of the Sea) like Big Mom and Kaido, uncovering more about the One Piece’s true nature 12.

Themes and Impact
One Piece explores deep themes of freedom, friendship, justice, and legacy. Luffy’s unwavering determination inspires allies and enemies alike, while the series critiques oppressive systems like the World Government 4. Its humor, emotional depth, and world-building have made it a cultural phenomenon, influencing countless fans and creators.

Conclusion
With over 1,100 chapters and still ongoing, One Piece remains a masterpiece of storytelling. As Luffy and his crew inch closer to the fabled treasure, the world awaits the revelation of what the "One Piece" truly is—a mystery that will reshape the world 12. Whether it’s a physical treasure or something more profound, Oda’s epic continues to captivate, proving that the journey itself is just as valuable as the destination."""

# 3. Create the text area, pre-filled with either the uploaded text or the sample
submission_text = st.text_area("Option 2: Paste essay text below (or edit uploaded content)", value=initial_text, height=250)

# This creates the button that starts the grading process.
if st.button("Grade Essay"):
    if submission_text.strip():
        # Show a "loading" spinner while the AI works.
        with st.spinner("AI is grading the essay..."):
            # Call the grading function from main.py
            explanations = run_grading_pipeline(submission_text)

        # Display the results.
        st.header("Transparent Grade Report")
        st.success(f"**Overall Grade: {explanations['overall_grade']}**")
        st.info(f"**Summary:** {explanations['overall_summary']}")

        st.subheader("Detailed Feedback")
        # Loop through each criterion and display its feedback in an expandable section.
        for criterion_key, exp_data in explanations["criterion_explanations"].items():
            with st.expander(f"**{exp_data['name']}** (Score: {exp_data['score']:.1f} / {exp_data['max_score']})", expanded=True):
                st.markdown(f"**Feedback:** {exp_data['feedback']}")
    else:
        st.warning("Please upload a file or paste an essay into the text box before grading.")

st.sidebar.header("About")
st.sidebar.info("This application demonstrates how Explainable AI (XAI) can bring transparency and trust to automated grading systems.")
