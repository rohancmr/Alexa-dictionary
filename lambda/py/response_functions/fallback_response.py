import json


def _load_apl_document(file_path):
    # type: (str) -> Dict[str, Any]
    """Load the apl json document at the path into a dict object."""
    with open(file_path) as f:
        return json.load(f)


def build_fallback_response(speech_text, reprompt, handler_input, alp_support):
    """Function to build response for launch request
    """
    if alp_support is False:
        handler_input.response_builder.speak(speech_text).ask(reprompt)

        return handler_input.response_builder.response

    else:
        pass

