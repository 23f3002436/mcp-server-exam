
import hashlib
import os

from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_request

mcp = FastMCP("Exam Challenge Server")

EMAIL = "23f3002436@ds.study.iitm.ac.in".strip().lower()


@mcp.tool
def solve_challenge() -> str:
    """Return the SHA-256 challenge hash from the HTTP request header."""

    request = get_http_request()
    challenge = request.headers.get("x-exam-challenge")

    if not challenge:
        raise ValueError("Missing X-Exam-Challenge header")

    message = f"{challenge}:{EMAIL}"
    digest = hashlib.sha256(message.encode("utf-8")).hexdigest()

    return digest[:16]


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))

    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=port,
        path="/mcp",
    )
