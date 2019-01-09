import json

from ask_sdk_model.dialog import ElicitSlotDirective


from ask_sdk_model.interfaces.alexa.presentation.apl.render_document_directive\
    import RenderDocumentDirective


def _load_apl_document(file_path):
    # type: (str) -> Dict[str, Any]
    """Load the apl json document at the path into a dict object."""
    with open(file_path) as f:
        return json.load(f)


def build_slot_prompt_response(prompt, handler_input, alp_support, slots):
    """Function to build response for launch request
    """
    if alp_support is False:
        return handler_input.response_builder.speak(
            prompt).ask(prompt).add_directive(
            ElicitSlotDirective(slot_to_elicit=slots['Query'].name)
        ).response

    else:
        handler_input.response_builder.speak(prompt).add_directive(
            RenderDocumentDirective(
                token="SlotPromptToken",
                document=_load_apl_document("./apl/long_text.json"),
                datasources={
                    "bodyTemplate1Data": {
                        "type": "object",
                        "objectId": "bt1Sample",
                        "backgroundImage": {
                            "contentDescription": None,
                            "smallSourceUrl": None,
                            "largeSourceUrl": None,
                            "sources": [
                                {
                                    "url": "https://i.imgur.com/qhWWsFT.jpg",
                                    "size": "small",
                                    "widthPixels": 0,
                                    "heightPixels": 0
                                },
                                {
                                    "url": "https://i.imgur.com/qhWWsFT.jpg",
                                    "size": "large",
                                    "widthPixels": 0,
                                    "heightPixels": 0
                                }
                            ]
                        },
                        "title": "",
                        "textContent": {
                            "primaryText": {
                                "type": "PlainText",
                                "text": prompt
                            }
                        },
                        "logoUrl": "https://i.imgur.com/eaFwECq.png"
                    }}))

        return handler_input.response_builder.response
