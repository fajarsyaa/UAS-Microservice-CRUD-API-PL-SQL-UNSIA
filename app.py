from app import app

app.secret_key = 'universitas_siber_asia'

if __name__ == '__main__':
    app.run(debug=True)
