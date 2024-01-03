if app.config['ENV'] == 'development':
    app.debug = True
    app.secret_key = 'development_secret_key'
elif app.config['ENV'] == 'production':
    app.debug = false
    app.secret_key = 'production_secret_key'