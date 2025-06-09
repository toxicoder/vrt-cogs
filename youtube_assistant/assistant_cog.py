import asyncio
import os
import json
import logging

import discord
from discord.ext import commands
from redbot.core.bot import Red
from redbot.core.config import Config

# For .env loading
from dotenv import load_dotenv

# For Gemini API
import google.generativeai as genai

# For YouTube API
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request # For checking token validity and refresh

# For YouTube OAuth flow (primarily for initial setup, but good to have if token needs manual refresh steps)
# from google_auth_oauthlib.flow import InstalledAppFlow

# It's good practice to have a logger
log = logging.getLogger("red.yourcogname.assistantcog") # Replace yourcogname as appropriate

class AssistantCog(commands.Cog):
    """
    A cog to create YouTube Music playlists using natural language via Gemini and YouTube Data API.
    """

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890) # Replace with a unique identifier
        # Define default global settings if any, though most will be from .env
        # self.config.register_global()

        # Load environment variables from .env file located in the bot's root directory
        # Assumes .env is in the same directory as red.py or the main bot script
        # For Redbot, data_path often is where such files might be looked for by users,
        # but .env is typically root. Let's assume root for now.
        try:
            # Try to find .env in the bot's root directory.
            # This might need adjustment based on actual Redbot deployment structure.
            # A common pattern for Redbot cogs is to let users configure paths or use core Red data paths.
            # For simplicity of this task, we'll rely on python-dotenv's default behavior (searching current dir and parents)
            # or specify a path if known.
            # If this cog were packaged, it wouldn't have direct access to bot's root .env easily.
            # The spec says "loaded from a .env file using the python-dotenv library".

            # Assuming the .env file is in the bot's root instance directory
            # For a cog, accessing a bot-root .env can be tricky.
            # A more robust RedBot way might be to use `redbot.core.drivers.DotEnv` if available and suitable,
            # or have users set these via `[p]set api` commands.
            # Given the prompt, direct dotenv usage is specified.

            # To make this more robust for different execution environments for the bot:
            # We check a few common locations for the .env file.
            # 1. Current working directory (if bot is run from its root)
            # 2. One level up (if the script/cog is in a subdirectory like `cogs/`)
            # This is a simplified approach. A production bot might need a more sophisticated config strategy.

            env_path = None
            if os.path.exists(".env"):
                env_path = ".env"
            elif os.path.exists("../.env"): # If cogs are in a 'cogs' subdirectory of the bot root
                env_path = "../.env"
            elif os.path.exists("../../.env"): # If cogs are nested deeper, e.g. cogs/author_repo/cog_name/
                env_path = "../../.env"

            if env_path:
                load_dotenv(dotenv_path=env_path)
                log.info(f"Loaded .env file from: {os.path.abspath(env_path)}")
            else:
                # Fallback to environment variables if .env not found (e.g., in Docker/Heroku)
                log.info(".env file not found in common locations, relying on environment variables.")
                # No need to call load_dotenv() if no .env file, os.getenv will still work if vars are set in the environment

        except Exception as e:
            log.error(f"Error loading .env file: {e}. Ensure your .env file is in the bot's root directory or parent directories.")
            # Depending on strictness, could raise an error or proceed if env vars are set directly

        # Load API keys from environment
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.youtube_client_id = os.getenv("YOUTUBE_CLIENT_ID")
        self.youtube_client_secret = os.getenv("YOUTUBE_CLIENT_SECRET")
        self.youtube_refresh_token = os.getenv("YOUTUBE_REFRESH_TOKEN")
        # These might be needed if not using a pre-saved refresh token, or for more complex OAuth credential objects
        # self.youtube_token_uri = os.getenv("YOUTUBE_TOKEN_URI", "https://oauth2.googleapis.com/token")
        # self.youtube_auth_uri = os.getenv("YOUTUBE_AUTH_URI", "https://accounts.google.com/o/oauth2/auth")
        # self.youtube_project_id = os.getenv("YOUTUBE_PROJECT_ID") # Often part of client_secrets.json

        self.gemini_model = None
        self.youtube_service = None

        if not self.gemini_api_key:
            log.error("GEMINI_API_KEY not found in environment variables or .env file.")
            # Potentially prevent cog loading or disable commands if critical keys are missing
        else:
            try:
                genai.configure(api_key=self.gemini_api_key)
                self.gemini_model = genai.GenerativeModel('gemini-1.5-pro-latest')
                log.info("Gemini API client configured.")
            except Exception as e:
                log.error(f"Failed to configure Gemini API client: {e}")

        if not all([self.youtube_client_id, self.youtube_client_secret, self.youtube_refresh_token]):
            log.error("YouTube OAuth credentials (CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN) not fully found.")
        else:
            try:
                self._initialize_youtube_service() # Placeholder, will be implemented in Step 3
                if self.youtube_service:
                    log.info("YouTube Data API service initialization process completed.")
                else:
                    # This specific error is now handled by _initialize_youtube_service itself or the generic exception catch.
                    pass # Or a more generic log if needed, but specific failure is logged in the method itself
            except Exception as e:
                log.error(f"Error during YouTube service initialization call: {e}")

    def _initialize_youtube_service(self):
        log.info("Attempting to initialize YouTube Data API service...")
        self.youtube_service = None  # Ensure it's None if setup fails

        if not all([self.youtube_client_id, self.youtube_client_secret, self.youtube_refresh_token]):
            log.error("YouTube OAuth credentials (CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN) are not fully configured. YouTube service cannot be initialized.")
            return

        try:
            # Create credentials object from the stored/loaded refresh token
            creds = Credentials.from_authorized_user_info(
                info={
                    "client_id": self.youtube_client_id,
                    "client_secret": self.youtube_client_secret,
                    "refresh_token": self.youtube_refresh_token,
                    # Token URI is usually fixed for Google's OAuth 2.0
                    "token_uri": "https://oauth2.googleapis.com/token"
                },
                scopes=["https://www.googleapis.com/auth/youtube.force-ssl"]
            )

            # Check if the credentials are valid and refresh if necessary
            # This is crucial because the access token obtained from a refresh token is short-lived.
            if not creds.valid:
                if creds.expired and creds.refresh_token:
                    log.info("YouTube API credentials expired. Attempting to refresh...")
                    try:
                        creds.refresh(Request())
                        log.info("YouTube API credentials refreshed successfully.")
                    except Exception as e:
                        log.error(f"Error refreshing YouTube API credentials: {e}")
                        # Potentially, if refresh fails, you might want to notify an admin or disable functionality.
                        # For now, we'll let it proceed, and API calls will fail.
                        return # Stop initialization if refresh fails
                else:
                    # This case might indicate a problem with the refresh token itself or configuration.
                    log.error("YouTube credentials are not valid and no refresh token available or not expired yet (which is odd). Cannot initialize YouTube service.")
                    return

            self.youtube_service = build("youtube", "v3", credentials=creds, cache_discovery=False) # cache_discovery=False for dynamic environments
            log.info("YouTube Data API service initialized successfully.")

        except HttpError as e:
            log.error(f"HttpError during YouTube service initialization: {e.status_code} {e.resp.get('content', '')}")
        except Exception as e:
            log.error(f"An unexpected error occurred during YouTube service initialization: {e}", exc_info=True)

    # --- Cog Setup/Teardown (Optional but good practice) ---
    async def cog_load(self):
        log.info(f"{self.__class__.__name__} loaded.")
        # You can add checks here, e.g., if API keys are missing, you could print a warning to console
        if not self.gemini_model:
            log.warning("Gemini model not available. 'createplaylist' command may fail.")
        if not self.youtube_service:
            # This will be called before _initialize_youtube_service is fully implemented
            # So, this warning might appear on first load, then clear if init is successful later.
            # Let's refine this logging after YouTube init is solid.
            log.warning("YouTube service not available. 'createplaylist' command may fail.")


    async def cog_unload(self):
        log.info(f"{self.__class__.__name__} unloaded.")
        # Clean up any resources if necessary (e.g., close HTTP sessions if any were manually created)

    # --- Helper methods and commands will go below ---

    @commands.hybrid_command(
        name="createplaylist",
        description="Creates a YouTube playlist based on your prompt using AI."
    )
    @commands.cooldown(1, 60, commands.BucketType.user) # Example cooldown: 1 use per 60s per user
    @commands.guild_only() # Typically, bot commands that interact with external services are guild_only
    async def createplaylist(self, ctx: commands.Context, *, prompt: str):
        """
        Creates a YouTube Music playlist using AI based on the provided prompt.

        Example:
        [p]createplaylist a workout mix with upbeat electronic music
        /createplaylist prompt:a fun summer vibe playlist with indie pop songs
        """
        # The prompt argument description for slash commands is inferred by discord.py
        # from the docstring or type hint if not explicitly set in @app_commands.describe
        # For hybrid commands, the help formatter will use the docstring.
        # We can add app_commands.describe for more explicit slash command help.

        # Deferral and initial response are handled by _create_playlist_logic
        await self._create_playlist_logic(ctx, prompt)

    async def _create_playlist_logic(self, ctx: commands.Context, prompt: str):
        """Core logic for creating a YouTube playlist based on a prompt."""

        # 1. Initial Acknowledgement
        initial_response_message = None
        is_deferred = False
        try:
            if ctx.interaction: # Indicates a slash command or component interaction that can be deferred
                # Using ephemeral=False for deferral, so followup is visible.
                # Initial ack can be ephemeral if we want to hide "thinking..."
                # For now, let's make the deferral visible, final message will replace it.
                await ctx.defer(ephemeral=False)
                is_deferred = True
                log.info(f"Interaction deferred for prompt: {prompt}")
            else: # Traditional prefix command or from on_message
                initial_response_message = await ctx.send("🤖 Crafting your playlist... this may take a moment.")
                log.info(f"Sent initial message for prompt: {prompt}")
        except discord.errors.NotFound: # Interaction may have expired
            log.warning("Interaction not found, likely expired before deferral/response.")
            await ctx.send("Sorry, the request took too long to acknowledge and may have expired. Please try again.")
            return
        except Exception as e:
            log.error(f"Error sending initial acknowledgement: {e}", exc_info=True)
            # Can't send to discord, so just log and exit
            return

        # Helper to send messages (handles followup for deferred interactions)
        async def send_response(message_content=None, embed=None, view=None):
            if is_deferred:
                # If an initial message was also sent for some reason (should not happen with defer),
                # we might need to delete it. But defer handles the placeholder.
                if ctx.interaction: # Should always be true if is_deferred
                    await ctx.followup.send(content=message_content, embed=embed, view=view)
            elif initial_response_message: # We sent a placeholder message, try to edit it or send new
                try:
                    # Try to edit the initial message if only content is changing
                    if message_content and not embed and not view:
                        await initial_response_message.edit(content=message_content)
                    else: # Otherwise, send a new message (e.g. if sending an embed)
                         await initial_response_message.delete() # Clean up placeholder
                         await ctx.send(content=message_content, embed=embed, view=view)
                except discord.NotFound: # Initial message might have been deleted
                    await ctx.send(content=message_content, embed=embed, view=view)
                except Exception as e:
                    log.error(f"Error updating/sending response: {e}")
                    await ctx.send(content="An error occurred while trying to update you. Please check logs.")
            else: # Fallback, should not happen if initial ack worked
                await ctx.send(content=message_content, embed=embed, view=view)

        # 2. API Client Checks
        if not self.gemini_model:
            log.error("Gemini model not available for _create_playlist_logic.")
            await send_response("I'm sorry, but my connection to the AI story-teller (Gemini) is not working. Please try again later.")
            return
        if not self.youtube_service:
            log.error("YouTube service not available for _create_playlist_logic.")
            await send_response("I'm sorry, but my connection to YouTube is not working. Please try again later.")
            return

        # 3. Gemini API Call
        playlist_data = None
        try:
            gemini_prompt = f"""
You are a helpful assistant that creates music playlists.
Based on the user's request, generate a JSON object with the following structure:
{{
  "playlist_name": "string",
  "description": "string",
  "songs": [
    {{"title": "string", "artist": "string"}}
  ]
}}
Only respond with the JSON object. Do not include any other text, explanations, or markdown formatting like ```json ... ```.
Ensure song titles and artists are accurate and well-known if possible.
User request: "{prompt}"
"""
            log.info(f"Sending prompt to Gemini: {prompt}")
            # Gemini API expects "parts" for the prompt if it's just text.
            response = await self.gemini_model.generate_content_async(gemini_prompt) # Use async version

            # Clean the response text to extract only the JSON part
            # Gemini Pro 1.5 sometimes still wraps in ```json ... ``` despite instructions
            cleaned_response_text = response.text.strip()
            if cleaned_response_text.startswith("```json"):
                cleaned_response_text = cleaned_response_text[7:]
            if cleaned_response_text.endswith("```"):
                cleaned_response_text = cleaned_response_text[:-3]

            log.debug(f"Gemini raw response: {response.text}")
            log.info(f"Gemini cleaned JSON attempt: {cleaned_response_text}")
            playlist_data = json.loads(cleaned_response_text)

            # Validate basic structure
            if not all(k in playlist_data for k in ["playlist_name", "description", "songs"]):
                raise KeyError("Missing one or more required keys in Gemini response.")
            if not isinstance(playlist_data["songs"], list):
                raise ValueError("Gemini response 'songs' field is not a list.")
            if not playlist_data["songs"]: # Ensure there's at least one song
                 await send_response("The AI couldn't come up with any songs for your prompt. Try being more specific or creative!")
                 return

        except json.JSONDecodeError as e:
            log.error(f"Error decoding JSON from Gemini: {e}. Response was: {response.text if 'response' in locals() else 'N/A'}")
            await send_response("I received a peculiar song list from the AI and couldn't quite understand it. Please try a different prompt!")
            return
        except (KeyError, ValueError) as e:
            log.error(f"Invalid structure in JSON from Gemini: {e}. Response was: {playlist_data if playlist_data else (response.text if 'response' in locals() else 'N/A')}")
            await send_response("The AI gave me a song list, but it seems to be missing some important details. Please try a different prompt!")
            return
        except Exception as e: # Catch other google.api_core.exceptions or general errors
            log.error(f"Error calling Gemini API: {e}", exc_info=True)
            await send_response("There was an issue dreaming up your playlist with the AI. Please try again.")
            return

        # 4. YouTube Playlist Creation
        new_playlist_id = None
        new_playlist_url = None
        try:
            log.info(f"Creating YouTube playlist: {playlist_data['playlist_name']}")
            playlist_request_body = {
                "snippet": {
                    "title": playlist_data["playlist_name"],
                    "description": playlist_data["description"]
                },
                "status": {"privacyStatus": "public"}
            }
            insert_request = self.youtube_service.playlists().insert(
                part="snippet,status",
                body=playlist_request_body
            )
            playlist_response = await self.bot.loop.run_in_executor(None, insert_request.execute) # Run blocking IO in executor
            new_playlist_id = playlist_response["id"]
            new_playlist_url = f"https://www.youtube.com/playlist?list={new_playlist_id}"
            log.info(f"Playlist created: {new_playlist_id} - {playlist_data['playlist_name']}")

        except HttpError as e:
            log.error(f"HttpError creating YouTube playlist: {e.resp.status} - {e.content}", exc_info=True)
            await send_response(f"I couldn't create the playlist on YouTube. Error: {e.resp.status}. Please try again later.")
            return
        except Exception as e:
            log.error(f"Unexpected error creating YouTube playlist: {e}", exc_info=True)
            await send_response("An unexpected error occurred while creating your playlist on YouTube. Please try again later.")
            return

        # 5. Song Search & Add Loop
        songs_added_count = 0
        total_songs_requested = len(playlist_data["songs"])
        failed_songs = []

        for i, song_item in enumerate(playlist_data["songs"]):
            try:
                song_title = song_item.get("title")
                song_artist = song_item.get("artist")
                if not song_title or not song_artist:
                    log.warning(f"Skipping song due to missing title/artist: {song_item}")
                    failed_songs.append(f"{song_title or 'N/A'} by {song_artist or 'N/A'} (missing info)")
                    continue

                query = f"{song_title} {song_artist}"
                log.info(f"Searching YouTube for ({i+1}/{total_songs_requested}): {query}")

                search_request = self.youtube_service.search().list(
                    part="snippet",
                    q=query,
                    type="video",
                    videoCategoryId="10", # Music Category
                    maxResults=1
                )
                search_response = await self.bot.loop.run_in_executor(None, search_request.execute)

                if search_response.get("items"):
                    video_id = search_response["items"][0]["id"]["videoId"]
                    log.info(f"Found videoId: {video_id} for query: {query}")

                    playlist_item_request_body = {
                        "snippet": {
                            "playlistId": new_playlist_id,
                            "resourceId": {
                                "kind": "youtube#video",
                                "videoId": video_id
                            }
                        }
                    }
                    insert_item_request = self.youtube_service.playlistItems().insert(
                        part="snippet",
                        body=playlist_item_request_body
                    )
                    await self.bot.loop.run_in_executor(None, insert_item_request.execute)
                    songs_added_count += 1
                    log.info(f"Added '{query}' (ID: {video_id}) to playlist {new_playlist_id}")
                else:
                    log.warning(f"No YouTube search results for: {query}")
                    failed_songs.append(f"{song_title} by {song_artist} (not found)")

            except HttpError as e:
                log.error(f"HttpError processing song '{query}': {e.resp.status} - {e.content}", exc_info=True)
                failed_songs.append(f"{song_title} by {song_artist} (API error adding)")
            except Exception as e:
                log.error(f"Unexpected error processing song '{query}': {e}", exc_info=True)
                failed_songs.append(f"{song_title} by {song_artist} (unexpected error)")

            # Small delay to avoid hitting rate limits too hard, if many songs
            # await asyncio.sleep(0.1) # Consider if rate limits become an issue

        # 6. Final Confirmation
        embed = discord.Embed(
            title="🎶 Playlist Created! 🎶",
            description=playlist_data.get("description", "Enjoy your new playlist!"),
            color=discord.Color.green() if songs_added_count > 0 else discord.Color.orange()
        )
        embed.add_field(name="Playlist Name", value=playlist_data["playlist_name"], inline=False)
        if new_playlist_url:
            embed.add_field(name="Link", value=f"[Click Here]({new_playlist_url})", inline=False)

        status_message = f"Successfully added {songs_added_count} out of {total_songs_requested} songs."
        if songs_added_count == 0 and total_songs_requested > 0:
             status_message = f"Could not add any of the {total_songs_requested} songs to the playlist. See logs for details."
        elif failed_songs:
            status_message += f"
