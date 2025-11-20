from infra.utils.log import get_uvicorn_log_config
from presentation.rest.app import app

if __name__ == "__main__":
    import uvicorn

    lc = get_uvicorn_log_config()

    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=lc)
