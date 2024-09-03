.PHONY: install start_analyzer start_generator

menu:
	@echo "Select an option:"; \
	select opt in "Start analyzer" "Start generator" "Exit"; do \
	    case $$opt in \
	        ("Start generator") make start_generator; break;; \
	        ("Start analyzer") make start_analyzer; break;; \
	        ("Exit") exit;; \
	        (*) echo "Invalid option";; \
	    esac; \
	done


install:
	python3 -m venv .venv
	./.venv/bin/pip install -r requirements.txt
	@mv prices_analyzer/.env.example prices_analyzer/.env
	@mv prices_generator/.env.example prices_generator/.env
 
start_analyzer:
	cd prices_analyzer && ../.venv/bin/python -m app.app

start_generator:
	cd prices_generator && ../.venv/bin/uvicorn app.app:app --reload