# workspace-auto-translator

# Setup

## Install GCloud

Go to the [GCloud Installation Page](https://cloud.google.com/sdk/docs/install) and follow the instructions to install the Google Cloud SDK.

## Create a Google Cloud Project

Go to the [Google Cloud Console](https://console.cloud.google.com/) and create a new project, note the project name.

```sh
export project_name="your-project-name"
```

## Create Credentials

### Client Secrets

- Go to the [Google Cloud Console](https://console.cloud.google.com/).
- Navigate to the **APIs & Services** -> **Credentials** page.
- Create a new OAuth 2.0 Client ID, application type **Desktop App**.
- Download the client secrets file, and save it as **secret/client_secrets.json**.

### Service Account

- Go to the [Google Cloud Console](https://console.cloud.google.com/)
- Navigate to the **IAM & Admin** -> **Service Accounts** page.
- Create a new service account, and download the JSON key file.
- Save the JSON key file as **secret/service_account.json**.


## Authenticate

This should open a browser window to authenticate with your Google account.

```sh
gcloud auth login
gcloud auth application-default login
```

## Enable APIs

```sh
gcloud config set project $project_name
gcloud services enable chat.googleapis.com pubsub.googleapis.com workspaceevents.googleapis.com
```

## Create PubSub Topic and Subscription

```sh
export topic_id="workspace-topic"
export topic_name="projects/$project_name/topics/$topic_id"
export subscription_id="workspace-subscription"

gcloud pubsub topics create $topic_id
gcloud pubsub topics add-iam-policy-binding $topic_name --member='serviceAccount:chat-api-push@system.gserviceaccount.com' --role='roles/pubsub.publisher'
gcloud pubsub subscriptions create $subscription_id --topic=$topic_name
```

## Configure Google Chat API

- Go to the [Google Chat API](https://console.cloud.google.com/apis/api/chat.googleapis.com) page.
- Go to Configuration tab.
- Fill in the **App name**, **Avatar URL**, and **Description**.
- Click **Enable Interactive Features**, check **Receive 1:1 messages** and **Join spaces and group conversations**
- For Connection Settings, choose **Cloud Pub/Sub** and **Cloud Pub/Sub Topic Name**
- Tick **Make this Chat app available to specific people and groups in Global Fashion Group**, and add your email.

# Start the Server

## Normal Start

Go to root directory of the project and run the following commands:

```sh
export PYTHONPATH="$(pwd):$PYTHONPATH"
python app/main.py
```

The application should prompt you to authenticate with your Google account.

## Start with Passphrase

If you want to hide your token on a shared machine, you can use a passphrase to encrypt the token. Add a leading space to the command to prevent it from being saved in the history.

```sh
 PASSPHRASE="your-passphrase" python app/main.py
```

If it still shows up in the history, try `HISTCONTROL=ignorespace` and re-run the command.