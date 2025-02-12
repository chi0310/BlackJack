if __name__ == '__main__':
    import uvicorn
    uvicorn.run('blackjack.controller.app:app',
                host='127.0.0.1',
                port=8080,
                reload=False)
