# ChatWars Database

[![Build status](https://dev.azure.com/ricardobchaves/Ricardo/_apis/build/status/chat-wars-database/chat-wars-database)](https://dev.azure.com/ricardobchaves/Ricardo/_build/latest?definitionId=23) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/7b22103a3e4e4776983d692219add41d)](https://www.codacy.com/manual/ricardochaves/chat-wars-database?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ricardochaves/chat-wars-database&amp;utm_campaign=Badge_Grade) [![Codacy Badge](https://api.codacy.com/project/badge/Coverage/7b22103a3e4e4776983d692219add41d)](https://www.codacy.com/manual/ricardochaves/chat-wars-database?utm_source=github.com&utm_medium=referral&utm_content=ricardochaves/chat-wars-database&utm_campaign=Badge_Coverage) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![GitHub](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/ricardochaves/chat-wars-database/blob/master/LICENSE)

## Command List for BotFather

/help - What can I do

## Data extraction

There is a Django command that extracts all messages from Telegram channels.

### Auction

All lots found with finalized status are included in the database.

### Exchange

IN PROGRESS

### WARNING

To perform the extraction you need a telegram app that is created at the following [link](https://my.telegram.org/apps).
With the data from this app you need to run [login.py](login.py) and it will print your connection string, it must be placed in the `TELEGRAM_STRING` environment variable to work.
> Beware of this string, it gives you access to absolutely everything in your account. I advise having a telegram account just for it, I did it. My personal account is not used to do the extraction.

## Running

The whole project runs with Docker

### Login

This is only necessary if you really want to extract data from the channel.

```bash
docker-compose run --rm web python login.py
```

Result:

```bash
Starting chat-wars-database_db_1 ... done
Please enter your phone (or bot token): YOUR_PHONE_NUMBER(+5511555555555)
Please enter the code you received: YOU_WILL_RECEIVE_ON_TELEGRAM
Please enter your password: YOUR_TELEGRAM_PASS
Signed in successfully as YOUR_NAME
YOUR_ACCESS_STRING
```

Set up a `.env` file in the project root. Use for example [.env_integration_tests](.env_integration_tests) as an example

### Items

There is a list of items in a command to load an initial database.

```bash
docker-compose run --rm web python manage.py seed_db
```

### Telegram Bot

The @CharWarsDataBaseBot bot runs with the command:

```bash
docker-compose run --rm web python manage.py game_bot
```

When a chart is requested, it sends a message to Gcloud's [PubSub](https://cloud.google.com/pubsub/docs/)

Another command is required to receive these messages, create the graph and send the result.

```bash
docker-compose run --rm web python manage.py game_bot_pubsub_consumer
```

### Web

The web version runs as a simple Django:

```bash
docker-compose up web
```

## Tests

```bash
docker-compose -f docker-compose-tests.yml up integration-tests
```


## License

The scripts and documentation in this project are released under the [MIT License](LICENSE)

## Contributions

Contributions are welcome! See [Contributor's Guide](docs/contributors.md)