
import streamlit as st

from src.agent.data_analyst_agent import (
    ask_data_analyst_detailed,
    AgentError,
)
from src.analytics.offline_analytics import run_offline_analysis
from src.analytics.visualization import create_bar_chart

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


# if st.button("Analyze", type="primary"):
#     if not question.strip():
#         st.warning("Please enter a question before analyzing.")
#
#     else:
#         try:
#             with st.spinner(
#                 "Analyzing your data... This may take a moment."
#             ):
#                 analysis = ask_data_analyst_detailed(question)
#
#             st.subheader("Analysis")
#             st.write(analysis["answer"])
#
#             with st.expander("View generated SQL"):
#                 st.code(analysis["sql"], language="sql")
#
#             with st.expander("View database results"):
#                 if analysis["results"]:
#                     st.dataframe(
#                         analysis["results"],
#                         width="stretch",
#                     )
#                 else:
#                     st.info("The query returned no rows.")
#
#         except AgentError as error:
#             st.error(str(error))
#
#         except Exception:
#             st.error(
#                 "Something went wrong while analyzing your data. "
#                 "Please try again."
#             )



#offline----------
if st.button("Analyze", type="primary"):
    if not question.strip():
        st.warning("Please enter a question before analyzing.")

    else:
        try:
            with st.spinner("Analyzing your data..."):
                analysis = run_offline_analysis(question)

                if analysis is None:
                    st.info(
                        "This question isn't supported by offline mode. "
                        "Trying Gemini AI..."
                    )
                    analysis = ask_data_analyst_detailed(question)
                else:
                    st.info("Offline demo mode: no Gemini API call was needed.")

            st.subheader("Analysis")
            st.write(analysis["answer"])

            # Visual analytics
            if analysis["results"]:
                fig = create_bar_chart(analysis["results"])

                if fig is not None:
                    st.subheader("Visual Analytics")
                    st.plotly_chart(fig, width="stretch")

            with st.expander("View generated SQL"):
                st.code(analysis["sql"], language="sql")

            with st.expander("View database results"):
                if analysis["results"]:
                    st.dataframe(
                        analysis["results"],
                        width="stretch",
                    )
                else:
                    st.info("The query returned no rows.")

        except AgentError as error:
            st.error(str(error))

        except Exception:
            st.error(
                "Something went wrong while analyzing your data. "
                "Please try again."
            )
