from srk.app import create_app  # type: ignore

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
