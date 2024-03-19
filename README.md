## to Build the image
$ docker-compose build aiupgrader

The container creates 2 directories, 1) /ai and 2) /repo
/ai maps to the current folder, which is the where the upgrade.py script is located
/repo maps to the target source code repository containing the .js files

## Setup
# OpenAI Assistant
You will need to create an OpenAI API account and create an assistant accordingly.
The assistant can be modified to fit the needs of the conversion.

# .env file
You need to create a local .env file in the root of the repository with the following content:
```
OPENAI_API_KEY="your api key"
OPENAI_ORGANIZATION="your organization id"
OPENAI_ASSISTANT_ID="your assistant id"
```

## to Start the container
$ REPO=/PATH/TO/TARGET_REPO docker-compose run --rm aiupgrader

## in the container
Note that the converted file will be generated and stored in the same directory
where the original files are.

# See the arguments for the upgrade.py script
$ upgrade.py --help

# Run the upgrade.py script as any command
$ upgrade.py -c /path/to/code.js -t /path/to/test.spec.js

# Run the upgrade.py without test file
$ upgrade.py -c /path/to/code.js

