import uvicorn

if __name__ == '__main__':
    uvicorn.run('app:app', port=1111, host='127.0.0.1', reload=True)
