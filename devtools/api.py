from fastapi import FastAPI

def app():
    _api = FastAPI()

    @_api.get("/hello")
    async def root():
        return {"message": "Hello World, there 2!!"}

    return _api

def main():
    import uvicorn
    uvicorn.run(app(), host="0.0.0.0", port=8080)
    

if __name__ == "__main__":
    main()