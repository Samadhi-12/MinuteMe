import os
from fastapi import Depends, HTTPException, status, Request
# Correct imports for the 'clerk-backend-api' package
from clerk_backend_api import Clerk, models # Import 'models' for error handling
from clerk_backend_api.security import AuthenticateRequestOptions

def get_clerk_client():
    """Initializes and returns the Clerk client using the secret key."""
    clerk_secret_key = os.getenv("CLERK_SECRET_KEY")
    if not clerk_secret_key:
        raise ValueError("CLERK_SECRET_KEY not found in environment variables.")
    # Per documentation, the client is initialized with the secret key as the bearer_auth token
    return Clerk(bearer_auth=clerk_secret_key)

async def get_current_user(request: Request) -> dict:
    """
    A FastAPI dependency that verifies the bearer token from the request
    using the official authenticate_request method.
    """
    clerk = get_clerk_client()
    try:
        print("🔐 Verifying user token...")
        # Use the official authenticate_request method from the SDK
        request_state = clerk.authenticate_request(
            request,
            AuthenticateRequestOptions() # Add options like authorized_parties if needed
        )

        if not request_state.is_signed_in:
             raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User is not signed in.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # The token payload is available in request_state.payload
        session_claims = request_state.payload
        print(f"✅ Token verified for user_id: {session_claims['sub']}")
        return session_claims

    # Catch the correct base error class from the 'models' submodule
    except models.ClerkBaseError as e:
        print(f"❌ Token verification failed: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials: {e.message}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        # Catch any other unexpected errors during authentication
        print(f"❌ An unexpected error occurred during authentication: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal error occurred during authentication."
        )