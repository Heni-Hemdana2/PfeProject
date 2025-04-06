DB_NAME ?= PFE_DB
SCRIPT_PATH := $(shell pwd)/bootstrap_db.sql
POSTGRES_PATH :=  /var/lib/postgresql/bootstrap_db.sql


bootstrap-db:
	@echo "Creating database $(DB_NAME)..."
	sudo -u postgres psql -c "DROP DATABASE IF EXISTS \"$(DB_NAME)\";"
	sudo -u postgres psql -c "CREATE DATABASE \"$(DB_NAME)\";"

backup-db: bootstrap-db
	@echo "Creating database $(DB_NAME)..."
	sudo -u postgres psql -c "DROP DATABASE IF EXISTS \"$(DB_NAME)\";"
	sudo -u postgres psql -c "CREATE DATABASE \"$(DB_NAME)\";"
	@echo "Populating the schema..."
	@echo "Changing owner | Script : $(SCRIPT_PATH)"
	sudo chown postgres:postgres $(SCRIPT_PATH)
	sudo cp $(SCRIPT_PATH) $(POSTGRES_PATH)
	sudo -u postgres psql -d $(DB_NAME) -f $(POSTGRES_PATH)
	@echo "Database $(DB_NAME) created and populated successfully."

conda-env:
	conda env create -f conda.yaml
