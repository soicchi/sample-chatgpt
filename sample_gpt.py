import json
import os
from abc import ABC, abstractmethod
from typing import Callable, Dict, List, Optional, Any

from openai import OpenAI


# インターフェース（抽象クラス）
class WeatherService(ABC):
    """天気情報を提供するサービスのインターフェース"""
    @abstractmethod
    def get_weather(self, location: str, unit: str = "fahrenheit") -> Dict[str, str]:
        pass


class AIClient(ABC):
    """AIクライアントのインターフェース"""
    @abstractmethod
    def chat_completion(self, messages: List[Dict[str, Any]], **kwargs) -> Any:
        pass


# 具象クラス
class MockWeatherService(WeatherService):
    """モックの天気サービス実装"""
    def __init__(self) -> None:
        self.weather_data = {
            "tokyo": {"location": "Tokyo", "temperature": "10"},
            "san francisco": {"location": "San Francisco", "temperature": "72"},
            "paris": {"location": "Paris", "temperature": "22"},
        }

    def get_weather(self, location: str, unit: str = "fahrenheit") -> Dict[str, str]:
        loc_info = self.weather_data.get(location.lower(), None)
        if loc_info is None:
            return {"location": location, "temperature": "unknown"}

        loc_info["unit"] = unit
        return loc_info


class OpenAIClient(AIClient):
    """OpenAIのAPI実装"""
    def __init__(self, api_key: Optional[str] = None):
        if api_key is None:
            raise ValueError("API key is required.")

        self.client = OpenAI(api_key=api_key)

    def chat_completion(self, messages: List[Dict[str, Any]], **kwargs) -> Any:
        return self.client.chat.completions.create(messages=messages, **kwargs)


# ツール関連のクラス
class ToolDefinition:
    """ツール定義を管理するクラス"""
    @staticmethod
    def get_weather_tool_definition() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "unit": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"],
                        },
                    },
                    "required": ["location"],
                },
            }
        }


class ToolRegistry:
    """利用可能なツール関数を管理するレジストリ"""
    def __init__(self, weather_service: WeatherService):
        self.weather_service = weather_service
        self._registry = {
            "get_current_weather": self._get_current_weather,
        }

    def get_function(self, func_name: str) -> Callable:
        """関数名から対応する関数を取得"""
        func = self._registry.get(func_name)
        if func is None:
            raise ValueError(f"Function {func_name} not found.")
        return func

    def _get_current_weather(self, location: str, unit: str = "fahrenheit") -> str:
        """天気情報を取得してJSON文字列で返す"""
        weather_info = self.weather_service.get_weather(location, unit)
        return json.dumps(weather_info)


# サービスクラス
class ChatService:
    """チャット機能を提供するサービス"""
    def __init__(self, ai_client: AIClient):
        self.ai_client = ai_client

    def image_description(self, image_url: str) -> str:
        """画像説明機能"""
        response = self.ai_client.chat_completion(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": [
                    {"type": "text", "text": "画像を説明してください。"},
                    {"type": "image_url", "image_url": {"url": image_url}},
                ]}
            ],
        )
        return response.choices[0].message.content


class FunctionCallingService:
    """関数呼び出し機能を提供するサービス"""
    def __init__(self, ai_client: AIClient, tool_registry: ToolRegistry):
        self.ai_client = ai_client
        self.tool_registry = tool_registry

    def process_query(self, user_query: str) -> str:
        """ユーザーのクエリを処理して結果を返す"""
        messages = [{"role": "user", "content": user_query}]
        tools = [ToolDefinition.get_weather_tool_definition()]

        # 最初のAPIコール
        response = self.ai_client.chat_completion(
            model="gpt-4o",
            messages=messages,
            tools=tools,
        )

        res_msg = response.choices[0].message
        messages.append(res_msg.to_dict())

        # ツール呼び出しの処理
        for tool_call in res_msg.tool_calls or []:
            func_name = tool_call.function.name
            func = self.tool_registry.get_function(func_name)
            func_args = json.loads(tool_call.function.arguments)

            result = func(
                location=func_args.get("location"),
                unit=func_args.get("unit"),
            )

            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": func_name,
                "content": result,
            })

        # 最終回答の取得
        second_res = self.ai_client.chat_completion(
            model="gpt-4o",
            messages=messages,
        )

        return second_res.to_json(indent=2)


# メイン実行
def sample_chatgpt():
    # 依存関係の注入
    weather_service = MockWeatherService()
    ai_client = OpenAIClient(api_key=os.getenv("OPENAI_API_KEY"))
    tool_registry = ToolRegistry(weather_service)

    # サービスの作成
    function_calling_service = FunctionCallingService(ai_client, tool_registry)

    # サンプル実行
    # image_url = "https://raw.githubusercontent.com/yoshidashingo/langchain-book/main/assets/cover.jpg"
    # result = chat_service.image_description(image_url)
    # print(result)

    result = function_calling_service.process_query("Tokyoの天気はどうですか？")
    print(result)


if __name__ == "__main__":
    sample_chatgpt()