Could not add: {', '.join(failed_songs[:3])}" # Show first few failures
            if len(failed_songs) > 3:
                status_message += f" and {len(failed_songs) - 3} more."

        embed.add_field(name="Status", value=status_message, inline=False)
        embed.set_footer(text="Powered by Gemini & YouTube Music")

        await send_response(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Listen for messages to handle @-mention commands."""
        # 1. Ignore messages from bots and ensure we are in a guild context
        if message.author.bot or not message.guild:
            return

        # 2. Check if the bot was mentioned at the beginning of the message
        bot_mention_strings = [
            self.bot.user.mention,
            f"<@{self.bot.user.id}>",       # Standard mention
            f"<@!{self.bot.user.id}>"      # Mention with nickname
        ]

        triggered_by_mention = None
        for mention_str in bot_mention_strings:
            if message.content.startswith(mention_str):
                triggered_by_mention = mention_str
                break

        if not triggered_by_mention:
            return

        # 3. Parse for command and prompt
        # Remove the mention and leading/trailing whitespace
        content_without_mention = message.content[len(triggered_by_mention):].strip()

        command_trigger = "createplaylist"

        if content_without_mention.lower().startswith(command_trigger):
            # Extract the prompt text
            prompt_text = content_without_mention[len(command_trigger):].strip()

            if not prompt_text:
                # User might have just typed "@BotName createplaylist"
                # Optionally, send a help message or ignore
                log.info(f"Mention command '{command_trigger}' received without prompt from {message.author.name}.")
                # await message.channel.send(f"Please provide a prompt after `@{self.bot.user.display_name} {command_trigger}`.")
                return # Or just ignore if no prompt

            log.info(f"Mention command '{command_trigger}' triggered by {message.author.name} with prompt: '{prompt_text}'")

            # 4. Invoke core logic
            # We need to create a context object for _create_playlist_logic
            # This ensures that responses go to the correct channel and user.
            ctx = await self.bot.get_context(message)
            if ctx: # Ensure context was successfully created
                # Check if the command itself is disabled or has checks that fail
                # For example, if the 'createplaylist' command itself has specific checks.
                # However, _create_playlist_logic doesn't assume it's being run by a valid command invocation directly.
                # We are programmatically calling its logic.
                # If createplaylist command had specific checks, we might want to replicate or call them.
                # For now, we directly call the logic.
                # It's also good to apply similar cooldowns if desired, though that's more complex for on_message.
                # The hybrid command already has a cooldown; this bypasses it.
                # For simplicity as per spec, we directly invoke.
                await self._create_playlist_logic(ctx, prompt_text)
            else:
                log.warning(f"Could not get context for message ID {message.id} from {message.author.name}")
        else:
            # Bot was mentioned, but not for the createplaylist command.
            # Could add other mention-based commands here in the future or just log.
            log.debug(f"Bot mentioned by {message.author.name}, but not for 'createplaylist': {content_without_mention}")

# --- End of AssistantCog methods ---
EOF
