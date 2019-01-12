# -*- coding: utf-8 -*-

# This is Word Cyclopedia Alexa Skill, built using
# the implementation of handler classes approach in skill builder.
import logging
import yaml
import requests

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name, viewport

from response_functions.launch_response import build_launch_response
from response_functions.help_response import build_help_response
from response_functions.cancel_response import build_cancel_response
from response_functions.fallback_response import build_fallback_response
from response_functions.slot_prompt_response import build_slot_prompt_response
from response_functions.meaning_response import build_meaning_response


__program = 'dictionary.py'
__author = 'Rohan Kumar'
__version = '1.0'


sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Read the configuration in config.yml
with open('config.yml', 'r') as stream:
    CONFIG = yaml.load(stream)

print("config: {}".format(CONFIG))


def _check_viewpoint(handler_input):
    """Function to check viewpoint of the device
    """
    alp_support = False
    device_viewpoint = str(
        viewport.get_viewport_profile(handler_input.request_envelope))

    if device_viewpoint != "ViewportProfile.UNKNOWN_VIEWPORT_PROFILE":
        alp_support = True

    return alp_support


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = (CONFIG['welcome_message'] + "\n" +
                       CONFIG['help_message'])
        alp_support = _check_viewpoint(handler_input)

        return build_launch_response(speech_text, handler_input, alp_support)


class GetMeaningIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("WordMeaningIntent")(handler_input)

    def _get_meaning(self, word):
        """Function to get meaning of the word
        """
        '''dictionary = PyDictionary()
        meaning = dictionary.meaning(word)'''

        url = 'https://owlbot.info/api/v2/dictionary/{}'.format(word)

        response = requests.get(url)

        meaning = {}

        if response.status_code == 200:
            result = response.json()

            try:
                for i in result:
                    if i['type'] in meaning:
                        meaning[i['type']].append(i)
                    else:
                        meaning[i['type']] = [i]

            except Exception as err:
                print("No value fetched. Got Error: {}".format(err))

        return meaning

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        slots = handler_input.request_envelope.request.intent.slots
        word = slots['Query'].value

        if word is not None:
            meaning = self._get_meaning(word)
            alp_support = _check_viewpoint(handler_input)

            return build_meaning_response(word.upper(), meaning,
                                          handler_input, alp_support)

        else:
            # check if all mandatory slots are filled else prompt user for slot
            prompt = CONFIG['word_slot']
            alp_support = _check_viewpoint(handler_input)

            return build_slot_prompt_response(word, prompt, handler_input,
                                              alp_support, slots)


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = CONFIG['help_message']
        alp_support = _check_viewpoint(handler_input)

        return build_help_response(speech_text, handler_input, alp_support)


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = CONFIG['goodbye_message']
        alp_support = _check_viewpoint(handler_input)

        return build_cancel_response(speech_text, handler_input, alp_support)


class FallbackIntentHandler(AbstractRequestHandler):
    """AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = ("{} skill can't help you with that. {}"
                       .format(CONFIG['skill_name'], CONFIG['help_message']))
        reprompt = CONFIG['reprompt_message']
        alp_support = _check_viewpoint(handler_input)

        return build_fallback_response(speech_text, reprompt, handler_input,
                                       alp_support)


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speech = "Sorry, there was some problem. Please try again!!"
        handler_input.response_builder.speak(speech).ask(speech)

        return handler_input.response_builder.response


sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(GetMeaningIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

handler = sb.lambda_handler()
