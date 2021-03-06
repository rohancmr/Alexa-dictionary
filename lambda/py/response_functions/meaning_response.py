import json

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model.interfaces.alexa.presentation.apl.render_document_directive\
    import RenderDocumentDirective


def _load_apl_document(file_path):
    # type: (str) -> Dict[str, Any]
    """Load the apl json document at the path into a dict object."""
    with open(file_path) as f:
        return json.load(f)


def _get_speech_text(word, meaning):
    """Function to get speech from the meaning
    """
    speech_text = ""
    display_text = ""

    if meaning != {}:
        for value, meaning_list in meaning.items():
            no_of_meanings = len(meaning_list)

            for index, text in enumerate(meaning_list):

                if (index == 0 and no_of_meanings >= 1):
                    speech_text += "As a {}, {} means:\n * {}".format(
                        value, word, text['definition'])

                    display_text += "<u><b>{}</b></u> [{}]:\n * {}"\
                        .format(word, value, text['definition'])

                else:
                    speech_text += " or\n * {}".format(text['definition'])
                    display_text += "\n * {}".format(text['definition'])

            speech_text += "\n\n"
            display_text += "\n\n"

    else:
        speech_text += "Sorry, no result found."
        display_text += "Sorry, no result found."

    print("Meaning Speech Response: {}".format(speech_text))
    print("Meaning Display Response: {}".format(display_text))

    return speech_text, display_text


def build_meaning_response(word, meaning, handler_input, alp_support):
    """Function to build response for launch request
    """
    speech_text, display_text = _get_speech_text(word, meaning)

    if alp_support is False:
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Word Cyclopedia", speech_text)
        ).set_should_end_session(True)

    else:
        handler_input.response_builder.speak(speech_text).add_directive(
            RenderDocumentDirective(
                token="MeaningResponseToken",
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
                                    "url": "https://i.imgur.com/Du6Spym.jpg",
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
                                "text": display_text
                            }
                        },
                        "logoUrl": "https://i.imgur.com/eaFwECq.png"
                    }}))

    return handler_input.response_builder.response
