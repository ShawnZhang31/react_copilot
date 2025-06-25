import os
from dotenv import load_dotenv
import asyncio

"""Utility functions used in our graph."""


async def split_model_and_provider(fully_specified_name: str) -> dict:
    """Initialize the configured chat model."""
    if ":" in fully_specified_name:
        provider, model = fully_specified_name.split(":", maxsplit=1)
    else:
        provider = "openai"
        model = fully_specified_name

    env_vars = await get_openai_env_vars()

    if provider == "deepseek":
        if not env_vars["api_key"]:
            raise ValueError("LLM_API_KEY environment variable is not set.")
        if not env_vars["base_url"]:
            raise ValueError("LLM_BASE_URL environment variable is not set.")
        
        return {
            "model": model,
            "model_provider": provider,
            "api_key": env_vars["api_key"],
            "api_base": env_vars["base_url"]
        }
    else:
        if not env_vars["api_key"]:
            raise ValueError("LLM_API_KEY environment variable is not set.")
        if not env_vars["base_url"]:
            raise ValueError("LLM_API_KEY environment variable is not set.")

        return {
            "model": model,
            "model_provider": provider,
            "api_key": env_vars["api_key"],
            "base_url": env_vars["base_url"]
        }

async def get_openai_env_vars() -> dict:
    """
    获取环境变量.env中OPENAI_API_KEY和OPENAI_BASE_URL的值
    
    Returns:
        dict: 包含API密钥和基础URL的字典
    """
    # 加载.env文件中的环境变量
    await asyncio.to_thread(load_dotenv)
    
    # 获取环境变量
    api_key = os.environ.get("LLM_API_KEY")
    base_url = os.environ.get("LLM_BASE_URL")

    return {
        "api_key": api_key,
        "base_url": base_url
    }


if __name__ == "__main__":
    # Example usage
    model_info = split_model_and_provider("deepseek:Qwen/Qwen3-32B")
    print(model_info)