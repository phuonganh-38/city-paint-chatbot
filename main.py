import os
import math
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai


# --- Load environment variables ---
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


# --- Streamlit page setup ---
st.set_page_config(
  page_title="City Paint Estimator",
  page_icon='🏗️',
  layout="centered"
)

st.title("City Paint Estimator with Gemini")
st.caption("Your smart assistant to estimate how many paint buckets are needed for the entire city.")

# --- Initialize model ---
if not GOOGLE_API_KEY:
  st.error("Missing API Key. Please set API key in your environment.")
else:
  gen_ai.configure(api_key=GOOGLE_API_KEY)
  model=gen_ai.GenerativeModel("gemini-2.0-flash")

# --- List of predefined questions ---
questions = [
    {
      "key": "scope",
      "question": "What is the scope of your painting project? (type *interior / exterior / both*)",
      "type": "choice",
      "options": ["interior", "exterior", "both"]
    },
    {
      "key": "buildings",
      "question": "How many buildings do you plan to paint?",
      "type": "number"
    },
    {
      "key": "area",
      "question": "What is the average wall area (in m²) of each building?",
      "type": "number"
    },
    {
      "key": "floors",
      "question": "How many floors does each building have on average?",
      "type": "number"
    },
    {
      "key": "layers",
      "question": "How many coats of paint do you plan to apply?",
      "type": "number"
    }
]

# --- Initialize session state ---
if "chat_history" not in st.session_state:
  st.session_state.chat_history = [("assistant", questions[0]["question"])]
if "answers" not in st.session_state:
  st.session_state.answers = {}
if "current_question" not in st.session_state:
  st.session_state.current_question = 0
if "completed" not in st.session_state:
  st.session_state.completed = False
if "waiting_for_restart" not in st.session_state:
  st.session_state.waiting_for_restart = False

# Display chat history
for sender, text in st.session_state.chat_history:
  with st.chat_message(sender):
    st.markdown(text)


if st.session_state.completed:
  pass

# --- Calculation function ---
def estimator(scope, buildings, avg_area, 
              floors, coats, can_vol=20, loss=0.05, 
              coverage=10, openings_rate=0.12):
  k = {"interior": 3.5, "exterior": 1.2, "both": 4.7}[scope]
  area_paint = k * avg_area * floors * buildings
  net_area = area_paint * (1 - openings_rate)
  liters_needed = net_area * coats / coverage
  liters_with_loss = liters_needed * (1 + loss)
  cans = math.ceil(liters_with_loss / can_vol)
  return {
    "area_paint": area_paint,
    "net_area": net_area,
    "liters_needed": liters_needed,
    "liters_with_loss": liters_with_loss,
    "cans": cans
  }


# --- Handle users'response ---
if not st.session_state.completed and not st.session_state.waiting_for_restart:
  user_input = st.chat_input("Enter your answer here")
  if user_input:
    current_key = questions[st.session_state.current_question]["key"]
    question_type = questions[st.session_state.current_question]["type"]

    if question_type == "number":
      try:
        # Convert to integers or floats
        parsed = float(user_input)
      except ValueError:
        with st.chat_message("assistant"):
          st.warning("⚠️ Please enter a valid number.")
        st.stop()

      if parsed <=0:
        with st.chat_message("assistant"):
          st.warning("⚠️ The number must be greater than 0.")
        st.stop()
      
      if current_key in ["buildings", "floors"]:
        if not parsed.is_integer():
          with st.chat_message("assistant"):
            st.warning("⚠️ Please enter a whole number.")
          st.stop()
        parsed = int(parsed)
      
      if current_key == "layers" and parsed > 3:
        with st.chat_message("assistant"):
          st.warning("⚠️ You don’t need more than 3 coats. I’ll use 3 as the maximum.")
        parsed = 3

      user_answer = parsed
    
    else:
      user_answer = user_input.strip().lower()

      if current_key == "scope" and user_answer not in ["interior", "exterior", "both"]:
        with st.chat_message("assistant"):
          st.warning("⚠️ Please type interior or exterior or both.")
        st.stop()

    # Store answer and append user message to history
    st.session_state.answers[current_key] = user_answer
    st.session_state.chat_history.append(("user", str(user_input)))

    if st.session_state.current_question + 1 < len(questions):
      st.session_state.current_question += 1
      next_question = questions[st.session_state.current_question]["question"]
      st.session_state.chat_history.append(("assistant", next_question))
    else: 
      st.session_state.completed = True

    st.rerun()


if st.session_state.completed and not st.session_state.waiting_for_restart:
  # Get user inputs 
  ans = st.session_state.answers

  # Compute
  result = estimator(
    scope=ans["scope"],
    buildings=ans["buildings"],
    avg_area=ans["area"],
    floors=ans["floors"],
    coats=ans["layers"],
    can_vol=20,
    loss=0.05,
    coverage=10,
    openings_rate=0.12
    )

  result_text = (
    f"Net area after excluding doors/windows: {result['net_area']:.0f} m²  \n" 
    f"Total liters required ({int(ans['layers'])} coat(s)): {result['liters_needed']:.0f} L  \n"
    f"You'll need approximately **{result['cans']} buckets** (20L each) to paint the entire city."
  )

  # Print result
  st.session_state.chat_history.append(("assistant", result_text))

  # Ask to restart calculation
  st.session_state.chat_history.append(("assistant", "Would you like to make another calculation? (yes / no)"))
  st.session_state.waiting_for_restart = True
  st.rerun()
  
if st.session_state.waiting_for_restart:
  user_input = st.chat_input("Enter your answer here")
  
  if user_input:
    user_input = user_input.strip().lower()
    st.session_state.chat_history.append(("user", user_input))

    if user_input in ["yes", "yess", "y", "sure", "ok"]:
      st.session_state.answers = {}
      st.session_state.current_question = 0
      st.session_state.completed = False
      st.session_state.waiting_for_restart = False
      st.session_state.chat_history = [("assistant", questions[0]["question"])]
      st.rerun()
    else:
      with st.chat_message("assistant"):
        st.write("Thank you for using City Paint Estimator with Gemini.")
      st.session_state.waiting_for_restart = False
      st.stop()




