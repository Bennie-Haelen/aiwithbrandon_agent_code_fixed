import asyncio  
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from memory_agent.agent import memory_agent
from utils import call_agent_async

load_dotenv()

# ===== PART 1: Initialize Persistent Session Service =====
# Using SQLLite database for persistent storage
db_url = "sqlite:///./my_agent_data.db"
session_service = DatabaseSessionService(db_url=db_url)

# ===== PART 2: Define Initial State =====
initial_state = {
    "user_name": "Brandon Hancock",
    "reminders": []
}

async def main_async():
    APP_NAME = "Memory Agent"
    USER_ID = "aiwithbrandon"

    # ===== PART 3: Session Management - Find or Create =====
    # Check for existing sessions for this user
    sessions_response = await session_service.list_sessions(
        app_name=APP_NAME,
        user_id=USER_ID
    )

    # If there is an existing session, use it; otherwise, create a new one
    if sessions_response.sessions:
        SESSION_ID = sessions_response.sessions[0].id
        print(f"Continuing existing session: {SESSION_ID}")
    else:
        # Create a new session with initial state
        new_session = await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            state=initial_state
        )
        SESSION_ID = new_session.id
        print(f"Created new session: {SESSION_ID}")
  
    # ===== PART 4: Agent Runner Setup =====
    runner = Runner(
        agent=memory_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )
        
    # ===== PART 5: Interactive Conversation Loop =====
    print("\nWelcome to Memory Agent Chat!")
    print("Your reminders will be remembered across conversations.")
    print("Type 'exit' or 'quit' to end the conversation.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Ending conversation. Your data has been saved to the database.")
            break
        # Process the user query through the agent
        await call_agent_async(
           runner=runner,
           user_id=USER_ID,
           session_id=SESSION_ID,
           query=user_input)

if __name__ == "__main__":
    asyncio.run(main_async())