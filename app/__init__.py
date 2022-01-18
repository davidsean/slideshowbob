import logging
import os

from json import JSONDecodeError
from flask import Flask, request, Response
from dotenv import load_dotenv

from app.message_scraper import MessageScraper
from app.google_photos_helper import GooglePhotosHelper


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# load environmental variables from .env
load_dotenv()
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN')

def create_app(test_config=None):

    app = Flask(__name__)
    # Disable strict trailing slashes in URLs
    app.url_map.strict_slashes = False

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    @app.route('/webhook', methods=['GET'])
    def get_webhook()-> Response:
        """process GET webhook

        Returns:
            Response: respoonse object
        """
        logger.info('GET webhook')
        # extract query params
        mode = request.args.get('hub.mode', None)
        token = request.args.get('hub.verify_token', None)
        challenge = request.args.get('hub.challenge', None)
        logger.debug('mode: %s', mode)
        logger.debug('token: %s', token)
        logger.debug('challenge: %s', challenge)

        if (mode is not None and token is not None):
            if (mode=='subscribe' and token==VERIFY_TOKEN):
                logger.info('Webhook Verified')
                return Response(challenge, status=200)
        return Response("Forbidden", status=402)


    @app.route('/webhook', methods=['POST'])
    def post_webhook():
        """process POST webhook

        Returns:
            Response: respoonse object
        """
        logger.debug('POST webhook')
        try:
            payload:dict = request.json
        except JSONDecodeError as err:
            logger.warning('Invalid payload: %s', err)
            return Response('Invalid payload', status=400)
        logger.debug(payload)
        if ('object' in payload) and (payload['object']=='page') and ('entry' in payload):
            # iterate over possibly multiple entries
            for entry in payload['entry']:
                if 'messaging' in entry and ('message' in entry['messaging'][0]):
                    logger.debug('got message')
                    # should only get one
                    message = entry['messaging'][0]['message']
                    # Helpers.scrape_message(message)
                    sender_id = entry['messaging'][0]['sender']['id']
                    logger.info('got sender_id: %s', sender_id)
                    if 'attachments' in message:
                        # process all attachments
                        for attachment in message['attachments']:
                            if 'type' in attachment and attachment['type'] == 'image':
                                #process image attachment
                                logger.debug('process image attachment')
                                if 'payload' in attachment:
                                    url = attachment['payload']['url']
                                    logger.info('got url: %s', url)
                                    msg_scaper = MessageScraper(url,sender_id)
                                    img = msg_scaper.process_post()
        else:
            logger.warning('payload.object is not page or entry not present. payload: %s', payload)
            return Response('Invalid payload', status=400)
        return Response("EVENT_RECEIVED", status=200)


    return app

