import json
from typing import Optional, cast

from langchain.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from langchain_core.runnables import RunnableConfig

from app.agents.requirements_graph import requirements_graph
from app.agents.travel_system_agents import planner_agent, booker_agent
from app.agents.requirements_graph import RequirementsGraphState


checkpointer = InMemorySaver()


class TravelSystemState(MessagesState):
    """State for the full travel planning pipeline."""

    requirements: Optional[dict]  # CompleteRequirements dict from requirements graph
    itinerary: Optional[dict]  # Itinerary dict from planner agent
    bookings: Optional[dict]  # Bookings dict from booker agent


def requirements_subgraph_node(
    state: TravelSystemState, config: RunnableConfig
) -> TravelSystemState:
    """
    Invoke the requirements graph as a subgraph.
    The subgraph shares 'messages' and 'requirements' state with parent.

    Handles interrupt loop internally to gather all user input before proceeding.
    Similar to requirements_graph.py main block pattern.
    """
    # Create subgraph state from parent state
    subgraph_state = RequirementsGraphState(
        messages=state["messages"],
        requirements_complete=False,
        interruption_message="",
        requirements=state.get("requirements"),
    )

    # Extract parent's thread_id from config and derive subgraph thread_id
    # RunnableConfig is dict-like with "configurable" key containing thread_id
    configurable = config.get("configurable", {}) if config else {}
    parent_thread_id = configurable.get("thread_id", "main-thread")
    subgraph_thread_id = f"{parent_thread_id}-requirements"
    subgraph_config = {"configurable": {"thread_id": subgraph_thread_id}}

    # Invoke the compiled requirements graph
    subgraph_result = requirements_graph.invoke(
        subgraph_state,
        subgraph_config,
    )

    # Handle interrupt loop - similar to requirements_graph.py
    while True:
        if "__interrupt__" in subgraph_result:
            # Extract interrupt message
            interrupt_value = subgraph_result["__interrupt__"]
            if isinstance(interrupt_value, list) and len(interrupt_value) > 0:
                interrupt_message = str(interrupt_value[0].value)
            else:
                interrupt_message = str(interrupt_value)

            # Display interrupt message to user
            print(f"\n{interrupt_message}")

            # Get user input
            user_input = input("Your response: ").strip()

            # Resume execution with user input
            subgraph_result = requirements_graph.invoke(
                Command(resume=user_input),
                subgraph_config,
            )
        else:
            # No interrupt, execution completed
            break

    # Extract requirements from completed subgraph execution
    requirements = subgraph_result.get("requirements")

    # The result contains 'requirements' field populated when complete
    return cast(TravelSystemState, {
        "messages": [AIMessage(content=json.dumps(requirements), name="requirements")],
        "requirements": requirements,
    })

def planner_agent_node(state: TravelSystemState) -> TravelSystemState:
    """
    Invoke planner agent to create itinerary based on requirements.
    """
    # requirements = state.get("requirements")

#     # Format requirements into context message for planner
#     requirements_str = json.dumps(requirements, indent=2)
#     planner_prompt = f"""Based on the following travel requirements, create a day-by-day itinerary:
    
# {requirements_str}"""

    # response = planner_agent.invoke({"messages": HumanMessage(content=planner_prompt)})

    # Invoke planner agent
    response = planner_agent.invoke(
        {"messages": state["messages"]}
    )

    itinerary = response["structured_response"].itinerary.model_dump()

    return cast(TravelSystemState, {
        "messages": [AIMessage(content=json.dumps(itinerary), name="planner")],
        "itinerary": itinerary,
    })


def booker_agent_node(state: TravelSystemState) -> TravelSystemState:
    """
    Invoke booker agent to book flights and hotels based on requirements and itinerary.
    """
#     requirements = state.get("requirements")
#     itinerary = state.get("itinerary")

#     # Format booking context
#     requirements_str = json.dumps(requirements, indent=2)
#     itinerary_str = json.dumps(itinerary, indent=2)

#     booker_prompt = f"""Based on the following requirements and itinerary, book the flights and hotels:

# REQUIREMENTS:
# {requirements_str}

# ITINERARY:
# {itinerary_str}

# Extract the flight ID from the confirmed flight in requirements and book it.
# For hotels, use the destination city and dates from the itinerary or requirements to book a hotel.
# Return booking confirmations for both flight and hotel."""

    # Invoke booker agent
    # response = booker_agent.invoke({"messages": [HumanMessage(content=booker_prompt)]})
    response = booker_agent.invoke({"messages": state["messages"]})

    # Extract structured bookings from response
    bookings = response["structured_response"].bookings.model_dump()

    return cast(TravelSystemState, {
        "messages": [AIMessage(content=json.dumps(bookings), name="booker")],
        "bookings": bookings,
    })


# Build the graph
graph = StateGraph(TravelSystemState)

graph.add_node("requirements_subgraph", requirements_subgraph_node)
graph.add_node("planner", planner_agent_node)
graph.add_node("booker", booker_agent_node)

# Define flow
graph.add_edge(START, "requirements_subgraph")
graph.add_edge("requirements_subgraph", "planner")
graph.add_edge("planner", "booker")
graph.add_edge("booker", END)

# Compile the graph
travel_system_graph = graph.compile(checkpointer=checkpointer)


if __name__ == "__main__":
    initial_state = TravelSystemState(
        messages=[
            HumanMessage(
                content="I want to go to Seoul(ICN) from Tokyo(NRT). My dates are flexible."
            )
        ],
        requirements=None,
        itinerary=None,
        bookings=None,
    )

    config = {"configurable": {"thread_id": "thread-1"}}

    # Invoke the graph - interrupt loop is now handled inside requirements_subgraph_node
    result = travel_system_graph.invoke(initial_state, config)

    print("\n=== FINAL RESULTS ===")
    print(f"Requirements: {json.dumps(result.get('requirements'), indent=2)}")
    print(f"\nItinerary: {json.dumps(result.get('itinerary'), indent=2)}")
    print(f"\nBookings: {json.dumps(result.get('bookings'), indent=2)}")
