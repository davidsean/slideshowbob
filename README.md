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
## HTTPS test with dev server
```bash
flask run --cert=./certs/certificates.pem-chain --key=./certs/privatekey.key --port 443 --host 0.0.0.0
```