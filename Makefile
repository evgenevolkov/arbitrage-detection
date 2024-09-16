.PHONY: install start_analyzer start_generator build_generator_container \
		start_generator_container stop_generator_container

menu:
	@echo "Select an option:"; \
	select opt in "Start generator" "Start analyzer" "Build generator container" \
				   "Start generator container" "Stop generator container" "Clean" \
				   "Exit"; do \
	    case $$opt in \
	        ("Start generator") make start_generator; break;; \
	        ("Start analyzer") make start_analyzer; break;; \
	        ("Build generator container") make build_generator_container; break;; \
	        ("Start generator container") make start_generator_container; break;; \
	        ("Stop generator container") make stop_generator_container; break;; \
	        ("Clean") make clean; break;; \
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

build_generator_container:
	docker build -t prices_generator:latest -f prices_generator/Dockerfile .

start_generator_container:
	docker rm -f prices_generator || true
	docker run --name prices_generator -p 8000:8000 --env-file prices_generator/.env prices_generator 

stop_generator_container:
	docker stop prices_generator || true

clean:
	docker stop prices_generator || true
	docker rm prices_generator || true
	docker rmi prices_generator:latest || true

docker_prune:
	docker image prune -f || true