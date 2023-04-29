from __future__ import annotations

import colorlog


handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
	"%(log_color)s%(asctime)-15s %(levelname)-8s %(message)s",
	datefmt=None,
	reset=True,
	log_colors={
		'DEBUG':    'cyan',
		'INFO':     'green',
		'WARNING':  'yellow',
		'ERROR':    'red',
		'CRITICAL': 'red,bg_white',
	}))

logger = colorlog.getLogger(__name__)
logger.setLevel(colorlog.INFO)
logger.addHandler(handler)