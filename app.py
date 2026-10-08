import os
import asyncio
import requests
import streamlit as st

from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")


# ============================================================
# STREAMLIT PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Aesthetic Clinic AI Support",
    page_icon="✨",
    layout="wide"
)


# ============================================================
# API KEY CHECK
# ============================================================

if not OPENAI_API_KEY or not SERPER_API_KEY:
    st.error(
        "OPENAI_API_KEY or SERPER_API_KEY is missing from your .env file."
    )
    st.stop()


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
    .main-title {
        font-size: 38px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #666;
        margin-bottom: 25px;
    }

    .answer-box {
        padding: 20px;
        border-radius: 12px;
        background-color: #f7f7f7;
        border: 1px solid #dddddd;
        margin-bottom: 20px;
    }

    .disclaimer {
        font-size: 13px;
        color: #777;
        padding: 10px;
        border-radius: 8px;
        background-color: #fafafa;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">✨ Aesthetic Clinic AI Support</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-powered support for skin, hair & aesthetic care queries</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="disclaimer">
    ℹ️ This application provides general educational information only.
    It is not a diagnosis and does not replace advice from a qualified
    medical or aesthetic professional.
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")


# ============================================================
# WEB SEARCH TOOL
# ============================================================

def web_search(query: str) -> str:
    """
    Search the web using the Serper API.
    This tool is used only by the Web Research Assistant.
    """

    url = "https://google.serper.dev/search"

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "q": query
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        organic_results = data.get("organic", [])

        if not organic_results:
            return "No web search results were found."

        results = []

        for item in organic_results[:5]:
            title = item.get("title", "No title")
            snippet = item.get("snippet", "No description")
            link = item.get("link", "")

            results.append(
                f"Title: {title}\n"
                f"Description: {snippet}\n"
                f"Link: {link}"
            )

        return "\n\n".join(results)

    except Exception as e:
        return f"Web search failed: {str(e)}"


# ============================================================
# FILE WRITING TOOL
# ============================================================

def save_to_file(
    query: str,
    clinic_answer: str,
    web_answer: str
) -> str:
    """
    Save the user's query and both agent answers
    into answers.txt.
    """

    try:
        with open(
            "answers.txt",
            "w",
            encoding="utf-8"
        ) as file:

            file.write("=" * 70 + "\n")
            file.write("AESTHETIC CLINIC AI SUPPORT\n")
            file.write("=" * 70 + "\n\n")

            file.write("USER QUERY\n")
            file.write("-" * 70 + "\n")
            file.write(query)
            file.write("\n\n")

            file.write("CLINIC ASSISTANT ANSWER\n")
            file.write("-" * 70 + "\n")
            file.write(clinic_answer)
            file.write("\n\n")

            file.write("WEB RESEARCH ASSISTANT ANSWER\n")
            file.write("-" * 70 + "\n")
            file.write(web_answer)
            file.write("\n\n")

            file.write("=" * 70 + "\n")
            file.write("END OF RECORD\n")
            file.write("=" * 70 + "\n")

        return "The query and both answers were successfully saved to answers.txt."

    except Exception as e:
        return f"File saving failed: {str(e)}"


# ============================================================
# OPENAI MODEL CLIENT
# ============================================================

model_client = OpenAIChatCompletionClient(
    model="gpt-5-mini",
    api_key=OPENAI_API_KEY
)


# ============================================================
# AGENT 1 — CLINIC ASSISTANT
# ============================================================

clinic_assistant = AssistantAgent(
    name="Clinic_Assistant",
    model_client=model_client,
    system_message="""
You are the Clinic Assistant for an aesthetic clinic.

Your job is to answer the user's question using your own
general knowledge.

Topics may include:
- Skin care
- Hair care
- Aesthetic procedures
- Common cosmetic treatments
- General treatment information
- Basic differences between procedures

Important rules:

1. Do not use any tools.
2. Answer directly using your own knowledge.
3. Give clear and easy-to-understand explanations.
4. Do not diagnose medical conditions.
5. Do not prescribe medicines.
6. Do not create personalized treatment plans.
7. For medical concerns, recommend consulting a qualified doctor
   or appropriate healthcare professional.
8. Keep the answer useful and reasonably concise.

After answering the user's question, stop.
"""
)


# ============================================================
# AGENT 2 — WEB RESEARCH ASSISTANT
# ============================================================

web_research_assistant = AssistantAgent(
    name="Web_Research_Assistant",
    model_client=model_client,
    tools=[web_search],
    system_message="""
You are the Web Research Assistant for an aesthetic clinic.

Your job is to research the user's question using the web_search tool
and then provide a useful answer based on the search results.

Important rules:

1. You MUST use the web_search tool before answering.
2. Use the search results to support your answer.
3. Summarize the important information clearly.
4. Do not diagnose medical conditions.
5. Do not prescribe medicines.
6. Do not create personalized treatment plans.
7. For medical concerns, recommend consulting a qualified doctor
   or appropriate healthcare professional.
8. Keep the answer clear and reasonably concise.

After providing your researched answer, stop.
"""
)


# ============================================================
# AGENT 3 — ENTRY AGENT
# ============================================================

entry_agent = AssistantAgent(
    name="Clinic_Entry_Agent",
    model_client=model_client,
    tools=[save_to_file],
    system_message="""
You are the Entry Agent for an aesthetic clinic.

Your job is to record the complete interaction.

You will receive:
1. The original user query.
2. The answer from Clinic_Assistant.
3. The answer from Web_Research_Assistant.

You MUST use the save_to_file tool.

Pass these three pieces of information to the tool:
- Original user query
- Clinic Assistant answer
- Web Research Assistant answer

After the file is successfully saved, provide a short confirmation.

Do not perform additional research.
Do not create another answer to the user's question.

Your final response should clearly confirm that
the information was saved to answers.txt.
"""
)


# ============================================================
# TEAM CONFIGURATION
# ============================================================

termination_condition = MaxMessageTermination(
    max_messages=6
)

team = RoundRobinGroupChat(
    participants=[
        clinic_assistant,
        web_research_assistant,
        entry_agent
    ],
    termination_condition=termination_condition
)


# ============================================================
# RUN MULTI-AGENT WORKFLOW
# ============================================================

async def run_clinic_support(query: str):
    """
    Run the three-agent sequential workflow.
    """

    result = await team.run(
        task=query
    )

    return result


# ============================================================
# EXTRACT ANSWERS
# ============================================================

def extract_answers(result):
    """
    Extract answers produced by the first two agents.
    """

    clinic_answer = ""
    web_answer = ""

    for message in result.messages:

        source = getattr(
            message,
            "source",
            ""
        )

        content = getattr(
            message,
            "content",
            ""
        )

        if not isinstance(content, str):
            continue

        if source == "Clinic_Assistant" and not clinic_answer:
            clinic_answer = content

        elif (
            source == "Web_Research_Assistant"
            and not web_answer
        ):
            web_answer = content

    return clinic_answer, web_answer


# ============================================================
# STREAMLIT USER INPUT
# ============================================================

st.subheader("💬 Ask Your Question")

query = st.text_area(
    "Enter your skin, hair or aesthetic care question:",
    placeholder=(
        "Example: What is the difference between PRP "
        "and a hair transplant?"
    ),
    height=120
)


# ============================================================
# RUN BUTTON
# ============================================================

if st.button(
    "✨ Get AI Support",
    use_container_width=True
):

    if not query.strip():
        st.warning("Please enter a question first.")

    else:

        with st.spinner(
            "🤖 Running the three AI agents..."
        ):

            try:

                result = asyncio.run(
                    run_clinic_support(query)
                )

                clinic_answer, web_answer = extract_answers(
                    result
                )

                # ====================================================
                # DISPLAY CLINIC ASSISTANT ANSWER
                # ====================================================

                st.subheader(
                    "🩺 Clinic Assistant"
                )

                if clinic_answer:
                    st.markdown(
                        '<div class="answer-box">',
                        unsafe_allow_html=True
                    )

                    st.write(clinic_answer)

                    st.markdown(
                        "</div>",
                        unsafe_allow_html=True
                    )

                else:
                    st.info(
                        "Clinic Assistant answer was not found."
                    )


                # ====================================================
                # DISPLAY WEB RESEARCH ANSWER
                # ====================================================

                st.subheader(
                    "🌐 Web Research Assistant"
                )

                if web_answer:
                    st.markdown(
                        '<div class="answer-box">',
                        unsafe_allow_html=True
                    )

                    st.write(web_answer)

                    st.markdown(
                        "</div>",
                        unsafe_allow_html=True
                    )

                else:
                    st.info(
                        "Web Research Assistant answer was not found."
                    )


                # ====================================================
                # ENTRY AGENT CONFIRMATION
                # ====================================================

                st.success(
                    "✅ The Entry Agent saved the interaction to answers.txt"
                )


                # ====================================================
                # SHOW SAVED FILE CONTENT
                # ====================================================

                if os.path.exists("answers.txt"):

                    with st.expander(
                        "📄 View saved answers.txt"
                    ):

                        with open(
                            "answers.txt",
                            "r",
                            encoding="utf-8"
                        ) as file:

                            saved_content = file.read()

                        st.text(saved_content)


            except Exception as e:

                st.error(
                    f"Something went wrong: {str(e)}"
                )


# ============================================================
# FOOTER
# ============================================================

st.write("")

st.caption(
    "Built with AutoGen AgentChat + OpenAI + Serper + Streamlit"
)