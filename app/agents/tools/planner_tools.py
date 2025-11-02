# app/agents/tools/planner_tools.py
from langchain_community.tools import DuckDuckGoSearchRun


# DuckDuckGo search tool for finding attractions, POIs, and travel information
web_search = DuckDuckGoSearchRun(
    name="web_search",
    description="Search the web for travel information, attractions, points of interest (POIs), and activities in a destination city. Use this to find popular sights, cultural sites, restaurants, shopping areas, and other tourist attractions.",
)


if __name__ == "__main__":
    print(web_search.invoke("sri lanka colombo hotels"))