
import streamlit as st

from src.agent.data_analyst_agent import (
    ask_data_analyst,
    AgentError,
)


st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="📊",
    layout="centered",
)


st.title("📊 AI Data Analyst")
st.write(
    "Ask questions about your Superstore sales data "
    "using natural language."
)

st.info(
    "Example: Which region generated the highest total sales?"
)


question = st.text_area(
    "Enter your question",
    placeholder="e.g. Which product category generated the highest profit?",
    height=100,
)

if st.button("Analyze", type="primary"):
    if not question.strip():
        st.warning("Please enter a question before analyzing.")

    else:
        try:
            with st.spinner(
                "Analyzing your data... This may take a moment."
            ):
                answer = ask_data_analyst(question)

            st.subheader("Analysis")
            st.write(answer)

        except AgentError as error:
            st.error(str(error))

        except Exception:
            st.error(
                "Something went wrong while analyzing your data. "
                "Please try again."
            )
