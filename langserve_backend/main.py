from fastapi import FastAPI, HTTPException
from langserve import add_routes
from diagnostics_graph import build_graph
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Medical Diagnostics API",
    description="AI-powered medical diagnostics using LangGraph and EuriAI",
    version="1.0.0"
)

try:
    # Build the diagnostic graph
    logger.info("Building diagnostic graph...")
    graph = build_graph()
    logger.info("Graph built successfully")
    
    # Add routes
    add_routes(app, graph, path="/diagnose")
    logger.info("Routes added successfully")
    
except Exception as e:
    logger.error(f"Error during startup: {e}")
    raise e

@app.get("/")
async def root():
    return {"message": "AI Medical Diagnostics API is running", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "AI Medical Diagnostics"}