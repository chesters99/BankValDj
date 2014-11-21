#

SHELL := /bin/sh
TEXT_COLOR=\x1b[34;01m
COMMAND_COLOR=\x1b[31;01m
NO_COLOR=\x1b[0m

all:
	@echo "$(TEXT_COLOR)"
	@echo "Use Fabric to create and setup amazon ec2 server with the following command"
	@echo "NB: config parameters are set in the /<project>/<project>/amazon_ec2_secret.json file"
	@echo "NB: fabfile.py contains the build steps"
	@echo "$(COMMAND_COLOR)"
	@echo "fab create_server setup_server"
	@echo "$(TEXT_COLOR)"
	@echo ""
	@echo "Once the server is tested and working run the following to clean up install files/logs"
	@echo "$(COMMAND_COLOR)"
	@echo "fab cleanup_files"
	@echo "$(NO_COLOR)"
