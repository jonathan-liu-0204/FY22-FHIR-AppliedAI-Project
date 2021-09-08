#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = "3978"
    APP_ID = os.environ.get("MicrosoftAppId", "5b48ed61-59a2-4a8c-a5be-985483e103a4")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "f8553227-2c54-45ba-ae28-5810e435053b")
    QNA_KNOWLEDGEBASE_ID = os.environ.get("QnAKnowledgebaseId", "f1761c11-86bf-4e80-b158-6a9fef86fb62")
    QNA_ENDPOINT_KEY = os.environ.get("QnAEndpointKey", "21f9eeb7-3334-4f33-ade0-500f470b8f61")
    QNA_ENDPOINT_HOST = os.environ.get("QnAEndpointHostName", "https://0831-fy22-fhir-appliedai-project-v2.azurewebsites.net/qnamaker")
