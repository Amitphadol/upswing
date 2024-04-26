import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from asyncio import CancelledError

from utilities.response import STANDARD_RESPONSES
from resources import objects
import logging

logger = logging.getLogger("Main Logger")

def _get_app():
   """
   Creates a new FastAPI application.

   """
   app = FastAPI(
      title="UpSwing Hotel Management System",
      description="""FastAPI, MQTT, MongoDB""",
      docs_url="/docs",
      redoc_url="/redoc",
      openapi_url="/openapi.json",
      responses=STANDARD_RESPONSES,
      lifespan=lifespan,
   )
   @app.get("/", include_in_schema=False)
   def root():
      """Return the root of the application."""
      return {
         "App": "Hotal management API",
         "version": "1.0",
         "status": "healthy",
      }

   return app
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Run the lifespan event."""
    try:
        objects.app_resources = objects.AppResources.initialize()
    except Exception as exception:
        logger.exception(
            f"Error occurred while initializing the objects: {exception}",
        )
        raise exception
    logger.info(f"Hotal management Application started successfully.")
    # End of startup events
    try:
        yield
    except CancelledError:
        pass
    finally:
        objects.app_resources.destroy()
        logger.warning("Hotal management Application shutting down.")


if __name__ == "__main__":
   uvicorn.run(
      app="main:_get_app",
      host="0.0.0.0",
      port=8005,
      factory=True,
      limit_concurrency=1000,
      log_level="error",
      loop="uvloop",
   )
