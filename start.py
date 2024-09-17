from src.ui.ui import UI
from src.services.services import Services
from src.ai.ai import AI

services = Services()
ai = AI(services)
ui = UI(services, ai)

ui.start()
