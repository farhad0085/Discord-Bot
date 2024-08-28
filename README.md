# Discord-Bot

## Installation

1. **Create a Bot**  
   If you haven't created a bot yet, follow these steps:
   - Visit the [Discord Developer Portal](https://discord.com/developers/applications).
   - Click on "New Application" to create a new application.
   - Select your newly created application and go to the "Bot" tab.
   - Enable message content intent to receive message content (otherwise message content will be blank)
   - Copy the token provided (Click on Reset token button) and replace the token in your `.env` file.


2. **Add Bot to Server**  
   - Navigate to "Installation" tab in your app and scroll to default install settings
   - In Guid install select bot in the scopes selector, and Administrator in permissions selector.
   - Copy the installation URL and paste it into your browser.
   - Follow the prompts to invite the bot to your server and complete the setup.


3. **Configure Your Environment**  
   Update your `.env` file with your bot's token and the guild (server) id.

By following these steps, your Discord bot should be properly set up and ready to use.
