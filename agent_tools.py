"""Step 5: register two sequential tools. See lab.md for the full contract."""
from pydantic_ai import Agent, RunContext
from action_model import Action
from room_tools import RoomSession, GoalReached


def register_tools(agent: Agent):
    # TODO: observe_room(ctx) -> ctx.deps.observe()
    # TODO: perform_action(ctx, action: Action) -> ctx.deps.perform(action.model_dump())
    # Both must be sequential with retries=0. After a successful action,
    # raise GoalReached if ctx.deps.goal_reached; the final result is already logged.
    
    @agent.tool(sequential=True, retries=0)
    async def observe_room(ctx: RunContext[RoomSession]) -> dict:
        """Read the player's current public observation and allowed action schema."""
        return ctx.deps.observe()

    @agent.tool(sequential=True, retries=0)
    async def perform_action(ctx: RunContext[RoomSession], action: Action) -> dict:
        """Perform ONE look or open action using known IDs. Python decides the result"""
        result = ctx.deps.perform(action.model_dump())
        if ctx.deps.goal_reached:
            raise GoalReached("The key is visible and remains where it was found.")
        return result

    

