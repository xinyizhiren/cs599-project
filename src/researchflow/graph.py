"""Graph runner with optional LangGraph support and deterministic fallback."""

from __future__ import annotations

from time import perf_counter
from typing import Any, Callable

from .state import ResearchState


NodeFn = Callable[[ResearchState], dict[str, Any]]
NodeSpec = tuple[str, NodeFn]


def _merge_state(state: ResearchState, update: dict[str, Any]) -> ResearchState:
    merged: ResearchState = dict(state)
    merged.update(update)
    return merged


def _run_traced_node(name: str, fn: NodeFn, state: ResearchState) -> ResearchState:
    start = perf_counter()
    trace = list(state.get("node_trace", []))
    try:
        update = fn(state)
        elapsed_ms = round((perf_counter() - start) * 1000, 3)
        trace.append(
            {
                "node": name,
                "status": "success",
                "elapsed_ms": elapsed_ms,
                "output_keys": sorted(update.keys()),
            }
        )
        update["node_trace"] = trace
        return _merge_state(state, update)
    except Exception as exc:
        elapsed_ms = round((perf_counter() - start) * 1000, 3)
        trace.append(
            {
                "node": name,
                "status": "failed",
                "elapsed_ms": elapsed_ms,
                "error": str(exc),
            }
        )
        errors = list(state.get("errors", []))
        errors.append({"node": name, "message": str(exc)})
        failed_state = _merge_state(state, {"node_trace": trace, "errors": errors})
        # Preserve the trace for callers that catch the exception.
        exc.args = (*exc.args, failed_state)
        raise


def run_sequential_graph(initial_state: ResearchState, nodes: list[NodeSpec]) -> ResearchState:
    state: ResearchState = dict(initial_state)
    for name, fn in nodes:
        state = _run_traced_node(name, fn, state)
    state["graph_runtime"] = "sequential"
    return state


def _run_langgraph(initial_state: ResearchState, nodes: list[NodeSpec]) -> ResearchState:
    from langgraph.graph import END, START, StateGraph

    workflow = StateGraph(ResearchState)
    for name, fn in nodes:
        workflow.add_node(name, lambda state, n=name, f=fn: _run_traced_node(n, f, state))

    workflow.add_edge(START, nodes[0][0])
    for (current_name, _), (next_name, _) in zip(nodes, nodes[1:]):
        workflow.add_edge(current_name, next_name)
    workflow.add_edge(nodes[-1][0], END)

    graph = workflow.compile()
    final_state: ResearchState = graph.invoke(dict(initial_state))
    final_state["graph_runtime"] = "langgraph"
    return final_state


def run_research_graph(
    initial_state: ResearchState,
    nodes: list[NodeSpec],
    prefer_langgraph: bool = True,
) -> ResearchState:
    if prefer_langgraph:
        try:
            return _run_langgraph(initial_state, nodes)
        except ModuleNotFoundError:
            pass
        except Exception as exc:
            # LangGraph should never make the MVP unusable. The fallback keeps
            # the same node contract and records why the graph runtime changed.
            fallback_state = run_sequential_graph(initial_state, nodes)
            errors = list(fallback_state.get("errors", []))
            errors.append({"node": "graph_runtime", "message": f"LangGraph fallback: {exc}"})
            fallback_state["errors"] = errors
            fallback_state["graph_runtime"] = "sequential_fallback"
            return fallback_state
    return run_sequential_graph(initial_state, nodes)
