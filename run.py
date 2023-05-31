if __name__ == '__main__':
    import uvicorn
    uvicorn.run('blackjack.controller.app_jwt:app',
                host='127.0.0.1',
                port=8080,
                reload=True)
