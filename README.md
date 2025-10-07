# **City Paint Chatbot with Gemini**

#### Link: https://city-paint-chatbot.streamlit.app/
---

## **Description**
This Chatbot was built with Google Gemini (gemini-2.0-flash), enabling users to interactively estimate the total amount of paint and the number of 20L buckets required for large-scale painting projects through natural conversation.

The chatbot collects the following inputs from users:
1. Number of buildings
2. Painting scope (interior, exterior, or both)
3. Average floor area per building
4. Average number of floors
5. Number of paint coats

Based on these parameters, the chatbot performs an accurate calculation of the total paintable surface area and paint volume needed.

Additionally, the AI model incorporates 2 important factors:

- Non-paintable areas such as doors and windows, estimated at **12% of the total surface area**

- Paint loss and wastage, estimated at **5% of paint required.**

For estimation purposes, the chatbot assumes an average paint coverage of 10 m² per litre, and uses 20-litre paint buckets, which are the standard capacity for large construction projects.

<br>

## **Project structure**
- `main.py`: main Streamlit python script for the Chatbot
- `.env`: contains Google API Key
- `requirements.txt`: a list of all packages required to run the project
- `README.md`: markdown file
<br>

## **Set up and Installation**
1. Install Git: If Git is not already installed on your system, download and install it from [Git's official website](https://git-scm.com/). Follow the installation instructions for your operating system.
  
2. Clone the repository:
- Open a terminal or command prompt and navigate to the directory where you want to download the project.
- Type the following command to clone the repository from GitHub

```
git clone https://github.com/phuonganh-38/city-paint-chatbot.git
cd city-paint-chatbot
```

3. Add your Google API Key:

In the downnloaded folder, add a new file called `.env`.
In `.env`:
```
GOOGLE_API_KEY=your_api_key_here
```

4. Start the streamlit app by running:
```
streamlit run main.py
```
<br>

## **Screenshot**
<img width="635" height="875" alt="image" src="https://github.com/user-attachments/assets/9d3b6306-99bd-4c3c-ae25-311d1d6f023d" />



