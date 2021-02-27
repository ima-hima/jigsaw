from src import create_app
import settings

app = create_app()
app.run(debug = True)
