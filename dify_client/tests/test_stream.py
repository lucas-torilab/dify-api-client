import json
from pathlib import Path

import pytest

from dify_client.models import (
    MessageEndStreamResponse,
    NodeFinishedData,
    NodeStartedData,
    StreamEvent,
    WorkflowFinishedData,
    WorkflowStartedData,
    build_chat_stream_response,
)


FIXTURE_PATH = Path(__file__).parent / "fixtures" / "dify_sse_response.sse"

# Expected concrete type of `WorkflowsStreamResponse.data` per event, since
# it's a Union pydantic must pick the right member of via smart-mode
# matching.
EVENT_TO_WORKFLOW_DATA_TYPE = {
    "workflow_started": WorkflowStartedData,
    "node_started": NodeStartedData,
    "node_finished": NodeFinishedData,
    "workflow_finished": WorkflowFinishedData,
}

# Real chat-messages SSE response captured from Dify, one JSON payload
# per "data: " line. Used to make sure every event Dify actually sends
# deserializes correctly through build_chat_stream_response.
SSE_EVENTS = [
    json.loads(line[len("data:") :])
    for line in FIXTURE_PATH.read_text().splitlines()
    if line.startswith("data:")
]


def test_fixture_contains_expected_events():
    assert len(SSE_EVENTS) == 105
    assert {event["event"] for event in SSE_EVENTS} == {
        "workflow_started",
        "node_started",
        "node_finished",
        "agent_log",
        "message",
        "workflow_finished",
        "message_end",
    }


@pytest.mark.parametrize(
    "raw_event",
    SSE_EVENTS,
    ids=[f"{i}-{event['event']}" for i, event in enumerate(SSE_EVENTS)],
)
def test_build_chat_stream_response_maps_every_event(raw_event):
    response = build_chat_stream_response(raw_event)

    # Every event in the log is a real, known StreamEvent, so it must
    # never fall back to the catch-all IGNORED sentinel.
    assert response.event == raw_event["event"]
    assert response.event != StreamEvent.IGNORED
    assert response.task_id == raw_event["task_id"]

    # Serialization back out must not raise.
    response.model_dump()
    response.model_dump_json()

    expected_data_type = EVENT_TO_WORKFLOW_DATA_TYPE.get(raw_event["event"])
    if expected_data_type is not None:
        assert type(response.data) is expected_data_type


def test_message_events_deserialize_answer_text():
    message_events = [
        raw_event
        for raw_event in SSE_EVENTS
        if raw_event["event"] == "message"
    ]
    assert message_events

    responses = [
        build_chat_stream_response(raw_event) for raw_event in message_events
    ]
    for response, raw_event in zip(responses, message_events):
        assert response.answer == raw_event["answer"]
        assert response.message_id == raw_event["message_id"]

    full_answer = "".join(response.answer for response in responses)
    assert "Kaki" in full_answer


def test_message_end_usage_metadata_deserializes():
    raw_event = next(
        raw_event
        for raw_event in SSE_EVENTS
        if raw_event["event"] == "message_end"
    )

    response = build_chat_stream_response(raw_event)

    assert isinstance(response, MessageEndStreamResponse)
    assert (
        response.metadata.usage.total_tokens
        == raw_event["metadata"]["usage"]["total_tokens"]
    )
