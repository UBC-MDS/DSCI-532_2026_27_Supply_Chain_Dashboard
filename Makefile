.PHONY: test install

install:
	pip install -r requirements.txt
	playwright install chromium

test:
	# Run shiny in the background, wait 3 seconds for it to boot, 
	# then run pytest. The 'kill' ensures the app closes after.
	shiny run src/app.py --port 8000 & \
	sleep 3 && \
	pytest; \
	EXIT_CODE=$$?; \
	pkill -f "shiny run" || true; \
	exit $$EXIT_CODE