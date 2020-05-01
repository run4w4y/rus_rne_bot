import logging
import rus_rne_bot


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
rus_rne_bot.run()
