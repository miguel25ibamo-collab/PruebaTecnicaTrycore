from app import create_app

# Este archivo es el punto de entrada para 'python wsgi.py' o servidores WSGI (gunicorn, waitress, etc.)
app = create_app()

if __name__ == "__main__":
    # debug=True recarga en caliente y muestra debugger
    app.run(debug=True)
