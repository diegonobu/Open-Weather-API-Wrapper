from api_wrapper.app import app, cache

if __name__ == '__main__':
    cache.init_app(app)
    app.run(port=5000, debug=True)
