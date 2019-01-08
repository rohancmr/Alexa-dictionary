from ask_sdk_model.ui import SimpleCard


def build_help_response(speech_text, handler_input, alp_support):
    """Function to build response for launch request
    """
    if alp_support is False:
        handler_input.response_builder.speak(speech_text).ask(
            speech_text).set_card(SimpleCard(
                "Word Cyclopedia", speech_text))

        return handler_input.response_builder.response

    else:
        pass

