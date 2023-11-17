from fastapi import FastAPI

app=FastAPI()

@app.post("/process_data")
def process_data(user_input : str):
    return {"message":"sent successfully"}