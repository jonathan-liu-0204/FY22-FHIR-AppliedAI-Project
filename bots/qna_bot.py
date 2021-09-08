# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
import urllib.parse
import urllib.request
import base64
import json
import re
import time

from botbuilder.ai.qna import QnAMaker, QnAMakerEndpoint
from botbuilder.core import ActivityHandler, MessageFactory, TurnContext, CardFactory
from botbuilder.schema import (
    ChannelAccount,
    HeroCard,
    CardAction,
    ActivityTypes,
    Attachment,
    AttachmentData,
    Activity,
    ActionTypes,
)

from config import DefaultConfig


class QnABot(ActivityHandler):
    def __init__(self, config: DefaultConfig):
        self.qna_maker = QnAMaker(
            QnAMakerEndpoint(
                knowledge_base_id=config.QNA_KNOWLEDGEBASE_ID,
                endpoint_key=config.QNA_ENDPOINT_KEY,
                host=config.QNA_ENDPOINT_HOST,
            )
        )

    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await self._send_welcome_message(turn_context)
    
    async def _send_welcome_message(self, turn_context: TurnContext):
        """
        Greet the user and give them instructions on how to interact with the bot.
        :param turn_context:
        :return:
        """
        for member in turn_context.activity.members_added:
            if member.id != turn_context.activity.recipient.id:
                await self._display_options(turn_context)

    async def on_message_activity(self, turn_context: TurnContext):
        if (
            turn_context.activity.attachments
            and len(turn_context.activity.attachments) > 0
        ):
            await self._handle_incoming_attachment(turn_context)
        else:
            await self._handle_outgoing_attachment(turn_context)

        #await self._display_options(turn_context)

    async def _handle_incoming_attachment(self, turn_context: TurnContext):
        """
        Handle attachments uploaded by users. The bot receives an Attachment in an Activity.
        The activity has a List of attachments.
        Not all channels allow users to upload files. Some channels have restrictions
        on file type, size, and other attributes. Consult the documentation for the channel for
        more information. For example Skype's limits are here
        <see ref="https://support.skype.com/en/faq/FA34644/skype-file-sharing-file-types-size-and-time-limits"/>.
        :param turn_context:
        :return:
        """
        for attachment in turn_context.activity.attachments:
            attachment_info = await self._download_attachment_and_write(attachment)
            if "filename" in attachment_info:
                #await turn_context.send_activity(
                #    f"Attachment {attachment_info['filename']} has been received to {attachment_info['local_path']}"
                #)
                await turn_context.send_activity("我們已經收到您的申請表，請稍候...我們正在為您辨識申請表之相關資料...")
                os.system(f"python3 form-recognizer-v2.py {attachment_info['local_path']} -o result.json")
                await turn_context.send_activity("已完成辨識，請您確認下方資料是否正確！")

                with open('result.json') as f:
                    data = json.load(f)
                seg = []
                for i in data['analyzeResult']['readResults'][0]['lines']:
                    seg.append(i['text'])


                str_seg = ' '.join(seg)

                name = str_seg[re.search(r'姓名',str_seg).span()[1]+1:re.search(r'身分證號碼',str_seg).span()[0]-1]
                SocialID = str_seg[re.search(r'身分證號碼',str_seg).span()[1]+1:re.search(r'出生',str_seg).span()[0]-1]
                Birth = str_seg[re.search(r'日期',str_seg).span()[1]+1:re.search(r'被保險人 性別',str_seg).span()[0]-3]
                Gender = str_seg[re.search(r'性別',str_seg).span()[1]+1:re.search(r'婚姻',str_seg).span()[0]-1]
                Marriage = str_seg[re.search(r'婚姻',str_seg).span()[1]+1:re.search(r'年齡',str_seg).span()[0]-1]
                YearsOld = str_seg[re.search(r'年齡',str_seg).span()[1]+1:re.search(r'公司名稱',str_seg).span()[0]-1]
                Company = str_seg[re.search(r'公司名稱',str_seg).span()[1]+1:re.search(r'工作內容',str_seg).span()[0]-1]
                Work = str_seg[re.search(r'工作內容',str_seg).span()[1]+1:re.search(r'職稱',str_seg).span()[0]-1]
                Position = str_seg[re.search(r'職稱',str_seg).span()[1]+1:re.search(r'副業',str_seg).span()[0]-1]
                OtherWork = str_seg[re.search(r'副業',str_seg).span()[1]+1:re.search(r'職業代碼',str_seg).span()[0]-1]
                WorkCode = str_seg[re.search(r'職業代碼',str_seg).span()[1]+1:re.search(r'國籍',str_seg).span()[0]-1]
                Nationality = str_seg[re.search(r'國籍',str_seg).span()[1]+1:re.search(r'外國',str_seg).span()[0]+2]
                Address = str_seg[re.search(r'外國',str_seg).span()[1]+1:re.search(r'※數字0請以の書寫',str_seg).span()[0]-1]
                Email = str_seg[re.search(r'E-MAIL',str_seg).span()[1]+1:re.search(r'電話 住',str_seg).span()[0]-1]
                HomeNum = str_seg[re.search(r'住宅',str_seg).span()[1]+1:re.search(r' 公司:',str_seg).span()[0]]
                CompanyNum = str_seg[re.search(r' 公司:',str_seg).span()[1]:re.search(r' 手機:',str_seg).span()[0]]
                TelNum = str_seg[re.search(r'手機:',str_seg).span()[1]:re.search(r'可免填要保人相',str_seg).span()[0]-10]
                SameData = str_seg[re.search(r'可免填要保人相',str_seg).span()[1]-18:re.search(r'可免填要保人相',str_seg).span()[0]+11]
                HelpEmail = str_seg[re.search(r'人相關欄位',str_seg).span()[1]+9:re.search(r'電子保單',str_seg).span()[0]]
                Paper = str_seg[re.search(r'電子保單',str_seg).span()[1]:re.search(r'保單 要',str_seg).span()[0]+2]
                SecondName = str_seg[re.search(r' 要 姓名 ',str_seg).span()[1]:re.search(r'/統一編號',str_seg).span()[0]]
                SecondSocialID = str_seg[re.search(r'/統一編號',str_seg).span()[1]:re.search(r' /統一編號 ',str_seg).span()[0]+17]
                SecondBirth = str_seg[re.search(r' 代表人姓名 ',str_seg).span()[1]-14:re.search(r' 代表人姓名 ',str_seg).span()[0]+1]
                RepresentName = str_seg[re.search(r' 代表人姓名 ',str_seg).span()[1]:re.search(r' 代表人姓名 ',str_seg).span()[0]+10]
                RepresentSocialID = str_seg[re.search(r'日 保 身分證號碼',str_seg).span()[1]:re.search(r'日 保 身分證號碼',str_seg).span()[0]+20]
                SecondAddress = str_seg[re.search(r'日 保 身分證號碼',str_seg).span()[1]+12:re.search(r'人 地址 關係',str_seg).span()[0]]
                Relationship =  str_seg[re.search(r'人 地址 關係',str_seg).span()[1]:re.search(r'人 地址 關係',str_seg).span()[0]+10]
                SecondHomeNum =  str_seg[re.search(r'人 地址 關係',str_seg).span()[1]+10:re.search(r'人 地址 關係',str_seg).span()[0]+25]
                SecondCompanyNum = str_seg[re.search(r'人 地址 關係',str_seg).span()[1]+22:re.search(r'人 地址 關係',str_seg).span()[0]+45]
                SecondTelNum = str_seg[re.search(r'人 地址 關係',str_seg).span()[1]+41:re.search(r'人 地址 關係',str_seg).span()[0]+58]
                PayPerson = str_seg[re.search(r' 付款人 ',str_seg).span()[1]:re.search(r'保險期間 自',str_seg).span()[0]-3]
                StartFrom = str_seg[re.search(r'保險期間 自',str_seg).span()[1]:re.search(r'零時起',str_seg).span()[0]]
                ThisPay = str_seg[re.search(r' 本 期: ',str_seg).span()[1]:re.search(r' 續 期:',str_seg).span()[0]]
                NextPay = str_seg[re.search(r' 續 期:',str_seg).span()[1]:re.search(r'未勾選視同本期繳費方式',str_seg).span()[0]-1]
                Continue = str_seg[re.search(r'效力。 自動續約附加條款',str_seg).span()[1]:re.search(r'防疫保障主',str_seg).span()[0]]
                TotalMoney = str_seg[re.search(r'合計總保險費',str_seg).span()[1]+5:re.search(r'合計總保險費',str_seg).span()[0]+18]

                await turn_context.send_activity(f"被保人姓名：{name}  \n 被保人身分證號碼：{SocialID}  \n 被保人出生日期：{Birth}  \n 被保人婚姻狀況：{Marriage}  \n 被保人年齡：{YearsOld}  \n 被保人公司名稱：{Company}  \n 被保人工作內容：{Work}  \n 被保人職稱：{Position}  \n 被保人副業：{OtherWork}  \n 被保人工作代碼：{WorkCode}  \n 被保人國籍：{Nationality}  \n 被保人住所地址：{Address}  \n 被保人Email：{Email}  \n 被保人住宅電話：{HomeNum}  \n 被保人公司電話：{CompanyNum}  \n 被保人手機號碼：{TelNum}  \n 是否維持電子保單：{Paper}  \n 要保人資訊同被保人資訊：{SameData}  \n 要保人姓名：{SecondName}  \n 要保人Email：{HelpEmail}  \n 要保人身分證字號：{SecondSocialID}  \n 要保人生日：{SecondBirth}  \n 要保人地址：{SecondAddress}  \n 要保人與被保人關係：{Relationship}  \n 要保人住宅電話：{SecondHomeNum}  \n 要保人公司電話：{SecondCompanyNum}  \n 要保人手機：{SecondTelNum}  \n 代表人姓名：{RepresentName}  \n 代表人身分證字號：{RepresentSocialID}  \n 付款人：{PayPerson}  \n 保險期間：{StartFrom}  \n 本期付款方式：{ThisPay}  \n 續期付款方式：{NextPay}  \n 自動續約：{Continue}  \n 保險總金額：{TotalMoney}")

                await turn_context.send_activity("若確認無誤，請輸入「y」，若有誤請輸入「n」，謝謝！")
                
    
    async def _download_attachment_and_write(self, attachment: Attachment) -> dict:
        """
        Retrieve the attachment via the attachment's contentUrl.
        :param attachment:
        :return: Dict: keys "filename", "local_path"
        """
        try:
            response = urllib.request.urlopen(attachment.content_url)
            headers = response.info()

            # If user uploads JSON file, this prevents it from being written as
            # "{"type":"Buffer","data":[123,13,10,32,32,34,108..."
            if headers["content-type"] == "application/json":
                data = bytes(json.load(response)["data"])
            else:
                data = response.read()

            local_filename = os.path.join(os.getcwd() + "/uploads/" , attachment.name)
            with open(local_filename, "wb") as out_file:
                out_file.write(data)

            return {"filename": attachment.name, "local_path": local_filename}
        except Exception as exception:
            print(exception)
            return {}

    async def _handle_outgoing_attachment(self, turn_context: TurnContext):
        reply = Activity(type=ActivityTypes.message)

        first_char = turn_context.activity.text[0]
        if first_char == "1":
            reply.text = "請您填寫下方申請表後回傳，謝謝您！"
            reply.attachments = [self._get_inline_attachment()]
        elif first_char == "2":
            reply.text = "您好！很高興為您服務！  \n\n 以下為相關作業流程： \n 1. 若確認投保，請您點選第一個選項「1. 線上投保疫苗險」，我們將會提供您疫苗險之申請表  \n 2. 將申請表單填寫完成後，請您將申請表直接回傳  \n 3. 系統將會辨識您回傳之申請表，將其資料擷取後回傳供您做確認  \n 4. 若確認無誤，我們將會將您的保險申請表登錄至系統，並且為您安排一位保險專員，供您日後做聯絡；若資料有誤，我們將會為您安排相關專員，協助您做資料上的修正  \n\n  以上為線上投保之申請流程，期待您的回覆，謝謝您！  \n\n 備註｜  \n 您若想要瞭解更多微軟產物保險之其他產品，請點選「3. 瞭解更多微軟產物保險之其他產品」"
        elif first_char == "3":
            reply.text = "您好！很高興為您服務！  \n\n 目前微軟產物保險除了疫苗險，我們還有許多其他產品供您做參考，詳細資訊如下：  \n\n 人身保險  \n - 人壽保險：生存險、死亡險、生死合險  \n - 年金保險  \n - 健康保險：醫療險、重大傷（疾）病險、癌症險、長期照顧險、失能險  \n - 傷害保險：意外傷害險  \n - 投資型保險：變額壽險、變額萬能壽險、變額年金保險  \n\n 財產保險 \n - 汽機車保險：汽機車強制險、車體損失險、第三人責任險、超額責任險  \n - 旅遊保險：旅遊平安險、旅遊不便險  \n - 責任保險：產品責任保險、公共意外責任保險  \n - 住宅保險：住宅火險、地震險  \n - 其他：海上保險、農作物保險、寵物險、手機險、戶外活動保險  \n\n 以上為我們其他保險產品，由於目前只有疫苗險能以線上申請的方式進行投保，若您希望可以針對其他產品做進一步瞭解，請您撥打我們的免付費客服電話，我們將有專人為您進行詳細的解說，謝謝！  \n\n  微軟免付費客服電話：00801-128-000  \n" 
        elif first_char == "y":
            reply.text = "謝謝您！我們已將您的保險申請表登錄至系統中！  \n 您的保險專員為：  \n - 專員姓名：Eric Wang  \n - 員工代碼：200  \n - 公司電話：00801-128-000 分機：8924  \n - 手機號碼：0912-345-678  \n\n 接下來若有任何疑問或是相關需求，歡迎直接聯絡您的保險專員，謝謝您，很高興為您服務！  \n"
        elif first_char == "n":
            reply.text = "很抱歉造成您的困擾！我們將儘速協助您更正您的資料！  \n 您的保險專員為：  \n - 專員姓名：Johnny Liu  \n - 員工代碼：404  \n - 公司電話：00801-128-000 分機：6853  \n - 手機號碼：0987-654-321  \n\n 接下來若有任何疑問或是相關需求，歡迎直接聯絡您的保險專員，謝謝您，很高興為您服務！  \n"
        else:
            reply.text = "不好意思！我不是很懂您的意思，請您重新選擇或是輸入，我們會盡全力協助您，謝謝！"

        await turn_context.send_activity(reply)
        await self._display_options(turn_context)

    async def _display_options(self, turn_context: TurnContext):
        """
        Create a HeroCard with options for the user to interact with the bot.
        :param turn_context:
        :return:
        """

        # Note that some channels require different values to be used in order to get buttons to display text.
        # In this code the emulator is accounted for with the 'title' parameter, but in other channels you may
        # need to provide a value for other parameters like 'text' or 'displayText'.
        card = HeroCard(
            text="您好, 我是微軟產物保險數位投保智能客服, 請問我可以怎麼協助您？",
            buttons=[
                CardAction(
                    type=ActionTypes.im_back, title="1. 線上投保疫苗險", value="1"
                ),
                CardAction(
                    type=ActionTypes.im_back, title="2. 瞭解線上投保疫苗險之相關作業流程", value="2"
                ),
                CardAction(
                    type=ActionTypes.im_back, title="3. 瞭解更多微軟產物保險之其他產品", value="3"
                ),
            ],
        )

        reply = MessageFactory.attachment(CardFactory.hero_card(card))
        await turn_context.send_activity(reply)

    
    
    def _get_inline_attachment(self) -> Attachment:
        """
        Creates an inline attachment sent from the bot to the user using a base64 string.
        Using a base64 string to send an attachment will not work on all channels.
        Additionally, some channels will only allow certain file types to be sent this way.
        For example a .png file may work but a .pdf file may not on some channels.
        Please consult the channel documentation for specifics.
        :return: Attachment
        """
        file_path = os.path.join(os.getcwd(), "resources/vaccine-insurance-form.jpg")
        with open(file_path, "rb") as in_file:
            base64_image = base64.b64encode(in_file.read()).decode()

        return Attachment(
            name="vaccine-insurance-form.jpg",
            content_type="image/jpeg",
            content_url=f"data:image/jpeg;base64,{base64_image}",
        )
    
    async def _get_upload_attachment(self, turn_context: TurnContext) -> Attachment:
        """
        Creates an "Attachment" to be sent from the bot to the user from an uploaded file.
        :param turn_context:
        :return: Attachment
        """
        with open(
            os.path.join(os.getcwd(), "resources/architecture-resize.png"), "rb"
        ) as in_file:
            image_data = in_file.read()

        connector = await turn_context.adapter.create_connector_client(
            turn_context.activity.service_url
        )
        conversation_id = turn_context.activity.conversation.id
        response = await connector.conversations.upload_attachment(
            conversation_id,
            AttachmentData(
                name="architecture-resize.png",
                original_base64=image_data,
                type="image/png",
            ),
        )

        base_uri: str = connector.config.base_url
        attachment_uri = (
            base_uri
            + ("" if base_uri.endswith("/") else "/")
            + f"v3/attachments/{response.id}/views/original"
        )

        return Attachment(
            name="architecture-resize.png",
            content_type="image/png",
            content_url=attachment_uri,
        )
    


