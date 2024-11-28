from fastapi import FastAPI, HTTPException, Path
from models import MsgPayload

app = FastAPI()
messages_list: dict[int, MsgPayload] = {}


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Hello"}


# About page route
@app.get("/about")
def about() -> dict[str, str]:
    return {"message": "This is the about page."}


# Route to add a message
@app.post("/messages/{msg_name}/")
def add_msg(msg_name: str) -> dict[str, MsgPayload]:
    # Generate an ID for the item based on the highest ID in the messages_list
    msg_id = max(messages_list.keys()) + 1 if messages_list else 0
    messages_list[msg_id] = MsgPayload(msg_id=msg_id, msg_name=msg_name)

    return {"message": messages_list[msg_id]}


# Route to list all messages
@app.get("/messages")
def message_items() -> dict[str, dict[int, MsgPayload]]:
    return {"messages:": messages_list}


@app.delete("/messages/{msg_id}/")
def delete_msg(msg_id: int = Path(..., title="The ID of the message to delete", ge=0)) -> dict[str, str]:
    """
    Delete a message by its ID.

    Args:
        msg_id (int): The ID of the message to delete.

    Returns:
        dict[str, str]: A dictionary with a message indicating the result.
    """
    if msg_id in messages_list:
        del messages_list[msg_id]
        return {"message": "Message deleted"}
    else:
        raise HTTPException(status_code=404, detail="Message not found")
