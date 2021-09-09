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