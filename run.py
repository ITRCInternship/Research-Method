from app import create_app

app = create_app()

if __name__ == '__main__':
    host = app.config.get('FLASK_HOST', '0.0.0.0')
    port = int(app.config.get('FLASK_PORT', 5002))
    debug_flag = app.config.get('FLASK_DEBUG', True)
    app.run(host=host, port=port, debug=debug_flag)
