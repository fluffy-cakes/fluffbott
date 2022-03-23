## Install Requirements

#### Create Docker container for testing app

```bash
docker run \
    --name app \
    --cap-add NET_ADMIN \
    --detach \
    --net host \
    --restart unless-stopped \
    -it \
    -v '/mnt/d/OneDrive/GitHub-me':/root/scrapbook \
    ubuntu:20.04
```


#### Install software requirements

```bash
apt-get update
apt-get install -y \
    python3 \
    python3-pip

pip3 install slack_bolt
```


#### Export tokens for use in app

```bash
export SLACK_BOT_TOKEN="asdf"
export SLACK_APP_TOKEN="asdf"
```


#### Test Dockerfile once created image

```bash
docker run \
    --detach \
    --name asdf \
    --net host \
    -e SLACK_APP_TOKEN='asdf' \
    -e SLACK_BOT_TOKEN='asdf' \
    asdf
```


## Handy Links
- https://api.slack.com/bolt
- https://api.slack.com/apps
- https://app.slack.com/block-kit-builder/
- https://slack.dev/bolt-python/tutorial/getting-started
    - https://api.slack.com/apps/A02UDT4MAG4/oauth?
    - https://api.slack.com/apps/A02UDT4MAG4/event-subscriptions?


## Bot Token Scopes
*Scopes that govern what your app can access.*

`channels:history`
View messages and other content in public channels that ASDFbot has been added to

`channels:read`
View basic information about public channels in a workspace

`chat:write`
Send messages as @asdf

`groups:history`
View messages and other content in private channels that ASDFbot has been added to

`im:history`
View messages and other content in direct messages that ASDFbot has been added to

`mpim:history`
View messages and other content in group direct messages that ASDFbot has been added to

`users:read`
View people in a workspace

`workflow.steps:execute`
Add steps that people can use in Workflow Builder

---

## Subscribe to bot events
*Apps can subscribe to receive events the bot user has access to (like new messages in a channel). If you add an event here, we’ll add the necessary OAuth scope for you.*

`message.channels`
A message was posted to a channel
Required scope: `channels:history`

`message.groups`
A message was posted to a private channel
Required scope: `groups:history`

`message.im`
A message was posted in a direct message channel
Required scope: `im:history`

`workflow_step_execute`
A workflow step supported by your app should execute
Required scope: `workflow.steps:execute`