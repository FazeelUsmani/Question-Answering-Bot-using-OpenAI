from fastapi import Header, HTTPException

async def get_api_key(x_api_key: str = Header(...)):
    if x_api_key != "expected_api_key":
        raise HTTPException(status_code=400, detail="Invalid API Key")
    return x_api_key
