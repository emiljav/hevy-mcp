import os
import sys
import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

if sys.platform == "win32":
    import msvcrt
    msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"), override=True)

API_KEY = os.getenv("HEVY_API_KEY")
BASE_URL = "https://api.hevyapp.com"

mcp = FastMCP("hevy")


def _headers() -> dict:
    if not API_KEY:
        raise RuntimeError("HEVY_API_KEY is not set in environment")
    return {"api-key": API_KEY}


async def _get(path: str, params: dict | None = None) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}{path}",
            headers=_headers(),
            params=params,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_workouts(page: int = 1, pageSize: int = 10) -> dict:
    """
    Get a paginated list of workouts.

    Args:
        page: Page number (1-based).
        pageSize: Number of workouts per page (max 10 per Hevy API).
    """
    return await _get("/v1/workouts", {"page": page, "pageSize": pageSize})


@mcp.tool()
async def get_workout(workout_id: str) -> dict:
    """
    Get a single workout by its ID.

    Args:
        workout_id: The unique workout identifier.
    """
    return await _get(f"/v1/workouts/{workout_id}")


@mcp.tool()
async def get_workout_count() -> dict:
    """Get the total number of workouts logged by the authenticated user."""
    return await _get("/v1/workouts/count")


@mcp.tool()
async def get_exercise_history(
    exercise_template_id: str, page: int = 1, pageSize: int = 10
) -> dict:
    """
    Get workout history for a specific exercise template.

    Args:
        exercise_template_id: The exercise template ID to retrieve history for.
        page: Page number (1-based).
        pageSize: Number of entries per page.
    """
    return await _get(
        f"/v1/exercise_templates/{exercise_template_id}/history",
        {"page": page, "pageSize": pageSize},
    )


@mcp.tool()
async def get_routines(page: int = 1, pageSize: int = 10) -> dict:
    """
    List all routines saved by the authenticated user.

    Args:
        page: Page number (1-based).
        pageSize: Number of routines per page.
    """
    return await _get("/v1/routines", {"page": page, "pageSize": pageSize})


@mcp.tool()
async def get_exercise_templates(page: int = 1, pageSize: int = 10) -> dict:
    """
    List available exercise templates (exercise library).

    Args:
        page: Page number (1-based).
        pageSize: Number of templates per page.
    """
    return await _get("/v1/exercise_templates", {"page": page, "pageSize": pageSize})


if __name__ == "__main__":
    mcp.run()
