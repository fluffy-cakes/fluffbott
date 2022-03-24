from slack_bolt                     import Ack, App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk                      import WebClient
from slack_sdk.web                  import SlackResponse
import logging
import os
import re


# logging.basicConfig(level=logging.DEBUG) # enable this if you want a good debug readout whilst developing
app = App(token = os.environ.get("SLACK_BOT_TOKEN"))



@app.action({"type": "workflow_step_edit", "callback_id": "annoyGroup"})
def edit(body: dict, ack: Ack, client: WebClient):
    ack()

    new_modal: SlackResponse = client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "workflow_step",
            "callback_id": "annoyGroup_view",
            "blocks": [
                {
                    "type": "section",
                    "block_id": "intro-section",
                    "text": {
                        "type": "plain_text",
                        "text": "Select the channel you want to annoy, and then select the world \"Tribe\" channel you only want to include.",
                    },
                },
                {
                    "type": "input",
                    "block_id": "channel_name_input",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "channel_name",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Write a channel name to annoy.",
                        },
                    },
                    "label": {"type": "plain_text", "text": "Channel name"},
                },
                {
                    "type": "input",
                    "block_id": "tribe_include_input",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "tribe_include",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Write a world tribe to include.",
                        },
                    },
                    "label": {"type": "plain_text", "text": "Tribe include"},
                },
            ],
        },
    )



@app.view("annoyGroup_view")
def save(ack: Ack, client: WebClient, body: dict):
    state_values = body["view"]["state"]["values"]

    response: SlackResponse = client.api_call(
        api_method="workflows.updateStep",
        json={
            "workflow_step_edit_id": body["workflow_step"]["workflow_step_edit_id"],
            "inputs": {
                "channelName": {
                    "value": state_values["channel_name_input"]["channel_name"]["value"],
                },
                "tribeInclude": {
                    "value": state_values["tribe_include_input"]["tribe_include"][
                        "value"
                    ],
                },
            },
            "outputs": [
                {
                    "name": "channelName",
                    "type": "text",
                    "label": "Channel Name",
                },
                {
                    "name": "tribeInclude",
                    "type": "text",
                    "label": "Tribe Include",
                },
            ],
        },
    )
    ack()



@app.event("workflow_step_execute")
def execute(body: dict):
    channel  = body["event"]["workflow_step"]["inputs"]["channelName"]["value"]
    tribe    = body["event"]["workflow_step"]["inputs"]["tribeInclude"]["value"]
    userList = []


    print(f"Channel name is \"{channel}\"")
    print(f"Tribe to include is \"{tribe}\"")


    for i in app.client.conversations_list().data["channels"]:
        if i["name"] == channel:
            channelId = i["id"]
            print(f"Spam channel is \"{channelId}\"")


    for i in app.client.conversations_list().data["channels"]:
        if i["name"] == tribe:
            channelTribe = i["id"]
            print(f"Tribe channel is \"{channelTribe}\"")


    for i in app.client.conversations_members(channel = channelId).data["members"]:
        if i in app.client.conversations_members(channel = channelTribe).data["members"]:
            user = app.client.users_info(user = i).data["user"]
            if user["is_bot"] == False:
                userList.append(i)
                userName = user["name"]
                print(f"Appending user \"{userName}\"")


    print("UserList is:")
    print(userList)


    for i in userList:
        print(f"Sending annoying message to {app.client.users_info(user = i).data['user']['name']}")


        app.client.chat_postMessage(
            channel = i,
            text    = "Watchya doin'?",
            blocks  =  [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"Hello <@{i}>!\n The {channel} channel is curious what you're currently working on?"
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "input",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "workingInputText",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "What you sayin'?"
                        }
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Today I'm working on...",
                        "emoji": True
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": f"POST to \"{channel}\"",
                                "emoji": True
                            },
                            "style": "primary",
                            "value": "SUBMIT",
                            "action_id": "workingInputButton"
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "GO AWAY!",
                                "emoji": True
                            },
                            "style": "danger",
                            "value": "SUBMIT",
                            "action_id": "goAwayButton"
                        }
                    ]
                }
            ]
        )



@app.event("message")
def handle_message_events(body, logger):
    logger.info(body)



@app.action("workingInputButton")
def update_modal(ack, body):
    ack()

    for i in body["actions"]:
        if i["action_id"] == "workingInputButton":
            channel = re.search('"(.+)"', i["text"]["text"]).group(1)

    for i in app.client.conversations_list().data["channels"]:
        if i["name"] == channel:
            channelId = i["id"]

    for i in body["message"]["blocks"]:
        if "element" in i:
            user = body["user"]["name"]

            if i["element"]["action_id"] == "workingInputText":
                blockId   = i["block_id"]
                userInput = body["state"]["values"][blockId]["workingInputText"]["value"]

                print(f"{user} has replied with \"{userInput}\" to channel \"{channel}\"")

                app.client.chat_update(
                    channel = body["channel"]["id"],
                    ts      = body["message"]["ts"],
                    text    = "Thanks :smile:",
                    blocks  = [
                        {
                            "type": "header",
                            "text": {
                                "type": "plain_text",
                                "text": "Thanks!",
                                "emoji": True
                            }
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"You're currently working on:\n\t\t\"_{userInput}_\"\n"
                            }
                        }
                    ]
                )

            app.client.chat_postMessage(
                channel = channelId,
                text    = f"<@{user}> is currently working on...",
                blocks = [
                    {
                        "type": "section",
                        "text": {
                            "type": "plain_text",
                            "text": f"<@{user}> is currently working on:",
                            "emoji": True
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"\"_{userInput}_\"\n\n\t\t:eyes: ~ if you want to know more"
                        }
                    }
                ]
            )



@app.action("goAwayButton")
def update_modal(ack, body):
    ack()
    print(f"{body['user']['name']} told me to go Go Away!")

    app.client.chat_update(
        channel = body["channel"]["id"],
        ts      = body["message"]["ts"],
        text    = "Sorry :disappointed:",
        blocks  = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Ah well, I gave it a try...\n\t\t`¯\\_(ツ)_/¯`"
                }
            }
        ]
    )



if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
