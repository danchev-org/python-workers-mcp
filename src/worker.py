import sys

from workers import DurableObject

sys.path.insert(0, "/session/metadata/vendor")
sys.path.insert(0, "/session/metadata")


def setup_server():
    from starlette.middleware import Middleware
    from starlette.middleware.cors import CORSMiddleware
    from mcp.server.fastmcp import FastMCP

    from exceptions import HTTPException, http_exception

    mcp = FastMCP("Open Markets Server", "0.0.1")

    from openmarkets.tools import (
        register_analyst_data_tools,
        register_calendar_tools,
        register_corporate_actions_tools,
        register_crypto_tools,
        register_extended_market_tools,
        register_financial_statements_tools,
        register_fund_tools,
        register_historical_data_tools,
        register_market_data_tools,
        register_news_tools,
        register_options_tools,
        register_stock_info_tools,
        register_technical_analysis_tools,
    )


    # Register all tool modules
    register_stock_info_tools(mcp)
    register_historical_data_tools(mcp)
    register_analyst_data_tools(mcp)
    register_financial_statements_tools(mcp)
    register_options_tools(mcp)
    register_calendar_tools(mcp)
    register_market_data_tools(mcp)
    register_crypto_tools(mcp)
    register_technical_analysis_tools(mcp)
    register_corporate_actions_tools(mcp)
    register_extended_market_tools(mcp)
    register_news_tools(mcp)
    register_fund_tools(mcp)

    return mcp, app


class FastMCPServer(DurableObject):
    def __init__(self, ctx, env):
        self.ctx = ctx
        self.env = env
        self.mcp, self.app = setup_server()

    async def on_fetch(self, request, env, ctx):
        import asgi

        return await asgi.fetch(self.app, request, self.env, self.ctx)


async def on_fetch(request, env):
    id = env.ns.idFromName("A")
    obj = env.ns.get(id)
    return await obj.fetch(request)
