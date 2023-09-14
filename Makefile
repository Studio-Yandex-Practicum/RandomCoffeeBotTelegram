.SILENT:

COLOR_RESET = \033[0m
COLOR_GREEN = \033[32m
COLOR_YELLOW = \033[33m
COLOR_WHITE = \033[00m

.DEFAULT_GOAL := help


.PHONY: help
help:  # Show help
	@echo -e "$(COLOR_GREEN)Makefile help:"
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "$(COLOR_GREEN)-$$(echo $$l | cut -f 1 -d':'):$(COLOR_WHITE)$$(echo $$l | cut -f 2- -d'#')\n"; done


.PHONY: runbot
runbot: # Run Telegram bot on Uvicorn
	@echo -e "$(COLOR_YELLOW)Starting bot...$(COLOR_RESET)"
	@cd src && poetry run uvicorn core.asgi:application --reload && cd .. && \
	echo -e "$(COLOR_GREEN)Bot stopped$(COLOR_RESET)"
