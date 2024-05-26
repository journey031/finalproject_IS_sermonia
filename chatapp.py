import streamlit as st
import openai
from streamlit.report_thread import async_to_sync

from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=st.secrets["API_key"])

async def generate_travel_recommendation(destination, duration, interests):
    prompt_text = (
        f"I'm planning a trip to {destination} for {duration} days and I'm interested in {interests}."
    )

    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a Travel Advisor"},
            {"role": "user", "content": prompt_text}
        ],
    )

    return response.choices[0].message.content

def app():
    st.title("Personalized Travel Itinerary Planner")

    if 'step' not in st.session_state:
        st.session_state.step = 1

    if st.session_state.step == 1:
        st.session_state.destination = st.text_input("Where do you want to go?")
        st.session_state.duration = st.number_input("How many days will your trip be?", min_value=1, max_value=30)
        st.session_state.interests = st.text_input("What are your interests or activities you'd like to do?")
        if st.button("Next"):
            st.session_state.step = 2

    if st.session_state.step == 2:
        if st.button("Get Travel Recommendation"):
            st.session_state.step = 3  # Proceed to show the recommendation
            st.experimental_rerun()

    if st.session_state.step == 3:
        if 'itinerary' not in st.session_state:
            itinerary = async_to_sync(generate_travel_recommendation)(
                st.session_state.destination,
                st.session_state.duration,
                st.session_state.interests
            )
            st.session_state.itinerary = itinerary
        else:
            st.write(f"Recommended itinerary for your trip to {st.session_state.destination} for {st.session_state.duration} days, focusing on {st.session_state.interests}, is: {st.session_state.itinerary}")
            if st.button("Start Over"):
                for key in ['step', 'destination', 'duration', 'interests', 'itinerary']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.experimental_rerun()

if __name__ == "__main__":
    app()
