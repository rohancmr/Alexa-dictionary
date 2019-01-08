import json

from ask_sdk_model.ui import SimpleCard


def _load_apl_document(file_path):
    # type: (str) -> Dict[str, Any]
    """Load the apl json document at the path into a dict object."""
    with open(file_path) as f:
        return json.load(f)


def build_launch_response(speech_text, handler_input, alp_support):
    """Function to build response for launch request
    """
    if alp_support is False:
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Word Cyclopedia", speech_text)
        ).set_should_end_session(False)

        return handler_input.response_builder.response

    else:
        pass

