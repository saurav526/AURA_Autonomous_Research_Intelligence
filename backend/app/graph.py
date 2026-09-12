from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, START, END

from .llm import chat
from .search import web_search


class State(TypedDict, total=False):
    query: str
    max_sources: int
    plan: List[str]
    sources: List[Dict[str, Any]]
    analysis: str
    verification: str
    final_answer: str
    confidence: float
    events: List[Dict[str, Any]]


def add_event(state, agent, detail):
    state.setdefault("events", []).append({
        "agent": agent,
        "status": "completed",
        "detail": detail
    })

    return state


def planner(state):
    prompt = f"""
Create a research plan for this question:

{state["query"]}

Return exactly 5 concise research tasks.
Cover:
1. Background
2. Current evidence
3. Competing views
4. Technical or quantitative evidence
5. Practical implications

Return one task per line.
"""

    text = chat(
        "You are a senior research planning agent.",
        prompt
    )

    plan = []

    for line in text.splitlines():
        line = line.strip()

        if line:
            line = line.lstrip("-•0123456789. ")
            plan.append(line)

    state["plan"] = plan[:5]

    return add_event(
        state,
        "Planner Agent",
        f"{len(state['plan'])} research tasks created"
    )


async def researcher(state):
    all_results = []

    for task in state["plan"]:
        results = await web_search(
            task,
            max(2, state["max_sources"] // 2)
        )

        all_results.extend(results)

    seen = set()
    unique_results = []

    for result in all_results:
        url = result.get("url", "")

        if url and url not in seen:
            seen.add(url)
            unique_results.append(result)

    state["sources"] = unique_results[:state["max_sources"]]

    return add_event(
        state,
        "Research Agent",
        f"{len(state['sources'])} sources collected"
    )


def analyst(state):
    evidence = "\n".join(
        f"- {source['title']} | {source['url']}\n"
        f"  {source.get('snippet', '')}"
        for source in state["sources"]
    )

    prompt = f"""
Question:

{state["query"]}


Research evidence:

{evidence}


Analyze the evidence carefully.

Separate:
- Established facts
- Reasonable inferences
- Trends
- Contradictions
- Limitations
- Missing evidence

Do not invent statistics.
Do not invent sources.
"""

    state["analysis"] = chat(
        "You are a rigorous research analysis agent.",
        prompt
    )

    return add_event(
        state,
        "Analysis Agent",
        "Research evidence analyzed"
    )


def verifier(state):
    source_urls = "\n".join(
        source["url"]
        for source in state["sources"]
    )

    prompt = f"""
Question:

{state["query"]}


Analysis:

{state["analysis"]}


Sources:

{source_urls}


Act as an adversarial fact-checking agent.

Identify:
- Unsupported claims
- Contradictions
- Weak evidence
- Potential hallucinations
- Claims that require cautious wording

At the end provide:

Confidence Score: X/100
"""

    state["verification"] = chat(
        "You are a skeptical fact-checking and verification agent.",
        prompt
    )

    import re

    scores = re.findall(
        r"(?:confidence\s*score|confidence|score)"
        r"[^0-9]{0,20}"
        r"([0-9]{1,3})",
        state["verification"],
        re.IGNORECASE
    )

    if scores:
        score = min(100, float(scores[-1]))
        state["confidence"] = score / 100
    else:
        state["confidence"] = 0.75

    return add_event(
        state,
        "Verification Agent",
        "Claims audited"
    )


def synthesizer(state):
    sources = "\n".join(
        f"[{index + 1}] {source['title']} - {source['url']}"
        for index, source in enumerate(state["sources"])
    )

    prompt = f"""
Create a professional research report answering:

{state["query"]}


ANALYSIS:

{state["analysis"]}


FACT CHECK:

{state["verification"]}


SOURCES:

{sources}


Use the following structure:

Executive Summary

Key Findings

Evidence

Risks and Uncertainty

Recommendations

Sources

Use source references such as [1], [2], [3].

Do not fabricate citations.
Only use the sources supplied above.
Clearly mention uncertainty when evidence is weak.
"""

    state["final_answer"] = chat(
        "You are the final senior research editor.",
        prompt,
        0.15
    )

    return add_event(
        state,
        "Synthesis Agent",
        "Final research report generated"
    )


def build_graph():

    workflow = StateGraph(State)

    workflow.add_node(
        "planner",
        planner
    )

    workflow.add_node(
        "researcher",
        researcher
    )

    workflow.add_node(
        "analyst",
        analyst
    )

    workflow.add_node(
        "verifier",
        verifier
    )

    workflow.add_node(
        "synthesizer",
        synthesizer
    )

    workflow.add_edge(
        START,
        "planner"
    )

    workflow.add_edge(
        "planner",
        "researcher"
    )

    workflow.add_edge(
        "researcher",
        "analyst"
    )

    workflow.add_edge(
        "analyst",
        "verifier"
    )

    workflow.add_edge(
        "verifier",
        "synthesizer"
    )

    workflow.add_edge(
        "synthesizer",
        END
    )

    return workflow.compile()


graph = build_graph()


async def run_research(
    query: str,
    max_sources: int = 8
):

    initial_state = {
        "query": query,
        "max_sources": max_sources,
        "events": []
    }

    result = await graph.ainvoke(
        initial_state
    )

    return result