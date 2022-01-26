# Slideshow Bob
Facebook Messenger bot that creates a live slideshow from pictures it receives.
First, you setup a slideshow from a Google Photos album. The Facebook messenger bot will automatically add the pictures it receives from the Messenger app to the album.

This allows you to setup a live photo steam on a monitor and have the crowd add pictures.
Perfect for events, weddings, parties... just make sure you choose who you invite to the Facebook Page!

You'll want to stop the service so that guests don't hog up all your Google space.
# How it works
This server registers to facebook messenger events what will trigger its webhooks. It needs to be served on a publically accessible IP over https (port 443). It sits and listens for activity and creates a photo album containing all the accumulated pictures users sent it.

 - Install the bot on your facebook Page
 - People can navigate to the page and post pictures to the bot
 - The user name and profiles are added to the posted picture before uploaded to a Google Photo album
 - The album used as a slideshow (with a cast device)

# dev

## Architecture
The work is split between a server entity and clients. The server needs to be publicly visible over a secure connection.
I used no-ip dynamic DNS client with free certificates provided by TrustCor, but you can use what you want.

The server does two things:
 - secure web server
 - MQTT broker

The client's job is to subscribe to the MQTT broker display the images on a screen. New images will trigger MQTT events and let the client know how to obtain the images.

## Server
### Facebook tokens
Webhooks triggered by Messenger events needs to be registered to the Facebook page. It's good to take a look at the Facebook documentation at [https://developers.facebook.com/docs/messenger-platform/getting-started/app-setup/](https://developers.facebook.com/docs/messenger-platform/getting-started/app-setup/). This guide will have you create a `VERIFY_TOKEN` and generate for you a `PAGE_ACCESS_TOKEN`. Make sure to create a `.env` file in the repository root and defined these variables. See `.end-example`
### certs
You will need a SSL certs (`certificate.pem` and `private.key`) as well as the root CA from the issuer. With HAProxy these can be combined in a single file `full.pem` can can be placed under the `/certs/` directory 

## Docker
The Flask webserver is used to serve the webhook endpoints. The traffice first transits through a HAProxy service that handles SSL. The MQTT broker receives and transmits data pertaining to the messenger posts in a way that is easily used by clients. These are tied together using a Docker stack that can be started using:

```bash
docker compose -f docker/docker-compose.yaml build
docker compose -f docker/docker-compose.yaml up
```
from the root of the repository. You must define the token and creates the certs first (see above).
If everything works, Sending text messages to the Facebok page should generate some outputs.

## Debugging
``bash
curl -H "Content-Type: application/json" -X POST "localhost:443/webhook" -d '{"object": "page", "entry": [{"messaging": [{"message": "this is a test POST message"}]}]}' -k
```
Note,  `-k` is used to ignore SSL stuff for local testing.
