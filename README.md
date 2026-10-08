\# 🤖 AutoGen Customer Support Agent



A multi-agent AI customer support application built with \*\*AutoGen\*\* and \*\*Streamlit\*\*.



This project demonstrates how multiple AI agents can collaborate to handle customer-support questions, generate responses, and record the interaction.



\## 🚀 Features



\* 🤖 Multi-agent customer support workflow

\* 💬 Natural-language question answering

\* 🧠 AI-powered response generation

\* 🖥️ Streamlit web interface

\* 📝 Saves interaction results to `answers.txt`

\* 🔐 Supports environment-based API configuration

\* 🧩 Demonstrates collaborative AI agent architecture



\## 🏗️ Architecture



```text

User

&#x20; │

&#x20; ▼

Streamlit UI

&#x20; │

&#x20; ▼

AI Agent 1

&#x20; │

&#x20; ▼

AI Agent 2

&#x20; │

&#x20; ▼

Customer Support Response

&#x20; │

&#x20; ▼

answers.txt

```



The application uses multiple AI agents to demonstrate how tasks can be distributed between specialized agents.



\## 🔄 Workflow



```text

Customer Question

&#x20;      │

&#x20;      ▼

&#x20;  Streamlit UI

&#x20;      │

&#x20;      ▼

&#x20;  AI Agent(s)

&#x20;      │

&#x20;      ▼

Collaborative Processing

&#x20;      │

&#x20;      ▼

Final Response

&#x20;      │

&#x20;      ▼

&#x20;answers.txt

```



\## 🛠️ Technology Stack



| Technology | Purpose                      |

| ---------- | ---------------------------- |

| Python     | Application development      |

| AutoGen    | Multi-agent AI orchestration |

| Streamlit  | Web interface                |

| OpenAI     | LLM-powered responses        |



\## 📂 Project Structure



```text

buildathon-support-autogen/

│

├── app.py

├── README.md

├── answers.txt

└── .gitignore

```



`answers.txt` contains locally generated interaction results.



\## ⚙️ Setup



\### 1. Clone the repository



```bash

git clone https://github.com/spriyaldiary-ship-it/autogen-customer-support-agent.git

```



\### 2. Open the project



```bash

cd autogen-customer-support-agent

```



\### 3. Create a virtual environment



```bash

python -m venv venv

```



\### 4. Activate the virtual environment



\#### Windows PowerShell



```powershell

venv\\Scripts\\Activate.ps1

```



\### 5. Install dependencies



Install the packages required by the application:



```bash

pip install streamlit autogen-agentchat autogen-ext openai python-dotenv

```



> Package requirements may change with different AutoGen versions. Use the versions compatible with the current application code when necessary.



\### 6. Configure environment variables



Create a `.env` file in the project directory if the application requires environment-based API configuration.



Example:



```env

OPENAI\_API\_KEY=your\_openai\_api\_key

```



\*\*Never commit API keys or `.env` files to GitHub.\*\*



\### 7. Run the application



```bash

python -m streamlit run app.py

```



The application will open in your browser.



\## 💡 How It Works



1\. The user enters a customer-support question.

2\. The Streamlit application passes the request to the AI agent workflow.

3\. Multiple agents collaborate to process the request.

4\. The final response is returned to the user.

5\. The interaction can be recorded in `answers.txt`.



\## 🎯 Project Goal



The goal of this project is to gain practical experience building \*\*multi-agent AI applications with AutoGen\*\*.



The project explores:



\* AI agent collaboration

\* Multi-agent workflows

\* LLM integration

\* Customer-support automation

\* Streamlit application development



\## 📚 Learning Outcomes



This project provided hands-on experience with:



\* AutoGen

\* AI agents

\* Multi-agent orchestration

\* Agent collaboration

\* OpenAI API integration

\* Streamlit

\* Python

\* Environment variables

\* AI application development



\## 🔮 Future Improvements



Possible future enhancements include:



\* Conversation memory

\* RAG-based customer support

\* Specialized support agents

\* Agent task validation

\* Structured response storage

\* Customer history tracking

\* Database integration

\* Authentication

\* REST API deployment

\* Production-ready monitoring



\## 📄 Buildathon Project



This project was created as part of a \*\*Generative AI Architecture / AutoGen Multi-Agent Customer Support Buildathon\*\*.



\## 👩‍💻 Author



\*\*Priyal\*\*



Hands-on learning in:



\*\*Generative AI • AI Agents • AutoGen • RAG • AI Automation\*\*



