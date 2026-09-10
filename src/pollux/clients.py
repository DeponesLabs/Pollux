import asyncio
import os
from datetime import datetime
import json
from dotenv import load_dotenv
from google import genai

from google.genai import types

load_dotenv()

from pollux.models import GeminiModel
from pollux.enums import GeminiModelType

try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
except ImportError as exc:  # pragma: no cover - dependency is optional at import time
    ClientSession = None
    StdioServerParameters = None
    stdio_client = None
    MCP_IMPORT_ERROR = exc
else:
    MCP_IMPORT_ERROR = None


class PolluxMCPClient:
    """Small sync wrapper around an MCP stdio server.

    This is intentionally minimal: Pollux can optionally connect to a server that
    exposes tools like ``query_star_catalog`` and invoke them without changing the
    Google Gemini chat flow.
    """

    def __init__(
        self,
        server_command: str | None = None,
        server_args: list[str] | None = None,
        env: dict[str, str] | None = None,
    ):
        if ClientSession is None or StdioServerParameters is None or stdio_client is None:
            raise ImportError(
                "The 'mcp' package is required for MCP client support. "
                f"Install it with: pip install mcp. Original error: {MCP_IMPORT_ERROR}"
            )

        self.server_command = server_command or os.environ.get("MCP_SERVER_COMMAND") or "python"
        self.server_args = server_args or [
            os.environ.get("MCP_SERVER_SCRIPT", "server.py")
        ]
        self.env = {**os.environ, **(env or {})}

    def _build_server_params(self) -> StdioServerParameters:
        return StdioServerParameters(
            command=self.server_command,
            args=self.server_args,
            env=self.env,
        )

    @staticmethod
    def _result_to_text(result: object) -> str:
        if result is None:
            return ""

        if hasattr(result, "content"):
            texts: list[str] = []
            for item in result.content:
                if hasattr(item, "text"):
                    texts.append(str(item.text))
                elif isinstance(item, dict):
                    if "text" in item:
                        texts.append(str(item["text"]))
                    else:
                        texts.append(json.dumps(item, ensure_ascii=False))
                else:
                    texts.append(str(item))
            if texts:
                return "\n".join(texts)

        if hasattr(result, "model_dump"):
            return json.dumps(result.model_dump(), ensure_ascii=False, indent=2)

        return str(result)

    def _run(self, coroutine):
        return asyncio.run(coroutine)

    async def _list_tools(self) -> list:
        async with stdio_client(self._build_server_params()) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                response = await session.list_tools()
                return list(response.tools)

    async def _call_tool(self, tool_name: str, arguments: dict[str, object] | None = None):
        async with stdio_client(self._build_server_params()) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                response = await session.call_tool(tool_name, arguments or {})
                return self._result_to_text(response)

    def list_tools(self) -> list:
        return self._run(self._list_tools())

    def call_tool(self, tool_name: str, arguments: dict[str, object] | None = None) -> str:
        return self._run(self._call_tool(tool_name, arguments))

    def query_star_catalog(self, star_name: str, catalog_id: str = "V/137D") -> str:
        return self.call_tool(
            "query_star_catalog",
            {"star_name": star_name, "catalog_id": catalog_id},
        )


class PolluxClient:
    
    today = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
    api_key = os.environ.get("GEMINI_API_KEY")
    daily_log_file = f"chat_records/gemini_records_{today}.txt"
        
    def __init__(
        self,
        model_type=GeminiModelType.FLASH_2_5,
        mcp_server_command: str | None = None,
        mcp_server_args: list[str] | None = None,
        mcp_env: dict[str, str] | None = None,
    ):

        if not PolluxClient.api_key:
            print("API Key not found! Please set the GEMINI_API_KEY environment variable.")
            exit()
            
        self.models : list[GeminiModel] = []
        self.safety_config = None
        self.mcp_client = None

        self.client = genai.Client(api_key=PolluxClient.api_key)
        self.set_safety_config()
        self.init_chat(model_type)
        self.fetch_models()
        self.configure_mcp_client(mcp_server_command, mcp_server_args, mcp_env)

    def configure_mcp_client(
        self,
        server_command: str | None = None,
        server_args: list[str] | None = None,
        env: dict[str, str] | None = None,
    ):
        command = server_command or os.environ.get("MCP_SERVER_COMMAND")
        if command is None:
            return

        self.mcp_client = PolluxMCPClient(
            server_command=command,
            server_args=server_args or [os.environ.get("MCP_SERVER_SCRIPT", "server.py")],
            env=env,
        )

    def query_star_catalog(self, star_name: str, catalog_id: str = "V/137D") -> str:
        if self.mcp_client is None:
            raise RuntimeError(
                "No MCP server is configured. Set MCP_SERVER_COMMAND or pass mcp_server_command="
                "when creating PolluxClient."
            )
        return self.mcp_client.query_star_catalog(star_name, catalog_id)

    def set_safety_config(self, hate_speech=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE, 
                                harassment=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                                sexually_explicit=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                                dangerous_content=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE):
        
        config = [
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                threshold=hate_speech
            ),
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                threshold=harassment
            ),
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                threshold=sexually_explicit
            ),
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=dangerous_content
            ),
        ]
        
        self.safety_config = types.GenerateContentConfig(safety_settings=config)

    def init_chat(self, model = GeminiModelType.FLASH_2_5):
        
        self.chat = self.client.chats.create(model=model, config=self.safety_config)
        
    def _chat_stream(self):
        
        print("#####__ Gemini Terminal is Ready! __#####")
        print("To exit, type 'quit' or 'exit'...\n")

        while True:
            user_input = input("\nYou: ")
            
            if user_input.lower() in ['quit', 'exit']:
                print("See you later!")
                break
                
            if not user_input.strip():
                continue

            try:
                response = self.chat.send_message(user_input)
                print(f"\nGemini: {response.text}")
                yield user_input, response.text
    
            except Exception as error:
                print(f"\nAn error occured: {error}")

    def fetch_models(self):
        
        for raw_model in self.client.models.list():
            gmodel = GeminiModel.from_api(raw_model)
            self.models.append(gmodel)
    
    def export_models_to_json(self, path="gemini_models_catalog.json"):
            
        models_dict_list = [model.to_dict() for model in self.models]
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(models_dict_list, f, indent=4, ensure_ascii=False)

    def exec_chat(self, archiver):
        
        print(f"#####__ Pollux Terminal is Ready! (Archiving to: {archiver.filename}) __#####")
        
        for user_input, response_text in self._chat_stream():
            archiver.append_message("User", user_input)
            archiver.append_message("Pollux", response_text)
            
        archiver.save()
