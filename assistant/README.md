# Assistant Cog

## Overview
The Assistant cog allows you to set up and configure an AI assistant or chat bot for your server using OpenAI's ChatGPT language models. It offers a range of features including configurable prompt injection, dynamic embeddings for external knowledge integration, custom function calling to extend its capabilities, and per-server configuration options.

## Author & Version
- **Author:** Vertyco
- **Version:** 6.12.24

## Features
- Converse with multiple GPT models
- Configurable prompt injection
- Dynamic embeddings for associating external knowledge
- Custom function calling for extending functionality
- Per-server configuration and API key management
- Conversation logging and persistence
- Integration with other cogs for expanded capabilities

## Requirements
- aiocache
- json5
- msgpack
- numpy
- openai>=1.40.0
- pandas
- pydantic
- pytz
- sentry_sdk
- tenacity
- tiktoken
- ujson
- google-auth

## Installation
Thank you for installing Assistant! type `[p]assistant` to see all commands. and `[p]chathelp` for tips on how to interact.
You will need an [OpenAI API key](https://platform.openai.com/account/api-keys) **per server** via `[p]assistant openaikey`.

**Warning**
It is not recommended to run this cog on a public bot or on a server with limited resources!

**Note**
This cog allows other 3rd party cogs to register functions with it, extending functionality. Be aware of what functions other cogs are registering with `[p]customfunc`

DOCUMENTATION: https://github.com/vertyco/vrt-cogs/blob/main/assistant/README.md

## Setup
Setting up the Assistant cog involves a few key steps to get your AI assistant operational.

### API Keys
**OpenAI API Key (Required):**
The cog requires an OpenAI API key to function, as it uses OpenAI's language models. You can obtain an API key from [OpenAI's website](https://platform.openai.com/account/api-keys).
Once you have your key, set it for your server using the following command:
`[p]assistant openaikey <your_openai_api_key>`

**Google AI Studio API Key (Optional):**
If you plan to use Google's Gemini models via AI Studio, you'll need a Google AI Studio API key.
Set it using:
`[p]assistant setgaistudiokey <your_google_ai_studio_key>`

**Google Cloud Project (Optional for Gemini via Vertex AI):**
Alternatively, for using Gemini models through Google Cloud's Vertex AI, you can authenticate using Application Default Credentials (ADC). This typically involves setting up a Google Cloud Project and authenticating the environment where your bot is running.
You can initiate the OAuth process for ADC with:
`[p]assistant gauth`

### Basic Configuration
Here are the essential steps to configure your assistant:

1.  **Set a Primary Model:** Choose the primary language model the assistant will use.
    `[p]assistant model <model_name>`
    (e.g., `gpt-4o`, `gpt-3.5-turbo`, `gemini-1.5-pro-latest`)

2.  **Designate an Assistant Channel:** Specify a channel where users can interact with the assistant without needing to use a prefix for each message. The bot will listen for any message in this channel.
    `[p]assistant channel <#channel_mention_or_id>`

These are the basic settings to get you started. You can explore many other customization options by viewing the current server settings with `[p]assistant view` and see all available commands with `[p]help assistant`.

## Commands
This section details the available commands for interacting with and configuring the Assistant cog.

### Main User Commands
These commands are for general interaction with the AI.

*   **`[p]chat <message>`** (Aliases: `ask`)
    *   The primary command to interact with the AI.
    *   `--outputfile <filename.txt>`: Sends the AI's response as a text file.
    *   `--extract`: Attempts to extract and resend code blocks if the response is cut short.
    *   `--last`: Edits your last message to include the AI's response (useful for continuing a thought).
*   **`[p]convostats [user]`**
    *   Shows conversation message count and token usage for yourself or an optional user.
*   **`[p]clearconvo`** (Alias: `convoclear`)
    *   Resets your current conversation with the AI.
*   **`[p]convopop`**
    *   Removes the last pair of messages (user's and AI's) from your conversation history.
*   **`[p]convocopy <#target-channel>`**
    *   Copies your current conversation to the specified channel.
*   **`[p]convoprompt [prompt text]`**
    *   Sets a temporary system prompt for your current conversation. If no prompt is provided, it clears the current conversation-specific prompt.
*   **`[p]draw <prompt> [size] [quality] [style]`** (App Command)
    *   Generates an image using DALL-E based on the provided prompt. Options for size, quality, and style may vary by model.
*   **`[p]tldr [timeframe] [channel] [user] [include_bot_messages]`** (App Command)
    *   Summarizes messages in a channel. You can specify a timeframe (e.g., `1h`, `30m`, `7d`), a specific channel, a user, and whether to include bot messages.
*   **`[p]query <search_query>`**
    *   Tests embedding responses by searching stored embeddings for relevant information without starting a full chat.
*   **`[p]chathelp`**
    *   Shows detailed help for chat usage, arguments, and tips for interacting with the AI.

### Administrative & Management Commands
These commands are used for configuring the cog and managing its features.

*   **`[p]assistant`**: The main command group for all assistant configurations. Most settings are managed via its subcommands.
*   **`[p]embeddings [query]`**: Hybrid command to open the embedding management menu. Allows creating, deleting, and searching embeddings. If a `query` is provided, it searches for that specific embedding. (Details in "Embeddings" section).
*   **`[p]customfunctions [function_name]`**: Hybrid command to open the custom function management menu. Allows adding, editing, and viewing custom Python functions the AI can call. If a `function_name` is provided, it jumps to that function. (Details in "Custom Functions" section).

### `[p]assistant` Subcommands
All settings for the Assistant cog are managed under this command group.

#### API Keys & Core Setup
*   **`[p]assistant openaikey`** (Alias: `key`): Set your OpenAI API key interactively. This key is used for accessing OpenAI models.
*   **`[p]assistant gauth [project_id]`** (Aliases: `googleauth`, `googleprojectid`) (Owner/Admin): Configure Google Cloud Project ID for Gemini models using ADC. If no ID, shows current. Use `none` to clear.
*   **`[p]assistant setgaistudiokey <key>`** (Owner): Set the Google AI Studio API key globally for Gemini models. Use `clear` or `none` to remove.
*   **`[p]assistant braveapikey`** (Alias: `brave`) (Owner): Set the Brave Search API key for the `search_internet` function.
*   **`[p]assistant toggle`**: Toggle the assistant on or off for the server.
*   **`[p]assistant view [private_true_false]`** (Alias: `v`): View current server settings for the assistant. Set `private` to `True` to receive the settings in a DM (if owner).
*   **`[p]assistant usage`**: View the token usage statistics for this server, broken down by model.
*   **`[p]assistant resetusage`**: Reset the token usage statistics for this server.
*   **`[p]assistant endpointoverride [endpoint_url]`** (Owner): Override the default OpenAI API endpoint. Use with caution. No URL removes override.

#### Model Configuration
*   **`[p]assistant model <model_name>`**: Set the primary OpenAI/compatible model to use (e.g., `gpt-4o`, `gpt-3.5-turbo`).
*   **`[p]assistant embedmodel <model_name>`**: Set the OpenAI Embedding model to use (e.g., `text-embedding-ada-002`, `text-embedding-3-small`).
*   **`[p]assistant resolution`**: Switch vision resolution (low/high/auto) for vision-capable models.
*   **`[p]assistant reasoning`**: Switch reasoning effort (low/medium/high) for `o1` models.
*   **`[p]assistant temperature <value>`**: Set the model's temperature (0.0-2.0). Higher values are more creative, lower are more deterministic.
*   **`[p]assistant frequency <value>`**: Set the frequency penalty (-2.0 to 2.0). Positive values reduce repetition.
*   **`[p]assistant presence <value>`**: Set the presence penalty (-2.0 to 2.0). Positive values encourage new topics.
*   **`[p]assistant seed [number]`**: Set a seed for more deterministic model outputs. No number removes the seed.
*   **`[p]assistant maxtokens <count>`**: Set the maximum token limit for a single conversation context (request + response). 0 for dynamic.
*   **`[p]assistant maxresponsetokens <count>`**: Set the maximum tokens the model can generate in a response. 0 for dynamic.

#### Prompt & System Message Configuration
*   **`[p]assistant prompt [prompt_text_or_attach_file]`**: Set the server-wide initial prompt (prepended to conversations). Attach a .txt file or provide text. No argument removes.
*   **`[p]assistant system [prompt_text_or_attach_file]`**: Set the server-wide system prompt. Attach a .txt file or provide text. No argument removes.
*   **`[p]assistant channelprompt [channel] [system_prompt_or_attach_file]`**: Set a system prompt specific to a channel, overriding the server-wide one. No prompt removes.
*   **`[p]assistant channelpromptshow [channel]`**: Display the system prompt for a specific channel.
*   **`[p]assistant sysoverride`**: Toggle whether users can set their own per-conversation system prompts using `[p]convoprompt`.
*   **`[p]assistant timezone <timezone_name>`**: Set the timezone (e.g., `America/New_York`) for time-related placeholders in prompts.

#### Channel & Interaction Management
*   **`[p]assistant channel [#channel/ID/None]`**: Designate a specific channel for prefix-less assistant interaction. `None` removes.
*   **`[p]assistant mention`**: Toggle whether the bot pings the user on replies.
*   **`[p]assistant mentionrespond`**: Toggle whether the bot responds to mentions in any channel (outside the designated assistant channel).
*   **`[p]assistant questionmark`**: Toggle if messages must end with a `?` to be treated as questions (affects embedding search).
*   **`[p]assistant questionmode`**: Toggle question mode. If on, embeddings are only sourced for first messages or those ending in `?`.
*   **`[p]assistant collab`**: Toggle collaborative conversations. If enabled, multiple users in the assistant channel share one conversation.
*   **`[p]assistant minlength <character_count>`**: Set the minimum character length for messages to be processed. 0 to disable.
*   **`[p]assistant toggledraw`** (Alias: `drawtoggle`): Enable or disable the `[p]draw` command for the server.
*   **`[p]assistant maxretention <message_count>`**: Set the maximum number of messages to retain in a conversation's history. 0 for no limit (memory permitting).
*   **`[p]assistant maxtime <seconds>`**: Set the maximum time (in seconds) a conversation remains active. 0 for indefinite (until cog reload).

#### Embeddings Management
*   **`[p]assistant topn <count>`**: Set the number of top matching embeddings (0-10) to include with prompts.
*   **`[p]assistant relatedness <score>`**: Set the minimum relatedness score (0.0-1.0) for an embedding to be included.
*   **`[p]assistant embedmethod`**: Cycle through embedding methods: `dynamic`, `static`, `hybrid`, `user`.
*   **`[p]assistant refreshembeds`** (Aliases: `refreshembeddings`, `syncembeds`, `syncembeddings`): Resync/recalculate embeddings if the embedding model changed or if there are mixed types.
*   **`[p]assistant resetembeddings <yes_or_no>`**: Wipe all saved embeddings for the server. Requires confirmation.
*   **`[p]assistant importcsv <overwrite_true_false>`**: Import embeddings from attached .csv or .xlsx files. Columns: `name`, `text`.
*   **`[p]assistant importjson <overwrite_true_false>`**: Import embeddings from an attached .json file.
*   **`[p]assistant importexcel <overwrite_true_false>`**: Import embeddings from an .xlsx file (supports `name`, `text`, `created`, `ai_created` columns).
*   **`[p]assistant exportcsv`**: Export server embeddings to a .csv file.
*   **`[p]assistant exportjson`**: Export server embeddings to a .json file (includes embedding vectors).
*   **`[p]assistant exportexcel`**: Export server embeddings to an .xlsx file.

#### Function Call Management
*   **`[p]assistant functioncalls`** (Alias: `usefunctions`): Toggle whether the AI can use custom or built-in functions.
*   **`[p]assistant maxrecursion <depth>`**: Set the maximum number of consecutive function calls the AI can make before responding.

#### User & Role Management
*   **`[p]assistant blacklist <user/role/channel>`**: Add or remove a user, role, or channel from the blacklist (assistant will ignore them).
*   **`[p]assistant tutor <user/role>`**: Add or remove a user or role from the "tutors" list. Tutors can have their interactions automatically converted to embeddings by the AI if `create_memory` function is enabled.
*   **`[p]assistant override model <model_name> <role>`**: Assign a specific model to be used by users with a certain role.
*   **`[p]assistant override maxtokens <count> <role>`**: Assign a specific max token limit for a role.
*   **`[p]assistant override maxresponsetokens <count> <role>`**: Assign a specific max response token limit for a role.
*   **`[p]assistant override maxretention <count> <role>`**: Assign a specific max message retention for a role.
*   **`[p]assistant override maxtime <seconds> <role>`**: Assign a specific max conversation time for a role.

#### Channel Context Configuration (`[p]assistant channelcontext ...`)
This group configures the assistant's ability to use recent messages from the current channel as context.
*   **`[p]assistant channelcontext enable <True/False>`** (Alias: `toggle`): Enable or disable this feature.
*   **`[p]assistant channelcontext maxmessages <count>`**: Set how many recent messages (0-50) to include.
*   **`[p]assistant channelcontext includebot <True/False>`** (Alias: `includebots`): Choose whether to include messages from other bots in the context.
*   **`[p]assistant channelcontext showsettings`** (Aliases: `view`, `settings`): Display current channel context settings.

#### Auto-Answer Feature
This feature allows the assistant to automatically answer questions outside its designated channel if an embedding is found or a question is detected.
*   **`[p]assistant autoanswer`**: Toggle the auto-answer feature on or off.
*   **`[p]assistant autoanswerthreshold <score>`**: Set the similarity score (0.0-1.0) required for an embedding to trigger an auto-answer.
*   **`[p]assistant autoanswerignore <#channel/ID>`**: Make the auto-answer feature ignore a specific channel.
*   **`[p]assistant autoanswermodel <model_name>`**: Set the model used for generating auto-answers.

#### Regex & Content Control
*   **`[p]assistant regexblacklist <regex_pattern>`**: Add or remove a regex pattern from the blacklist. Bot responses matching the pattern will have matching text removed.
*   **`[p]assistant regexfailblock`**: Toggle whether a reply is blocked if a regex operation fails (e.g., due to complexity).

#### Data Management (Guild Specific)
*   **`[p]assistant resetconversations <yes_or_no>`**: Wipe all saved conversation history for the assistant in the current server. Requires confirmation.

#### Owner Commands (Bot Owner Only)
These commands are for global bot management and can only be used by the bot owner.
*   **`[p]assistant wipecog <confirm_bool>`**: Wipe all settings and data for the entire Assistant cog across all servers. **Use with extreme caution.**
*   **`[p]assistant backupcog`**: Create a backup of the cog's global settings and function definitions (does not include server-specific conversation data or embeddings).
*   **`[p]assistant restorecog`**: Restore the cog's global settings from an attached backup file.
*   **`[p]assistant resetglobalconversations <yes_or_no>`**: Wipe all saved conversation history for all servers. Requires confirmation.
*   **`[p]assistant persist`**: Toggle persistent conversations globally. If enabled, conversations are saved to disk; otherwise, they are in memory and lost on reload/restart.
*   **`[p]assistant resetglobalembeddings <yes_or_no>`**: Wipe all saved embeddings across all servers. Requires confirmation.
*   **`[p]assistant listentobots`** (Aliases: `botlisten`, `ignorebots`): Toggle whether the assistant listens to messages from other bots globally. **Not recommended for public bots.**

## Key Functionalities (In-depth)

### Conversations
Interacting with the Assistant is primarily done through the `[p]chat <your message>` command (or its alias `[p]ask`). Each user generally has their own conversation session with the AI.

*   **Scope:** By default, conversations are per-user, per-channel. This means your conversation in #general is separate from your conversation in #off-topic, and also separate from another user's conversation in #general.
    *   **Collaborative Conversations:** You can change this behavior using `[p]assistant collab`. When enabled, all users interacting with the assistant in the designated assistant channel (or any channel if no specific assistant channel is set) will contribute to a single, shared conversation. This is useful for group brainstorming or shared AI interaction.
*   **History Management:** The AI remembers a certain amount of past messages in the current conversation to maintain context.
    *   `[p]assistant maxretention <message_count>`: Sets the maximum number of user/AI message pairs retained in history.
    *   `[p]assistant maxtime <seconds>`: Sets how long a conversation stays active and its history is kept.
    *   The bot owner can also enable `[p]assistant persist` for conversations to be stored in a file, making them survive bot restarts. Otherwise, they are in memory.
*   **Managing Your Conversation:**
    *   `[p]clearconvo`: Wipes your current conversation history with the AI, starting fresh.
    *   `[p]convopop`: Removes the most recent user message and AI response from your history. Useful if a turn went wrong.
    *   `[p]convocopy <#target-channel>`: Copies your current conversation (including history) to a new channel, useful for sharing or archiving.
    *   `[p]convostats [user]`: Shows your (or another specified user's) current conversation length and token usage.

### Embeddings (Long-Term Memory)
Embeddings provide the Assistant with a form of long-term memory, allowing it to recall specific information or context beyond the immediate conversation history. They are numerical representations of text that capture semantic meaning.

*   **What are Embeddings?** Think of embeddings as snippets of knowledge. When you ask the Assistant a question, it can search its stored embeddings for relevant snippets to inform its answer. This is more efficient and often more accurate than trying to stuff all information into the prompt.
*   **Creating Embeddings:**
    *   **Manual Creation (Tutors):** Users or roles designated as "tutors" (via `[p]assistant tutor <user/role>`) can create embeddings from messages. Reacting to a message with the 🧠 (brain) emoji will trigger the process of converting that message's content into an embedding.
    *   **AI-Generated (via `create_memory` function):** If the `create_memory` custom function is enabled and a tutor is interacting with the AI, the AI itself can decide to create an embedding from parts of the conversation it deems important for future recall.
    *   **Importing:** You can bulk-import embeddings using `[p]assistant importcsv`, `[p]assistant importjson`, or `[p]assistant importexcel`.
*   **How Embeddings are Used:**
    *   When you send a message, the Assistant can convert your query into an embedding and compare it against its database of stored embeddings.
    *   `[p]assistant topn <count>`: This setting determines how many of the most similar embeddings are retrieved and added to the context for the AI.
    *   `[p]assistant relatedness <score>`: This sets a minimum similarity score (between 0.0 and 1.0) for an embedding to be considered relevant enough to be included.
    *   The chosen embedding method (`[p]assistant embedmethod`) also influences how these are presented to the model.
*   **Managing Embeddings:**
    *   The primary tool for managing embeddings is the `[p]embeddings` command. This opens an interactive menu where you can:
        *   Add new embeddings manually.
        *   View existing embeddings.
        *   Edit the text or name of embeddings.
        *   Delete embeddings.
        *   Search for embeddings by name or content.
    *   You can also export all embeddings for a server using `[p]assistant exportcsv`, `[p]assistant exportjson`, or `[p]assistant exportexcel`.
    *   `[p]assistant resetembeddings <yes_or_no>` allows wiping all embeddings for the server.
    *   `[p]assistant refreshembeds` can be used to re-calculate embedding vectors if you change the embedding model (`[p]assistant embedmodel`).

### Custom Functions (Extending Capabilities)
Custom functions allow the AI to interact with other bot commands, external APIs, or run predefined Python code to fetch information or perform actions. This greatly extends the Assistant's capabilities beyond simple text generation.

*   **What is Function Calling?** The AI model can be told about available "tools" (functions). If it determines that using one of these tools would help answer a user's query, it can formulate a "function call" request. The cog then executes the corresponding Python code and returns the result to the AI, which uses this information to formulate its final response.
*   **Registering Functions:**
    *   **Bot Owner:** The bot owner can define and manage custom Python functions directly within the cog using the `[p]customfunctions` command menu. This requires writing Python code and defining a JSON schema that describes the function's purpose, parameters, and expected input. **The bot owner is responsible for the safety and behavior of this custom code.**
    *   **Third-Party Cogs:** Other cogs can also register their functions with the Assistant, allowing for a modular and extensible ecosystem. Server administrators should be aware of what functions are being registered by other cogs (viewable in `[p]customfunctions` and `[p]assistant view`).
*   **Managing Custom Functions:**
    *   `[p]customfunctions [function_name]`: Opens an interactive menu to view, add, edit, delete, enable, or disable custom functions. Bot owners can see and edit the code; server admins can typically only see names, descriptions, and enabled status.
    *   Function status (enabled/disabled) is managed within this menu. There isn't a separate `disabled_functions` setting; it's per-function.
*   **Permissions:** Functions can have permission levels associated with them (e.g., owner-only, admin-only, general use), restricting who can trigger their execution through the AI. This is typically configured when the function is defined.
*   **Global Controls:**
    *   `[p]assistant functioncalls` (Alias: `usefunctions`): Toggles the entire function calling feature on or off for the server.
    *   `[p]assistant maxrecursion <depth>`: Sets how many times the AI can call functions consecutively before it must provide a direct response to the user. This prevents infinite loops.

### Prompt Engineering
Effective communication with the AI often involves careful "prompt engineering" – crafting the instructions and context the AI receives.

*   **System Prompts:** These are overarching instructions that guide the AI's personality, role, and response style.
    *   `[p]assistant system [prompt_text_or_attach_file]`: Sets the main system prompt for the server. This is a powerful way to define the AI's base behavior.
*   **Initial User Prompts (Pre-Prompt):** This is text that gets prepended to the user's first message in a new conversation.
    *   `[p]assistant prompt [prompt_text_or_attach_file]`: Sets this initial prompt. It can be used to set the scene or provide initial context.
*   **Channel-Specific System Prompts:** You can override the main system prompt for specific channels.
    *   `[p]assistant channelprompt <#channel> [system_prompt_or_attach_file]`: Sets a custom system prompt for interactions within the specified channel.
*   **Per-Conversation System Prompts:** Users can temporarily set their own system prompt for their current conversation if allowed.
    *   `[p]convoprompt [prompt_text]`: Sets a system prompt for the duration of the current conversation.
    *   `[p]assistant sysoverride`: Server admins can toggle whether users are allowed to use `[p]convoprompt`.
*   **Placeholders:** Prompts can include dynamic placeholders that get replaced with current information. Examples include:
    *   `{username}`, `{displayname}`: The user's name.
    *   `{botname}`: The bot's name.
    *   `{channelname}`, `{channelmention}`: Current channel details.
    *   `{server}`: Server name.
    *   `{time}`, `{date}`, `{timestamp}`: Current time/date information (respects `[p]assistant timezone`).
    *   And many more (refer to `[p]help assistant prompt` or `[p]help assistant system` for a full list).

### Image Generation
The Assistant can generate images using OpenAI's DALL-E models.

*   **`[p]draw <prompt> [size] [quality] [style]`** (App Command): This command takes a textual description (prompt) and generates an image.
    *   You can often specify parameters like `size` (e.g., `1024x1024`), `quality` (e.g., `hd`), and `style` (e.g., `vivid`, `natural`), though available options depend on the specific DALL-E model version being used by the API.
    *   The availability of this command is controlled by `[p]assistant toggledraw`.

### Channel Context
This feature allows the Assistant to use recent messages from the current channel as part of its context when formulating a response, even if those messages are not part of the direct conversation history with the AI.

*   **Enabling:** Use `[p]assistant channelcontext enable True` to turn this feature on.
*   **How it Works:** When enabled, the cog fetches a configurable number of recent messages from the channel where the interaction is happening. This text is then provided to the AI as additional context.
*   **Configuration:**
    *   `[p]assistant channelcontext maxmessages <count>`: Sets the maximum number of recent messages (0-50) from the channel to include.
    *   `[p]assistant channelcontext includebot <True/False>`: Determines whether messages from other bots (including the Assistant itself) should be part of this fetched context.
    *   View current settings with `[p]assistant channelcontext showsettings`.

### Internet Search (Web Search Function)
The Assistant can be equipped with a function to search the internet to answer questions about recent events or topics not covered in its training data.

*   **`search_internet` Function:** This is a built-in custom function that, when enabled and called by the AI, uses the Brave Search API to perform a web search.
*   **API Key:** To enable this functionality, the bot owner must set a Brave Search API key using `[p]assistant braveapikey`. Brave offers a free tier for their API that is often sufficient for typical bot usage.
*   The AI will decide when to use this function based on the user's query. You can often prompt it to search by asking things like "Search the web for..." or if it indicates it doesn't have up-to-date information.

## Configuration Deep Dive
The Assistant cog offers a rich set of configuration options, primarily managed through the `[p]assistant` command and its various subcommands. This allows for fine-tuned control over the AI's behavior, performance, and integration within your server.

Key areas to focus on when configuring the Assistant include:

*   **API Keys:**
    *   **OpenAI API Key:** Essential for core functionality. Set per-server via `[p]assistant openaikey`.
    *   **Google Keys:** Optional for using Gemini models, either via Google AI Studio (`[p]assistant setgaistudiokey` - global) or Google Cloud ADC (`[p]assistant gauth` - global project ID).
    *   **Brave API Key:** For enabling the `search_internet` function (`[p]assistant braveapikey` - global).
*   **Model Selection:**
    *   **Chat Model:** Choose the primary language model for conversations using `[p]assistant model <model_name>`.
    *   **Embedding Model:** Select the model for generating embeddings via `[p]assistant embedmodel <model_name>`. This impacts how textual data is converted for similarity searches.
*   **Prompt Customization:** Tailor the AI's responses and personality.
    *   **Global Prompts:** Server-wide system instructions (`[p]assistant system`) and initial user message prefixes (`[p]assistant prompt`).
    *   **Channel-Specific Prompts:** Override global system prompts for particular channels (`[p]assistant channelprompt`).
    *   **Per-Conversation Prompts:** Allow users to set temporary system prompts for their own conversations (`[p]convoprompt`), if enabled by `[p]assistant sysoverride`.
*   **Embedding Behavior (Memory Control):**
    *   `[p]assistant topn <count>`: How many relevant embeddings are fetched.
    *   `[p]assistant relatedness <score>`: The similarity threshold for fetching embeddings.
    *   `[p]assistant embedmethod`: The strategy for incorporating embeddings into the AI's context (dynamic, static, hybrid, user).
*   **Function Call Toggles:**
    *   `[p]assistant functioncalls`: Globally enable or disable the AI's ability to use functions.
    *   `[p]assistant maxrecursion <depth>`: Limit how many consecutive function calls the AI can make.
*   **Overrides and Access Control:**
    *   **Role-Based Overrides:** Customize settings like model, max tokens, and retention for specific roles using `[p]assistant override ...` commands.
    *   **Blacklists/Tutors:** Control who the assistant interacts with or who can create embeddings using `[p]assistant blacklist` and `[p]assistant tutor`.

For a comprehensive list of all settings, use `[p]assistant view` and explore the subcommands detailed in the "Commands" section.

## Third-Party Cog Integration
The Assistant cog is designed to be extensible. Other Red cogs can register their own custom functions with the Assistant. This allows developers to create specialized tools or integrate functionalities from their cogs directly into the AI's capabilities.

*   When a third-party cog registers a function, it will appear in the list viewable via `[p]customfunctions`.
*   These functions are subject to the same management rules as functions defined directly by the bot owner:
    *   They can be enabled or disabled on a per-server basis through the `[p]customfunctions` menu.
    *   Their usage is governed by the global `[p]assistant functioncalls` toggle.
    *   Permissions associated with these functions (if defined by the third-party cog) will be respected.
*   Server administrators should review the functions registered by third-party cogs to understand what capabilities are being added to the Assistant.

## Data Privacy
The following statement describes how user data is handled by this cog:

"This cog stores prompts and OpenAI API keys on a per server basis. If enabled, conversations with the bot are also persistently stored"

This means:
*   Server-specific configurations, including system prompts and initial prompts, are stored.
*   OpenAI API keys are stored per server if set by an administrator.
*   If the bot owner enables persistent conversations (`[p]assistant persist`), the history of interactions with the Assistant will be saved to disk, allowing them to survive bot restarts. Otherwise, conversation history is held in memory and cleared on cog reload or bot restart.
*   Embeddings, which are derived from user messages or provided data, are also stored per server.

Please ensure your usage of this cog complies with your server's privacy policies and any applicable regulations.

## License
This cog is licensed under the MIT License. See the `LICENSE` file in the cog's directory or repository for more details.
