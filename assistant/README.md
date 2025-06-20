Set up and configure an AI assistant (or chat) cog for your server with one of OpenAI's ChatGPT language models.<br/><br/>Features include configurable prompt injection, dynamic embeddings, custom function calling, and more!<br/><br/>- **[p]assistant**: base command for setting up the assistant<br/>- **[p]chat**: talk with the assistant<br/>- **[p]convostats**: view a user's token usage/conversation message count for the channel<br/>- **[p]clearconvo**: reset your conversation with the assistant in the channel

# Authentication Methods

This cog supports two methods for authenticating with Google AI services:

*   **Google AI Studio Key**: A simpler method using an API key obtained directly from Google AI Studio. Suitable for quick setups and personal use.

## Google AI Studio Key

This key is used for authenticating with Google's Gemini models via Google AI Studio. You can set this key in two ways:

1.  **Using the Admin Command (Recommended for most users)**:
    *   The bot owner or an administrator can set the API key globally using the following command:
        ```bash
        [p]assistant setgaistudiokey <your_api_key>
        ```
        Replace `<your_api_key>` with the actual key obtained from [Google AI Studio](https://aistudio.google.com/).
    *   To clear a previously set key using this command, use:
        ```bash
        [p]assistant setgaistudiokey clear
        ```

2.  **Setting an Environment Variable (Advanced)**:
    *   You can set the `GOOGLE_AI_STUDIO_API_KEY` environment variable in the environment where your Red Discord Bot is running.
        ```bash
        export GOOGLE_AI_STUDIO_API_KEY="your_actual_api_key"
        ```
    *   The bot will automatically detect and use this key upon startup.
    *   This method is often preferred for deployments using Docker or other containerization systems, as it keeps sensitive keys out of bot commands or configuration files that might be version-controlled.

**Important Notes**:
*   **Precedence**: If the `GOOGLE_AI_STUDIO_API_KEY` environment variable is set, it will **always take precedence** over any key set using the `setgaistudiokey` command.
*   **Security**: Treat your API key like a password. Do not share it publicly or commit it to version control.
*   **Usage**: This API key is specifically for accessing Gemini models through the Google AI Studio endpoint. For Vertex AI access (another way to use Gemini), you'll need to configure GCP Authentication.

*   **Google Cloud Platform (GCP) Authentication**: A more robust method using service accounts for accessing Google Cloud services, including Vertex AI which can also run Gemini models. Recommended for self-hosted bots or when running within a GCP environment, providing more fine-grained control and security.

## Google Cloud Platform (GCP) Authentication

This method is recommended for self-hosted bots or those running in a GCP environment. It involves using a service account for more secure and fine-grained access control.

1.  **Set up a Google Cloud Project**:
    *   If you don't have one already, create a new project in the [Google Cloud Console](https://console.cloud.google.com/).
    *   Ensure the Vertex AI API is enabled for your project. You can find this under "APIs & Services" > "Enabled APIs & services". If not listed, click "+ ENABLE APIS AND SERVICES" and search for "Vertex AI API" to enable it.

2.  **Create a Service Account**:
    *   In the Google Cloud Console, navigate to "IAM & Admin" > "Service Accounts".
    *   Click "+ CREATE SERVICE ACCOUNT".
    *   Give your service account a name (e.g., "gemini-assistant-bot").
    *   Grant the service account the "Vertex AI User" role (roles/aiplatform.user). This role provides the necessary permissions to access Vertex AI services, including Gemini models.
    *   Click "Done".

3.  **Create and Download a Service Account Key**:
    *   After creating the service account, find it in the list and click on it.
    *   Go to the "KEYS" tab.
    *   Click "ADD KEY" > "Create new key".
    *   Choose "JSON" as the key type and click "CREATE".
    *   A JSON file containing the key will be downloaded to your computer. **Keep this file secure and do not share it publicly.**

4.  **Set Environment Variable**:
    *   Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable in the environment where your Red Hat Discord bot is running. This variable must contain the full path to the JSON key file you downloaded.
        *   **Linux/macOS**: `export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"`
        *   **Windows (PowerShell)**: `$env:GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"`
        *   For Docker deployments, you can set this environment variable in your Dockerfile or docker-compose.yml.
    *   The bot needs to be restarted after setting this environment variable for it to take effect.

5.  **Configure Cog Settings**:
    *   Set your Google Cloud Project ID in the cog's settings. This is usually the Project ID (not the project name or number) associated with your service account.
        ```
        [p]assistant setgoogleprojectid <your-project-id>
        ```
    *   *(Developer Note: The specific command to set this was not identified during review, but it's stored in `db.google_project_id` as noted in the Gemini section. Bot owners should verify the exact command or method provided by the cog version they are using.)*

Once these steps are completed, the cog should be able to authenticate with Google Cloud services using the provided service account credentials.

Choose the method that best suits your setup and needs. Detailed instructions for each are provided below.

# Google Gemini Model Support

The Assistant cog also supports Google's Gemini models, allowing you to leverage their advanced capabilities.

## How to Use Gemini Models

To use a Gemini model, you first need to select it using the model selection command:
- `[p]assistant model <model_name>`

You can find a list of available Gemini models (e.g., `gemini-2.5-pro`, `gemini-1.5-flash`) by either:
- Checking the output of `[p]assistant model` with no arguments (if it lists available models).
- Referring to the cog's internal model list (though this might not be directly visible to end-users, admins can be aware).

Once a Gemini model is selected, your interactions via the `[p]chat` command and other features will utilize that model.

## Prerequisites for Gemini

For Gemini models to function correctly, the bot owner must have Google Cloud Platform (GCP) authentication configured as described in the **"Google Cloud Platform (GCP) Authentication"** section above. This includes:

1.  **Setting up a Google Cloud Project and enabling the Vertex AI API.**
2.  **Creating a Service Account with the "Vertex AI User" role (or other roles that grant `aiplatform.endpoints.predict` permission) and downloading its JSON key.**
3.  **Setting the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to the path of the downloaded JSON key file.**
4.  **Configuring the Google Cloud Project ID in the cog's settings** (e.g., using `[p]assistant setgoogleprojectid <your-project-id>`).

Ensure all steps in the "Google Cloud Platform (GCP) Authentication" section have been completed. The "Vertex AI User" role is generally recommended as it provides comprehensive access for Gemini functionalities. Without proper authentication, attempts to use Gemini models will result in errors.

# Channel Context Feature

The Channel Context feature allows the assistant to consider recent messages from the current channel when generating a response. This can help the assistant maintain context over a longer interaction or refer to recent topics discussed in the channel.

- **`channel_context_enabled`**: This is the main setting to turn the feature on or off. When enabled, the bot will fetch recent messages from the channel.
- **`channel_context_max_messages`**: Defines the maximum number of recent messages (from 0 to 50) that will be included as context. A value of 0 effectively disables the context gathering for that channel, even if the main feature is enabled.
- **`include_bot_messages_in_context`**: A boolean setting (true/false) that determines whether messages from other bot users should be included in the gathered channel context.

## `[p]channelcontext` Command Group

This group of commands allows administrators to manage the Channel Context feature settings.

### `[p]channelcontext enable <true_false>`
Enables or disables the Channel Context feature for the server.
- **`<true_false>`**: Required. Set to `true` to enable or `false` to disable.
- Aliases: `toggle`

### `[p]channelcontext maxmessages <messages>`
Sets the maximum number of recent channel messages to include as context.
- **`<messages>`**: Required. An integer between 0 and 50. Setting to 0 means no messages will be fetched, even if the feature is enabled.

### `[p]channelcontext includebot <true_false>`
Determines whether messages from other bot users are included in the channel context.
- **`<true_false>`**: Required. Set to `true` to include messages from other bots, or `false` to exclude them.
- Aliases: `includebots`

### `[p]channelcontext showsettings`
Displays the current settings for the Channel Context feature.
- Aliases: `view`, `settings`

# /draw (Slash Command)
Generate an image with Dalle-3<br/>
 - Usage: `/draw <prompt> [size] [quality] [style]`
 - `prompt:` (Required) What would you like to draw?
 - `size:` (Optional) The size of the image to generate
 - `quality:` (Optional) The quality of the image to generate
 - `style:` (Optional) The style of the image to generate

 - Checks: `Server Only`
# /tldr (Slash Command)
Summarize whats been happening in a channel<br/>
 - Usage: `/tldr [timeframe] [question] [channel] [member] [private]`
 - `timeframe:` (Optional) The number of messages to scan
 - `question:` (Optional) Ask for specific info about the conversation
 - `channel:` (Optional) The channel to summarize messages from
 - `member:` (Optional) Target a specific member
 - `private:` (Optional) Only you can see the response

 - Checks: `Server Only`
# [p]chathelp
Get help using assistant<br/>
 - Usage: `[p]chathelp`
# [p]chat
Chat with [botname]!<br/>

Conversations are *Per* user *Per* channel, meaning a conversation you have in one channel will be kept in memory separately from another conversation in a separate channel<br/>

**Optional Arguments**<br/>
`--outputfile <filename>` - uploads a file with the reply instead (no spaces)<br/>
`--extract` - extracts code blocks from the reply<br/>
`--last` - resends the last message of the conversation<br/>

**Example**<br/>
`[p]chat write a python script that prints "Hello World!"`<br/>
- Including `--outputfile hello.py` will output a file containing the whole response.<br/>
- Including `--outputfile hello.py --extract` will output a file containing just the code blocks and send the rest as text.<br/>
- Including `--extract` will send the code separately from the reply<br/>
 - Usage: `[p]chat <question>`
 - Aliases: `ask, escribir, razgovor, discuter, plaudern, 채팅, charlar, baterpapo, and sohbet`
 - Cooldown: `1 per 6.0 seconds`
 - Checks: `server_only`
# [p]convostats
Check the token and message count of yourself or another user's conversation for this channel<br/>

Conversations are *Per* user *Per* channel, meaning a conversation you have in one channel will be kept in memory separately from another conversation in a separate channel<br/>

Conversations are only stored in memory until the bot restarts or the cog reloads<br/>
 - Usage: `[p]convostats [user]`
 - Checks: `server_only`
# [p]convoclear
Reset your conversation with the bot<br/>

This will clear all message history between you and the bot for this channel<br/>
 - Usage: `[p]convoclear`
 - Aliases: `clearconvo`
 - Checks: `server_only`
# [p]convopop
Pop the last message from your conversation<br/>
 - Usage: `[p]convopop`
 - Checks: `bot_has_server_permissions and server_only`
# [p]convocopy
Copy the conversation to another channel, thread, or forum<br/>
 - Usage: `[p]convocopy <channel>`
 - Checks: `bot_has_server_permissions and server_only`
# [p]convoprompt
Set a system prompt for this conversation!<br/>

This allows customization of assistant behavior on a per channel basis!<br/>

Check out [This Guide](https://platform.openai.com/docs/guides/prompt-engineering) for prompting help.<br/>
 - Usage: `[p]convoprompt [prompt]`
 - Checks: `server_only`
# [p]convoshow
View the current transcript of a conversation<br/>

This is mainly here for moderation purposes<br/>
 - Usage: `[p]convoshow [user=None] [channel=operator.attrgetter('channel')]`
 - Restricted to: `GUILD_OWNER`
 - Aliases: `showconvo`
 - Checks: `server_only`
# [p]query
Fetch related embeddings according to the current topn setting along with their scores<br/>

You can use this to fine-tune the minimum relatedness for your assistant<br/>
 - Usage: `[p]query <query>`
# [p]assistant
Setup the assistant<br/>

You will need an **[api key](https://platform.openai.com/account/api-keys)** from OpenAI to use ChatGPT and their other models.<br/>
 - Usage: `[p]assistant`
 - Restricted to: `ADMIN`
 - Aliases: `assist`
 - Checks: `server_only`
## [p]assistant embedmethod
Cycle between embedding methods<br/>

**Dynamic** embeddings mean that the embeddings pulled are dynamically appended to the initial prompt for each individual question.<br/>
When each time the user asks a question, the previous embedding is replaced with embeddings pulled from the current question, this reduces token usage significantly<br/>

**Static** embeddings are applied in front of each user message and get stored with the conversation instead of being replaced with each question.<br/>

**Hybrid** embeddings are a combination, with the first embedding being stored in the conversation and the rest being dynamic, this saves a bit on token usage.<br/>

**User** embeddings are injected into the beginning of the prompt as the first user message.<br/>

Dynamic embeddings are helpful for Q&A, but not so much for chat when you need to retain the context pulled from the embeddings. The hybrid method is a good middle ground<br/>
 - Usage: `[p]assistant embedmethod`
## [p]assistant embedmodel
Set the OpenAI Embedding model to use<br/>
 - Usage: `[p]assistant embedmodel [model=None]`
## [p]assistant openaikey
Set your OpenAI key<br/>
 - Usage: `[p]assistant openaikey`
 - Aliases: `key`
## [p]assistant questionmark
Toggle whether questions need to end with **__?__**<br/>
 - Usage: `[p]assistant questionmark`
## [p]assistant minlength
set min character length for questions<br/>

Set to 0 to respond to anything<br/>
 - Usage: `[p]assistant minlength <min_question_length>`
## [p]assistant frequency
Set the frequency penalty for the model (-2.0 to 2.0)<br/>
- Defaults is 0<br/>

Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.<br/>
 - Usage: `[p]assistant frequency <frequency_penalty>`
## [p]assistant exportcsv
Export embeddings to a .csv file<br/>

**Note:** csv exports do not include the embedding values<br/>
 - Usage: `[p]assistant exportcsv`
## [p]assistant collab
Toggle collaborative conversations<br/>

Multiple people speaking in a channel will be treated as a single conversation.<br/>
 - Usage: `[p]assistant collab`
## [p]assistant usage
View the token usage stats for this server<br/>
 - Usage: `[p]assistant usage`
## [p]assistant relatedness
Set the minimum relatedness an embedding must be to include with the prompt<br/>

Relatedness threshold between 0 and 1 to include in embeddings during chat<br/>

Questions are converted to embeddings and compared against stored embeddings to pull the most relevant, this is the score that is derived from that comparison<br/>

**Hint**: The closer to 1 you get, the more deterministic and accurate the results may be, just don't be *too* strict or there wont be any results.<br/>
 - Usage: `[p]assistant relatedness <mimimum_relatedness>`
## [p]assistant sysoverride
Toggle allowing per-conversation system prompt overriding<br/>
 - Usage: `[p]assistant sysoverride`
## [p]assistant regexblacklist
Remove certain words/phrases in the bot's responses<br/>
 - Usage: `[p]assistant regexblacklist <regex>`
## [p]assistant toggledraw
Toggle the draw command on or off<br/>
 - Usage: `[p]assistant toggledraw`
 - Aliases: `drawtoggle`
## [p]assistant presence
Set the presence penalty for the model (-2.0 to 2.0)<br/>
- Defaults is 0<br/>

Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics.<br/>
 - Usage: `[p]assistant presence <presence_penalty>`
## [p]assistant importcsv
Import embeddings to use with the assistant<br/>

Args:<br/>
    overwrite (bool): overwrite embeddings with existing entry names<br/>

This will read excel files too<br/>
 - Usage: `[p]assistant importcsv <overwrite>`
## [p]assistant wipecog
Wipe all settings and data for entire cog<br/>
 - Usage: `[p]assistant wipecog <confirm>`
 - Restricted to: `BOT_OWNER`
## [p]assistant maxrecursion
Set the maximum function calls allowed in a row<br/>

This sets how many times the model can call functions in a row<br/>

Only the following models can call functions at the moment<br/>
- gpt-4o-mini<br/>
- gpt-4o<br/>
- ect..<br/>
 - Usage: `[p]assistant maxrecursion <recursion>`
## [p]assistant exportjson
Export embeddings to a json file<br/>
 - Usage: `[p]assistant exportjson`
## [p]assistant resetglobalembeddings
Wipe saved embeddings for all servers<br/>

This will delete any and all saved embedding training data for the assistant.<br/>
 - Usage: `[p]assistant resetglobalembeddings <yes_or_no>`
 - Restricted to: `BOT_OWNER`
## [p]assistant braveapikey
Enables use of the `search_internet` function<br/>

Get your API key **[Here](https://brave.com/search/api/)**<br/>
 - Usage: `[p]assistant braveapikey`
 - Restricted to: `BOT_OWNER`
 - Aliases: `brave`
## [p]assistant system
Set the system prompt for GPT to use<br/>

Check out [This Guide](https://platform.openai.com/docs/guides/prompt-engineering) for prompting help.<br/>

**Placeholders**<br/>
- **botname**: [botname]<br/>
- **timestamp**: discord timestamp<br/>
- **day**: Mon-Sun<br/>
- **date**: MM-DD-YYYY<br/>
- **time**: HH:MM AM/PM<br/>
- **timetz**: HH:MM AM/PM Timezone<br/>
- **members**: server member count<br/>
- **username**: user's name<br/>
- **displayname**: user's display name<br/>
- **roles**: the names of the user's roles<br/>
- **rolementions**: the mentions of the user's roles<br/>
- **avatar**: the user's avatar url<br/>
- **owner**: the owner of the server<br/>
- **servercreated**: the create date/time of the server<br/>
- **server**: the name of the server<br/>
- **py**: python version<br/>
- **dpy**: discord.py version<br/>
- **red**: red version<br/>
- **cogs**: list of currently loaded cogs<br/>
- **channelname**: name of the channel the conversation is taking place in<br/>
- **channelmention**: current channel mention<br/>
- **topic**: topic of current channel (if not forum or thread)<br/>
- **banktype**: whether the bank is global or not<br/>
- **currency**: currency name<br/>
- **bank**: bank name<br/>
- **balance**: the user's current balance<br/>
 - Usage: `[p]assistant system [system_prompt]`
 - Aliases: `sys`
## [p]assistant resolution
Switch vision resolution between high and low for relevant GPT-4-Turbo models<br/>
 - Usage: `[p]assistant resolution`
## [p]assistant maxretention
Set the max messages for a conversation<br/>

Conversation retention is cached and gets reset when the bot restarts or the cog reloads.<br/>

Regardless of this number, the initial prompt and internal system message are always included,<br/>
this only applies to any conversation between the user and bot after that.<br/>

Set to 0 to disable conversation retention<br/>

**Note:** *actual message count may exceed the max retention during an API call*<br/>
 - Usage: `[p]assistant maxretention <max_retention>`
## [p]assistant seed
Make the model more deterministic by setting a seed for the model.<br/>
- Default is None<br/>

If specified, the system will make a best effort to sample deterministically, such that repeated requests with the same seed and parameters should return the same result.<br/>
 - Usage: `[p]assistant seed [seed=None]`
## [p]assistant regexfailblock
Toggle whether failed regex blocks the assistant's reply<br/>

Some regexes can cause [catastrophically backtracking](https://www.rexegg.com/regex-explosive-quantifiers.html)<br/>
The bot can safely handle if this happens and will either continue on, or block the response.<br/>
 - Usage: `[p]assistant regexfailblock`
## [p]assistant timezone
Set the timezone used for prompt placeholders<br/>
 - Usage: `[p]assistant timezone <timezone>`
## [p]assistant listentobots
Toggle whether the assistant listens to other bots<br/>

**NOT RECOMMENDED FOR PUBLIC BOTS!**<br/>
 - Usage: `[p]assistant listentobots`
 - Restricted to: `BOT_OWNER`
 - Aliases: `botlisten and ignorebots`
## [p]assistant view
View current settings<br/>

To send in current channel, use `[p]assistant view false`<br/>
 - Usage: `[p]assistant view [private=False]`
 - Aliases: `v`
## [p]assistant importjson
Import embeddings to use with the assistant<br/>

Args:<br/>
    overwrite (bool): overwrite embeddings with existing entry names<br/>
 - Usage: `[p]assistant importjson <overwrite>`
## [p]assistant backupcog
Take a backup of the cog<br/>

- This does not backup conversation data<br/>
 - Usage: `[p]assistant backupcog`
 - Restricted to: `BOT_OWNER`
## [p]assistant channel
Set the channel for the assistant<br/>
 - Usage: `[p]assistant channel [channel=None]`
## [p]assistant resetembeddings
Wipe saved embeddings for the assistant<br/>

This will delete any and all saved embedding training data for the assistant.<br/>
 - Usage: `[p]assistant resetembeddings <yes_or_no>`
## [p]assistant importexcel
Import embeddings from an .xlsx file<br/>

Args:<br/>
    overwrite (bool): overwrite embeddings with existing entry names<br/>
 - Usage: `[p]assistant importexcel <overwrite>`
## [p]assistant maxtime
Set the conversation expiration time<br/>

Regardless of this number, the initial prompt and internal system message are always included,<br/>
this only applies to any conversation between the user and bot after that.<br/>

Set to 0 to store conversations indefinitely or until the bot restarts or cog is reloaded<br/>
 - Usage: `[p]assistant maxtime <retention_seconds>`
## [p]assistant channelprompt
Set a channel specific system prompt<br/>
 - Usage: `[p]assistant channelprompt [channel=operator.attrgetter('channel')] [system_prompt]`
## [p]assistant maxtokens
Set maximum tokens a convo can consume<br/>

Set to 0 for dynamic token usage<br/>

**Tips**<br/>
- Max tokens are a soft cap, sometimes messages can be a little over<br/>
- If you set max tokens too high the cog will auto-adjust to 100 less than the models natural cap<br/>
- Ideally set max to 500 less than that models maximum, to allow adequate responses<br/>

Using more than the model can handle will raise exceptions.<br/>
 - Usage: `[p]assistant maxtokens <max_tokens>`
## [p]assistant tutor
Add/Remove items from the tutor list.<br/>

If using OpenAI's function calling and talking to a tutor, the AI is able to create its own embeddings to remember later<br/>

`role_or_member` can be a member or role<br/>
 - Usage: `[p]assistant tutor <role_or_member>`
 - Aliases: `tutors`
## [p]assistant restorecog
Restore the cog from a backup<br/>
 - Usage: `[p]assistant restorecog`
 - Restricted to: `BOT_OWNER`
## [p]assistant prompt
Set the initial prompt for GPT to use<br/>

Check out [This Guide](https://platform.openai.com/docs/guides/prompt-engineering) for prompting help.<br/>

**Placeholders**<br/>
- **botname**: [botname]<br/>
- **timestamp**: discord timestamp<br/>
- **day**: Mon-Sun<br/>
- **date**: MM-DD-YYYY<br/>
- **time**: HH:MM AM/PM<br/>
- **timetz**: HH:MM AM/PM Timezone<br/>
- **members**: server member count<br/>
- **username**: user's name<br/>
- **displayname**: user's display name<br/>
- **roles**: the names of the user's roles<br/>
- **rolementions**: the mentions of the user's roles<br/>
- **avatar**: the user's avatar url<br/>
- **owner**: the owner of the server<br/>
- **servercreated**: the create date/time of the server<br/>
- **server**: the name of the server<br/>
- **py**: python version<br/>
- **dpy**: discord.py version<br/>
- **red**: red version<br/>
- **cogs**: list of currently loaded cogs<br/>
- **channelname**: name of the channel the conversation is taking place in<br/>
- **channelmention**: current channel mention<br/>
- **topic**: topic of current channel (if not forum or thread)<br/>
- **banktype**: whether the bank is global or not<br/>
- **currency**: currency name<br/>
- **bank**: bank name<br/>
- **balance**: the user's current balance<br/>
 - Usage: `[p]assistant prompt [prompt]`
 - Aliases: `pre`
## [p]assistant exportexcel
Export embeddings to an .xlsx file<br/>

**Note:** csv exports do not include the embedding values<br/>
 - Usage: `[p]assistant exportexcel`
## [p]assistant mentionrespond
Toggle whether the bot responds to mentions in any channel<br/>
 - Usage: `[p]assistant mentionrespond`
## [p]assistant resetconversations
Wipe saved conversations for the assistant in this server<br/>

This will delete any and all saved conversations for the assistant.<br/>
 - Usage: `[p]assistant resetconversations <yes_or_no>`
## [p]assistant resetglobalconversations
Wipe saved conversations for the assistant in all servers<br/>

This will delete any and all saved conversations for the assistant.<br/>
 - Usage: `[p]assistant resetglobalconversations <yes_or_no>`
 - Restricted to: `BOT_OWNER`
## [p]assistant blacklist
Add/Remove items from the blacklist<br/>

`channel_role_member` can be a member, role, channel, or category channel<br/>
 - Usage: `[p]assistant blacklist <channel_role_member>`
## [p]assistant override
Override settings for specific roles<br/>

**NOTE**<br/>
If a user has two roles with override settings, override associated with the higher role will be used.<br/>
 - Usage: `[p]assistant override`
### [p]assistant override maxtime
Assign a max retention time override to a role<br/>

*Specify same role and time to remove the override*<br/>
 - Usage: `[p]assistant override maxtime <retention_seconds> <role>`
### [p]assistant override maxretention
Assign a max message retention override to a role<br/>

*Specify same role and retention amount to remove the override*<br/>
 - Usage: `[p]assistant override maxretention <max_retention> <role>`
### [p]assistant override model
Assign a role to use a model<br/>

*Specify same role and model to remove the override*<br/>
 - Usage: `[p]assistant override model <model> <role>`
### [p]assistant override maxresponsetokens
Assign a max response token override to a role<br/>

Set to 0 for response tokens to be dynamic<br/>

*Specify same role and token count to remove the override*<br/>
 - Usage: `[p]assistant override maxresponsetokens <max_tokens> <role>`
### [p]assistant override maxtokens
Assign a max token override to a role<br/>

*Specify same role and token count to remove the override*<br/>
 - Usage: `[p]assistant override maxtokens <max_tokens> <role>`
## [p]assistant resetusage
Reset the token usage stats for this server<br/>
 - Usage: `[p]assistant resetusage`
## [p]assistant temperature
Set the temperature for the model (0.0 - 2.0)<br/>
- Defaults is 1<br/>

Closer to 0 is more concise and accurate while closer to 2 is more imaginative<br/>
 - Usage: `[p]assistant temperature <temperature>`
## [p]assistant questionmode
Toggle question mode<br/>

If question mode is on, embeddings will only be sourced during the first message of a conversation and messages that end in **?**<br/>
 - Usage: `[p]assistant questionmode`
## [p]assistant maxresponsetokens
Set the max response tokens the model can respond with<br/>

Set to 0 for response tokens to be dynamic<br/>
 - Usage: `[p]assistant maxresponsetokens <max_tokens>`
## [p]assistant channelpromptshow
Show the channel specific system prompt<br/>
 - Usage: `[p]assistant channelpromptshow [channel=operator.attrgetter('channel')]`
## [p]assistant toggle
Toggle the assistant on or off<br/>
 - Usage: `[p]assistant toggle`
## [p]assistant refreshembeds
Refresh embedding weights<br/>

*This command can be used when changing the embedding model*<br/>

Embeddings that were created using OpenAI cannot be use with the self-hosted model and vice versa<br/>
 - Usage: `[p]assistant refreshembeds`
 - Aliases: `refreshembeddings, syncembeds, and syncembeddings`
## [p]assistant functioncalls
Toggle whether GPT can call functions<br/>
 - Usage: `[p]assistant functioncalls`
 - Aliases: `usefunctions`
## [p]assistant model
Set the OpenAI model to use<br/>
 - Usage: `[p]assistant model [model=None]`
## [p]assistant persist
Toggle persistent conversations<br/>
 - Usage: `[p]assistant persist`
 - Restricted to: `BOT_OWNER`
## [p]assistant mention
Toggle whether to ping the user on replies<br/>
 - Usage: `[p]assistant mention`
## [p]assistant topn
Set the embedding inclusion amout<br/>

Top N is the amount of embeddings to include with the initial prompt<br/>
 - Usage: `[p]assistant topn <top_n>`
# [p]embeddings (Hybrid Command)
Manage embeddings for training<br/>

Embeddings are used to optimize training of the assistant and minimize token usage.<br/>

By using this the bot can store vast amounts of contextual information without going over the token limit.<br/>

**Note**<br/>
You can enter a search query with this command to bring up the menu and go directly to that embedding selection.<br/>
 - Usage: `[p]embeddings [query]`
 - Slash Usage: `/embeddings [query]`
 - Restricted to: `ADMIN`
 - Aliases: `emenu`
 - Checks: `server_only`
# [p]customfunctions (Hybrid Command)
Add custom function calls for Assistant to use<br/>

**READ**<br/>
- [Function Call Docs](https://platform.openai.com/docs/guides/gpt/function-calling)<br/>
- [OpenAI Cookbook](https://github.com/openai/openai-cookbook/blob/main/examples/How_to_call_functions_with_chat_models.ipynb)<br/>
- [JSON Schema Reference](https://json-schema.org/understanding-json-schema/)<br/>

The following objects are passed by default as keyword arguments.<br/>
- **user**: the user currently chatting with the bot (discord.Member)<br/>
- **channel**: channel the user is chatting in (TextChannel|Thread|ForumChannel)<br/>
- **server**: current server (discord.Guild)<br/>
- **bot**: the bot object (Red)<br/>
- **conf**: the config model for Assistant (GuildSettings)<br/>
- All functions **MUST** include `*args, **kwargs` in the params and return a string<br/>
```python
# Can be either sync or async
async def func(*args, **kwargs) -> str:
```
Only bot owner can manage this, server owners can see descriptions but not code<br/>
 - Usage: `[p]customfunctions [function_name=None]`
 - Slash Usage: `/customfunctions [function_name=None]`
 - Aliases: `customfunction and customfunc`
 - Checks: `server_only`
