import streamlit as st

# Page config
st.set_page_config(
    page_title="AI Vehicle Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Title
st.title("🤖 AI Vehicle Assistant")

st.markdown("""
Ask questions about:

- Fuel efficiency
- MPG
- Horsepower
- Engine performance
- Fuel saving tips
- CO₂ emissions
""")

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Sidebar
st.sidebar.title("💡 Suggested Questions")

st.sidebar.info("""
- How to improve MPG?
- What affects fuel efficiency?
- Which car saves more fuel?
- What is horsepower?
- How to reduce CO₂ emissions?
""")

# User input
user_input = st.chat_input(
    "Ask your vehicle question..."
)

# AI Response Logic
def generate_response(question):

    question = question.lower()

    if "mpg" in question:
        return """
MPG means Miles Per Gallon.

Higher MPG means:
✅ Better fuel efficiency
✅ Lower fuel cost
✅ Less pollution
"""

    elif "horsepower" in question:
        return """
Horsepower measures engine power.

Higher horsepower:
- Gives better speed
- Uses more fuel sometimes
"""

    elif "fuel efficiency" in question:
        return """
Fuel efficiency depends on:

- Vehicle weight
- Engine size
- Tire pressure
- Driving style
- Aerodynamics
"""

    elif "co2" in question or "pollution" in question:
        return """
Lower fuel consumption reduces CO₂ emissions.

Ways to reduce pollution:
✅ Maintain vehicle
✅ Drive smoothly
✅ Avoid excess weight
"""

    elif "save fuel" in question:
        return """
Fuel saving tips:

✅ Maintain steady speed
✅ Avoid sudden braking
✅ Keep tires inflated
✅ Reduce unnecessary load
"""

    else:
        return """
I can help with:

🚗 MPG
⛽ Fuel efficiency
🌍 CO₂ emissions
⚙️ Horsepower
💰 Fuel cost
"""

# Process user message
if user_input:

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Display user message
    with st.chat_message("user"):
        st.write(user_input)

    # Generate AI response
    response = generate_response(user_input)

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    # Display assistant response
    with st.chat_message("assistant"):
        st.write(response)