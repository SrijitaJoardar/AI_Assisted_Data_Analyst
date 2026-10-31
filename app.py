
import logging
import streamlit as st

from src.utils.logger import setup_logger

from src.agent.data_analyst_agent import (
    ask_data_analyst_detailed,
    AgentError,
)
from src.analytics.offline_analytics import run_offline_analysis
from src.analytics.visualization import create_bar_chart


# --------------------------------------------------
# LOGGING CONFIGURATION
# --------------------------------------------------

setup_logger()
logger = logging.getLogger(__name__)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.title("📊 AI Data Analyst")

    st.write(
        "An AI-powered analytics assistant "
        "for exploring Superstore sales data."
    )

    st.divider()

    st.subheader("About this project")

    st.write(
        """
        This application allows users to ask questions
        about sales data using natural language.

        **Technology stack**
        - Python
        - SQLite
        - Pandas
        - Gemini API
        - Streamlit
        - Plotly
        """
    )

    st.divider()

    st.subheader("Example questions")

    st.markdown(
        """
        - Which region generated the highest total sales?
        - Which category generated the highest profit?
        - Show sales by region.
        - Which region generated the highest profit?
        - What is the average quantity by segment?
        - What are the total sales and total profit?
        """
    )

    st.divider()

    st.caption("AI Data Analyst | Portfolio Project")


# --------------------------------------------------
# MAIN PAGE
# --------------------------------------------------

st.title("AI Data Analyst")

st.write(
    "Explore your Superstore sales data "
    "by asking questions in natural language."
)

st.info(
    "Ask a business question below. "
    "The application will analyze your data and present the results."
)


# --------------------------------------------------
# QUESTION INPUT
# --------------------------------------------------

with st.form("analysis_form"):

    question = st.text_area(
        "What would you like to know?",
        placeholder=(
            "Example: Which region generated "
            "the highest total sales?"
        ),
        height=110,
    )

    submitted = st.form_submit_button(
        "🔍 Analyze Data",
        type="primary",
        width="stretch",
    )


# --------------------------------------------------
# ANALYSIS EXECUTION
# --------------------------------------------------

if submitted:

    if not question.strip():

        logger.warning("Analysis submitted with an empty question.")

        st.warning(
            "Please enter a question before analyzing."
        )

    else:

        logger.info("Analysis request received.")

        try:

            with st.spinner(
                "Analyzing your data. Please wait..."
            ):

                # Try offline analytics first.
                analysis = run_offline_analysis(question)

                if analysis is None:

                    logger.info(
                        "Offline analysis did not match. "
                        "Using Gemini AI fallback."
                    )

                    analysis = ask_data_analyst_detailed(
                        question
                    )

                    mode = "Gemini"

                else:

                    logger.info(
                        "Question successfully answered using offline analytics."
                    )

                    mode = "Offline"

                # Preserve results across Streamlit reruns.
                st.session_state["analysis_mode"] = mode
                st.session_state["analysis_result"] = analysis
                st.session_state["last_question"] = question

            logger.info(
                "Analysis request completed successfully. Mode: %s",
                mode,
            )

        except AgentError as error:

            logger.error(
                "Agent analysis failed: %s",
                error,
            )

            st.error(str(error))

            st.session_state.pop("analysis_result", None)
            st.session_state.pop("analysis_mode", None)

        except ValueError as error:

            logger.warning(
                "Invalid analysis input: %s",
                error,
            )

            st.warning(str(error))

            st.session_state.pop("analysis_result", None)
            st.session_state.pop("analysis_mode", None)

        except Exception:

            logger.exception(
                "Unexpected error during analysis."
            )

            st.error(
                "Something went wrong while analyzing your data. "
                "Please try again."
            )

            st.session_state.pop("analysis_result", None)
            st.session_state.pop("analysis_mode", None)


# --------------------------------------------------
# DISPLAY ANALYSIS
# --------------------------------------------------

if "analysis_result" in st.session_state:

    analysis = st.session_state["analysis_result"]
    mode = st.session_state["analysis_mode"]

    st.divider()

    st.subheader("Analysis Results")

    st.caption(
        f"Question: {st.session_state['last_question']}"
    )

    if mode == "Offline":

        st.success(
            "Offline Analysis | No Gemini API call was required."
        )

    else:

        st.info(
            "Gemini AI Analysis | Answer generated using Gemini."
        )

    # Answer
    st.markdown("### Answer")

    st.write(analysis["answer"])

    # Visualization
    if analysis["results"]:

        fig = create_bar_chart(analysis["results"])

        if fig is not None:

            st.markdown("### Visual Analytics")

            st.plotly_chart(
                fig,
                width="stretch",
            )

    # SQL and raw database results
    col1, col2 = st.columns(2)

    with col1:

        with st.expander("View Generated SQL"):

            st.code(
                analysis["sql"],
                language="sql",
            )

    with col2:

        with st.expander("View Database Results"):

            if analysis["results"]:

                st.dataframe(
                    analysis["results"],
                    width="stretch",
                    hide_index=True,
                )

            else:

                st.info(
                    "The query returned no rows."
                )
