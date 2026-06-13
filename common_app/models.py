from django.db import models
from django.utils import timezone

class Language(models.Model):
    lgId = models.BigAutoField(primary_key=True, db_column='lg_id')
    lgDisOrder = models.BigIntegerField(null=True, blank=True, db_column='lg_dis_order')
    lgLongName = models.CharField(max_length=255, null=True, blank=True, db_column='lg_long_name')
    lgName = models.CharField(max_length=255, null=True, blank=True, db_column='lg_name')

    class Meta:
        managed = False
        db_table = 'tbl_language'

class SecurityQuestion(models.Model):
    secId = models.BigAutoField(primary_key=True, db_column='sec_id')
    secQuestion = models.CharField(max_length=255, null=True, blank=True, db_column='sec_question')

    class Meta:
        managed = False
        db_table = 'tbl_security_question'

class Country(models.Model):
    id = models.AutoField(primary_key=True)
    cntCode = models.CharField(max_length=255, null=True, blank=True, db_column='cnt_code')
    cntName = models.CharField(max_length=80, db_column='cntName')
    iso2 = models.CharField(max_length=2, null=True, blank=True, db_column='iso2')
    longName = models.CharField(max_length=80, db_column='long_name')
    oid = models.IntegerField(null=True, blank=True)
    phoneMinLength = models.IntegerField(db_column='phone_min_length')
    phoneMaxLength = models.IntegerField(db_column='phone_max_length')

    class Meta:
        managed = False
        db_table = 'tbl_country'

class CountryToState(models.Model):
    countryToStateId = models.BigAutoField(primary_key=True, db_column='country_to_state_id')
    fkCountryId = models.BigIntegerField(db_column='fk_country_id')
    stateCapital = models.CharField(max_length=100, null=True, blank=True, db_column='state_capital')
    stateLong = models.CharField(max_length=100, null=True, blank=True, db_column='state_long')
    stateShort = models.CharField(max_length=10, null=True, blank=True, db_column='state_short')

    class Meta:
        managed = False
        db_table = 'country_to_state'

class Member(models.Model):
    memberId = models.BigAutoField(primary_key=True, db_column='Member_Id')
    membershipType = models.CharField(max_length=255, null=True, blank=True, db_column='membership_type')
    password = models.CharField(max_length=255, null=True, blank=True, db_column='Password')
    companyName = models.CharField(max_length=255, null=True, blank=True, db_column='company_name')
    firstName = models.CharField(max_length=255, null=True, blank=True, db_column='First_Name')
    lastName = models.CharField(max_length=255, null=True, blank=True, db_column='Last_Name')
    address = models.CharField(max_length=255, null=True, blank=True, db_column='Address')
    streetAddress = models.TextField(null=True, blank=True, db_column='street_address')
    city = models.CharField(max_length=255, null=True, blank=True, db_column='City')
    state = models.CharField(max_length=255, null=True, blank=True, db_column='State')
    postCode = models.CharField(max_length=255, null=True, blank=True, db_column='Post_Code')
    country = models.CharField(max_length=255, null=True, blank=True, db_column='Country')
    phone = models.CharField(max_length=255, null=True, blank=True, db_column='Phone')
    fax = models.CharField(max_length=255, null=True, blank=True, db_column='Fax')
    cell = models.CharField(max_length=255, null=True, blank=True, db_column='Cell')
    email = models.CharField(max_length=255, null=True, blank=True, db_column='Email')
    memberStatus = models.IntegerField(default=1, db_column='member_status')
    businessName = models.CharField(max_length=255, null=True, blank=True, db_column='business_Name')
    websiteName = models.CharField(max_length=255, null=True, blank=True, db_column='website_Name')
    newsletterSubscribe = models.IntegerField(null=True, blank=True, db_column='newsletter_subscribe')
    is2FA = models.IntegerField(default=0, db_column='is2FA')
    twilioNumberPurchaseDt = models.DateTimeField(null=True, blank=True, db_column='twilioNumberPurchaseDt')
    twilioNumberRenewDt = models.DateTimeField(null=True, blank=True, db_column='twilioNumberRenewDt')
    dateRegistered = models.DateTimeField(null=True, blank=True, db_column='Date_Registered')
    lastLoggedin = models.DateTimeField(null=True, blank=True, db_column='Last_Loggedin')
    campEmailServers = models.CharField(max_length=255, null=True, blank=True, db_column='camp_email_servers')
    publicWebAdd = models.CharField(max_length=255, null=True, blank=True, db_column='public_web_add')
    pusername = models.CharField(max_length=255, null=True, blank=True, db_column='pusername')
    ppassword = models.CharField(max_length=255, null=True, blank=True, db_column='ppassword')
    paypalTransactionid = models.CharField(max_length=255, null=True, blank=True, db_column='paypal_transactionid')
    usedPlanId = models.CharField(max_length=255, null=True, blank=True, db_column='Used_plan_id')
    authorizeCustomerPaymentProfileId = models.CharField(max_length=255, null=True, blank=True, db_column='authorizeCustomerPaymentProfileId')
    authorizeCustomerProfileId = models.CharField(max_length=255, null=True, blank=True, db_column='authorizeCustomerProfileId')
    betacode = models.CharField(max_length=255, null=True, blank=True, db_column='betacode')
    betalimit = models.IntegerField(null=True, blank=True, db_column='betalimit')
    billDate = models.DateField(null=True, blank=True, db_column='billDate')
    billDay = models.IntegerField(null=True, blank=True, db_column='billDay')
    ccDeleteRequest = models.CharField(max_length=1, default='N', db_column='cc_delete_request')
    memberDefaultLanguage = models.CharField(max_length=255, default='en', db_column='member_default_language')
    optin = models.CharField(max_length=1, null=True, blank=True, db_column='optin')
    parentMemberId = models.BigIntegerField(default=0, db_column='parent_member_id')
    performance = models.IntegerField(default=1, db_column='performance')
    planMonthlyYn = models.CharField(max_length=1, default='N', db_column='plan_monthly_yn')
    promotionEAS = models.IntegerField(default=1, db_column='promotionEAS')
    secAns1 = models.CharField(max_length=255, null=True, blank=True, db_column='sec_ans_1')
    secAns2 = models.CharField(max_length=255, null=True, blank=True, db_column='sec_ans_2')
    secAns3 = models.CharField(max_length=255, null=True, blank=True, db_column='sec_ans_3')
    secQus1 = models.IntegerField(default=0, db_column='sec_qus_1')
    secQus2 = models.IntegerField(default=0, db_column='sec_qus_2')
    secQus3 = models.IntegerField(default=0, db_column='sec_qus_3')
    shopifyStoreName = models.CharField(max_length=255, null=True, blank=True, db_column='shopify_store_name')
    shopifyStoreToken = models.CharField(max_length=255, null=True, blank=True, db_column='shopify_store_token')
    smFbAccessToken = models.TextField(null=True, blank=True, db_column='sm_fb_accessToken')
    smFbId = models.CharField(max_length=255, null=True, blank=True, db_column='sm_fb_id')
    smLinAuthToken = models.TextField(null=True, blank=True, db_column='sm_lin_authToken')
    smLinExpiresAt = models.CharField(max_length=255, null=True, blank=True, db_column='sm_lin_expiresAt')
    smTwOauthToken = models.CharField(max_length=255, null=True, blank=True, db_column='sm_tw_oauthToken')
    smTwOauthTokenSecret = models.CharField(max_length=255, null=True, blank=True, db_column='sm_tw_oauthTokenSecret')
    smsConversationYn = models.CharField(max_length=1, default='N', db_column='sms_conversation_yn')
    smsCvrMyphoneYn = models.CharField(max_length=1, default='Y', db_column='sms_cvr_myphone_yn')
    subaccountTypeId = models.BigIntegerField(default=0, db_column='subaccount_type_id')
    subAccountAuthToken = models.CharField(max_length=255, null=True, blank=True, db_column='subAccountAuthToken')
    subAccountPhoneSId = models.CharField(max_length=255, null=True, blank=True, db_column='subAccountPhoneSId')
    subAccountSId = models.CharField(max_length=255, null=True, blank=True, db_column='subAccountSId')
    subFriendlyName = models.CharField(max_length=255, null=True, blank=True, db_column='subFriendlyName')
    totalEmailLimit = models.IntegerField(null=True, blank=True, db_column='Total_email_limit')
    totalSubscribeLimit = models.IntegerField(null=True, blank=True, db_column='Total_subscribe_limit')
    totalSurveysLimit = models.IntegerField(null=True, blank=True, db_column='Total_surveys_limit')
    twilioNumber = models.CharField(max_length=255, null=True, blank=True, db_column='twilioNumber')
    updatePromotion = models.IntegerField(default=1, db_column='updatePromotion')
    updateSupport = models.IntegerField(default=1, db_column='updateSupport')
    usedEmailLimit = models.IntegerField(null=True, blank=True, db_column='Used_email_limit')
    usedSubscribeLimit = models.IntegerField(null=True, blank=True, db_column='Used_subscribe_limit')
    usedSurveysLimit = models.IntegerField(null=True, blank=True, db_column='Used_surveys_limit')
    zoomToken = models.TextField(null=True, blank=True, db_column='zoom_token')
    imageUrl = models.CharField(max_length=255, null=True, blank=True, db_column='imageUrl')
    otp = models.CharField(max_length=255, null=True, blank=True, db_column='otp')
    googleCalendarAccessToken = models.TextField(null=True, blank=True, db_column='google_calendar_access_token')
    googleCalendarRefreshToken = models.TextField(null=True, blank=True, db_column='google_calendar_refresh_token')
    googleCalendarSyncTime = models.CharField(max_length=255, null=True, blank=True, db_column='google_calendar_sync_time')
    outlookCalendarAccessToken = models.TextField(null=True, blank=True, db_column='outlook_calendar_access_token')
    outlookCalendarRefreshToken = models.TextField(null=True, blank=True, db_column='outlook_calendar_refresh_token')
    outlookCalendarSyncTime = models.CharField(max_length=255, null=True, blank=True, db_column='outlook_calendar_sync_time')
    conversationsTwilioNumber = models.CharField(max_length=255, null=True, blank=True, db_column='conversationsTwilioNumber')
    twoFANo = models.CharField(max_length=255, null=True, blank=True, db_column='2FANo')
    smsAllowFlg = models.IntegerField(db_column='sms_allow_flg')
    smsWhiteFlag = models.IntegerField(db_column='sms_white_flag')
    planId = models.BigIntegerField(default=0, db_column='plan_id')
    authKey = models.CharField(max_length=255, null=True, blank=True, db_column='auth_key')
    authToken = models.CharField(max_length=255, null=True, blank=True, db_column='auth_token')
    conversationsSubAccountPhoneSId = models.CharField(max_length=255, null=True, blank=True, db_column='conversationsSubAccountPhoneSId')
    conversationsTwilioNumberPurchaseDt = models.DateTimeField(null=True, blank=True, db_column='conversationsTwilioNumberPurchaseDt')
    conversationsTwilioNumberRenewDt = models.DateTimeField(null=True, blank=True, db_column='conversationsTwilioNumberRenewDt')
    defaultConversationsSubAccountPhoneSId = models.CharField(max_length=255, null=True, blank=True, db_column='defaultConversationsSubAccountPhoneSId')
    defaultConversationsTwilioNumber = models.CharField(max_length=255, null=True, blank=True, db_column='defaultConversationsTwilioNumber')
    emailNotification = models.TextField(null=True, blank=True, db_column='email_notification')
    enableApi = models.CharField(max_length=1, default='N', db_column='enable_api')
    googleCalendarEmail = models.CharField(max_length=255, null=True, blank=True, db_column='google_calendar_email')
    linkSendDt = models.DateTimeField(null=True, blank=True, db_column='link_send_dt')
    outlookCalendarEmail = models.CharField(max_length=255, null=True, blank=True, db_column='outlook_calendar_email')
    smsNotification = models.CharField(max_length=1, default='N', db_column='sms_notification')
    timeZone = models.CharField(max_length=255, null=True, blank=True, db_column='time_zone')
    webConference = models.TextField(null=True, blank=True, db_column='web_conference')
    tenDLCStatus = models.CharField(max_length=255, default='No', db_column='10dlc_status')
    loginPreference = models.CharField(max_length=255, null=True, blank=True, db_column='login_preference')
    username = models.CharField(max_length=255, null=True, blank=True, db_column='username')

    @property
    def is_authenticated(self):
        return True

    class Meta:
        managed = False
        db_table = 'tbl_member'

class CountrySetting(models.Model):
    id = models.BigAutoField(primary_key=True)
    cntyId = models.BigIntegerField(db_column='cntyId', null=True, blank=True)
    cntyISO2 = models.CharField(max_length=255, db_column='cntyISO2', null=True, blank=True)
    cntyName = models.CharField(max_length=255, db_column='cntyName', null=True, blank=True)
    cntyPriceSymbol = models.CharField(max_length=255, db_column='cntyPriceSymbol', null=True, blank=True)
    cntyAssessmentPrice = models.FloatField(db_column='cntyAssessmentPrice', default=0.0)
    cntySurveyPrice = models.FloatField(db_column='cntySurveyPrice', default=0.0)
    cntyIndividualPrice = models.FloatField(db_column='cntyIndividualPrice', default=0.0)
    cntySocialMediaPrice = models.FloatField(db_column='cntySocialMediaPrice', default=0.0)
    cntyCampaignPerPrice = models.FloatField(db_column='cntyCampaignPerPrice', default=0.0)
    cntySurveyPerPrice = models.FloatField(db_column='cntySurveyPerPrice', default=0.0)
    cntyAssessmentPerPrice = models.FloatField(db_column='cntyAssessmentPerPrice', default=0.0)
    cntyMMSPerPrice = models.FloatField(db_column='cntyMMSPerPrice', default=0.0)
    cntySMSPerPrice = models.FloatField(db_column='cntySMSPerPrice', default=0.0)
    cntySMSNumberPerPrice = models.FloatField(db_column='cntySMSNumberPerPrice', default=0.0)
    cntyFirstInvFreeAmt = models.FloatField(db_column='cntyFirstInvFreeAmt', default=0.0)
    cntyInvLessAmtNotCharge = models.FloatField(db_column='cntyInvLessAmtNotCharge', default=0.0)
    cntyTranslateCharCharge = models.FloatField(db_column='cntyTranslateCharCharge', default=0.0)
    cntySMSConversationsPerPrice = models.FloatField(db_column='cntySMSConversationsPerPrice', default=0.0)
    cntyCallPerMinPrice = models.FloatField(db_column='cntyCallPerMinPrice', default=0.0)
    cntyContactsIncluded = models.BigIntegerField(db_column='cntyContactsIncluded', null=True, blank=True)
    cntyMaxNumberOfEmail = models.BigIntegerField(db_column='cntyMaxNumberOfEmail', null=True, blank=True)
    cntyPlanId = models.BigIntegerField(db_column='cntyPlanId', null=True, blank=True)
    cntyPlanPrice = models.FloatField(db_column='cntyPlanPrice', default=0.0)
    cntySupport = models.TextField(db_column='cntySupport', null=True, blank=True)
    cntyMultiUser = models.CharField(max_length=255, db_column='cntyMultiUser', null=True, blank=True)
    cntyAutomation = models.CharField(max_length=255, db_column='cntyAutomation', null=True, blank=True)
    cntyWhiteListing = models.CharField(max_length=255, db_column='cntyWhiteListing', null=True, blank=True)
    cntyCalendar = models.CharField(max_length=255, db_column='cntyCalendar', null=True, blank=True)
    cntyZoomConferences = models.CharField(max_length=255, db_column='cntyZoomConferences', null=True, blank=True)
    cntySocialMedia = models.CharField(max_length=255, db_column='cntySocialMedia', null=True, blank=True)
    cntySmsInbox = models.CharField(max_length=255, db_column='cntySmsInbox', null=True, blank=True)
    cntyAbTesting = models.CharField(max_length=255, db_column='cntyAbTesting', null=True, blank=True)
    cntyPlanPopular = models.CharField(max_length=255, db_column='cntyPlanPopular', null=True, blank=True)
    cntyPlanDisplayOrder = models.IntegerField(db_column='cntyPlanDisplayOrder', null=True, blank=True)
    cntyFormResponse = models.FloatField(db_column='cntyFormResponse', default=0.0)
    cntyAdditionalContacts = models.IntegerField(db_column='cntyAdditionalContacts', null=True, blank=True)
    cntyAdditionalContactsPrice = models.FloatField(db_column='cntyAdditionalContactsPrice', default=0.0)
    cnty10DLCPrice = models.FloatField(db_column='cnty10DLCPrice', default=0.0)
    cnty10DLCCampaignTypeCharge = models.FloatField(db_column='cnty10DLCCampaignTypeCharge', default=0.0)
    cnty10DLCOtherCharge = models.FloatField(db_column='cnty10DLCOtherCharge', default=0.0)
    cntyWarmupPrice = models.FloatField(db_column='cntyWarmupPrice', default=0.0)
    ctnyAiGeneratedImage = models.FloatField(db_column='ctnyAiGeneratedImage', default=0.0)
    ctnyAiEditedImage = models.FloatField(db_column='ctnyAiEditedImage', default=0.0)
    ctnyContactPerPrice = models.FloatField(db_column='ctnyContactPerPrice', default=0.0)
    cntyLinkExpiryDateTime = models.DateTimeField(db_column='cntyLinkExpiryDateTime', null=True, blank=True)
    cntyUpdateDateTime = models.DateTimeField(db_column='cntyUpdateDateTime', null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'tbl_country_setting'

class CampaignsEmail(models.Model):
    campId = models.BigAutoField(primary_key=True, db_column='camp_id')
    byAutoManual = models.CharField(max_length=10, null=True, blank=True)
    byMeasure = models.CharField(max_length=10, null=True, blank=True)
    byNumber = models.IntegerField(null=True, blank=True)
    byType = models.CharField(max_length=10, null=True, blank=True)
    campDesc = models.TextField(null=True, blank=True, db_column='camp_desc')
    campDetail = models.TextField(db_column='camp_detail')
    campDetailB = models.TextField(null=True, blank=True, db_column='camp_detail_B')
    campEmailServers = models.CharField(max_length=255, db_column='camp_email_servers')
    campGroup = models.CharField(max_length=10, db_column='camp_group')
    campMainType = models.IntegerField(null=True, blank=True, db_column='camp_main_type')
    campName = models.TextField(db_column='camp_name')
    campStatus = models.IntegerField(null=True, blank=True, db_column='camp_status')
    campType = models.IntegerField(db_column='camp_type')
    defEmId = models.IntegerField(null=True, blank=True, db_column='def_em_id')
    emailSetting = models.CharField(max_length=1, null=True, blank=True, db_column='email_setting')
    fromAdd = models.CharField(max_length=255, db_column='from_add')
    fromName = models.CharField(max_length=255, null=True, blank=True, db_column='from_name')
    fromNameB = models.CharField(max_length=255, null=True, blank=True, db_column='from_name_B')
    groupList = models.TextField(db_column='grouplist')
    incrementalUpdates = models.CharField(max_length=10, null=True, blank=True, db_column='incremental_updates')
    isSend = models.CharField(max_length=1, null=True, blank=True, db_column='is_send')
    logo = models.CharField(max_length=255, null=True, blank=True)
    lookSerUrl = models.TextField(db_column='look_ser_url')
    mailType = models.CharField(max_length=255, null=True, blank=True, db_column='mail_type')
    mailServer = models.TextField(db_column='mailServer')
    memberList = models.TextField(null=True, blank=True, db_column='memberlist')
    mySerReqAuth = models.CharField(max_length=255, db_column='my_ser_req_auth')
    mypageId = models.BigIntegerField(null=True, blank=True, db_column='mypageId')
    mypageIdB = models.BigIntegerField(null=True, blank=True, db_column='mypageIdB')
    ppassword = models.CharField(max_length=255)
    publicWebAdd = models.CharField(max_length=255, db_column='public_web_add')
    pusername = models.CharField(max_length=255)
    ranQues = models.CharField(max_length=2, db_column='ran_ques')
    readMemberList = models.TextField(db_column='readMemberList')
    readyToMail = models.CharField(max_length=1, db_column='ReadyToMail')
    remainGroupPer = models.IntegerField(null=True, blank=True, db_column='remaingroupper')
    replyToAdd = models.CharField(max_length=255, db_column='reply_to_add')
    resendDuration = models.IntegerField(null=True, blank=True)
    resendTillOpen = models.CharField(max_length=1, db_column='resendTillOpen')
    resultTie = models.CharField(max_length=10, null=True, blank=True, db_column='result_tie')
    rndQuesTxt = models.IntegerField(db_column='rnd_ques_txt')
    scheduleType = models.IntegerField(null=True, blank=True)
    scheduleTypeB = models.IntegerField(null=True, blank=True)
    segId = models.BigIntegerField(null=True, blank=True)
    selectGroupPer = models.IntegerField(null=True, blank=True, db_column='selectgroupper')
    sendDate = models.DateTimeField(db_column='send_date')
    sendOnDate = models.DateTimeField(null=True, blank=True)
    sendOnDateB = models.DateTimeField(null=True, blank=True)
    sendOnTime = models.TimeField(null=True, blank=True)
    sendOnTimeB = models.TimeField(null=True, blank=True)
    subMemberId = models.BigIntegerField(null=True, blank=True, db_column='sub_member_id')
    subject = models.CharField(max_length=255)
    subjectB = models.CharField(max_length=255, null=True, blank=True)
    templateId = models.BigIntegerField(db_column='template_id')
    templateName = models.CharField(max_length=255, db_column='template_name')
    testingType = models.IntegerField(null=True, blank=True, db_column='testing_type')
    tries = models.IntegerField(null=True, blank=True)
    triesCount = models.IntegerField(null=True, blank=True, db_column='tries_count')
    tt = models.IntegerField(null=True, blank=True)
    memberId = models.BigIntegerField(db_column='Member_Id')
    archiveYn = models.CharField(max_length=1, default='N', db_column='archive_yn')

    class Meta:
        managed = False
        db_table = 'tbl_campaigns_email'

class Userlist(models.Model):
    emailId = models.BigAutoField(primary_key=True, db_column='Email_Id')
    email = models.CharField(max_length=255, null=True, blank=True, db_column='Email')
    firstName = models.CharField(max_length=255, null=True, blank=True, db_column='First_Name')
    lastName = models.CharField(max_length=255, null=True, blank=True, db_column='Last_Name')
    phoneNumber = models.CharField(max_length=255, null=True, blank=True, db_column='phoneNumber')
    udf1 = models.CharField(max_length=255, null=True, blank=True, db_column='udf1')
    udf2 = models.CharField(max_length=255, null=True, blank=True, db_column='udf2')
    udf3 = models.CharField(max_length=255, null=True, blank=True, db_column='udf3')
    udf4 = models.CharField(max_length=255, null=True, blank=True, db_column='udf4')
    udf5 = models.CharField(max_length=255, null=True, blank=True, db_column='udf5')
    udf6 = models.CharField(max_length=255, null=True, blank=True, db_column='udf6')
    udf7 = models.CharField(max_length=255, null=True, blank=True, db_column='udf7')
    udf8 = models.CharField(max_length=255, null=True, blank=True, db_column='udf8')
    udf9 = models.CharField(max_length=255, null=True, blank=True, db_column='udf9')
    udf10 = models.CharField(max_length=255, null=True, blank=True, db_column='udf10')
    groupId = models.BigIntegerField(db_column='group_id', null=True, blank=True)
    memberId = models.BigIntegerField(db_column='Member_Id', null=True, blank=True)
    status = models.CharField(max_length=255, db_column='Status', null=True, blank=True)
    smsStatus = models.CharField(max_length=255, db_column='smsStatus', null=True, blank=True)
    badEmail = models.CharField(max_length=1, db_column='BadEmail', default='N')
    badPhoneNumber = models.CharField(max_length=1, db_column='BadPhoneNumber', default='N')
    optId = models.BigIntegerField(db_column='optid', null=True, blank=True)
    isChecked = models.IntegerField(null=True, blank=True, db_column='IsChecked')
    bounceReason = models.TextField(null=True, blank=True, db_column='bouncereason')
    tempCronId = models.BigIntegerField(null=True, blank=True, db_column='temp_cron_id')
    smsSid = models.CharField(max_length=255, null=True, blank=True, db_column='smsSid')
    streetAddress1 = models.TextField(null=True, blank=True, db_column='street_address1')
    streetAddress2 = models.TextField(null=True, blank=True, db_column='street_address2')
    fullName = models.CharField(max_length=255, null=True, blank=True, db_column='full_name')
    phone = models.CharField(max_length=255, null=True, blank=True, db_column='phone')
    city = models.CharField(max_length=255, null=True, blank=True, db_column='city')
    stateProvRegion = models.CharField(max_length=255, null=True, blank=True, db_column='stateProvRegion')
    zipPostalCode = models.CharField(max_length=255, null=True, blank=True, db_column='zipPostalCode')
    country = models.CharField(max_length=255, null=True, blank=True, db_column='country')
    birthday = models.CharField(max_length=255, null=True, blank=True, db_column='birthday')
    gender = models.CharField(max_length=255, null=True, blank=True, db_column='gender')
    signupSource = models.CharField(max_length=255, null=True, blank=True, db_column='signupSource')
    contactRating = models.BigIntegerField(null=True, blank=True, db_column='contactRating')
    optInIPAddress = models.CharField(max_length=255, null=True, blank=True, db_column='optInIPAddress')
    confirmIP = models.CharField(max_length=255, null=True, blank=True, db_column='confirmIP')
    optOutIpAddress = models.CharField(max_length=255, null=True, blank=True, db_column='optOutIpAddress')
    latitude = models.CharField(max_length=255, null=True, blank=True, db_column='latitude')
    longitude = models.CharField(max_length=255, null=True, blank=True, db_column='longitude')
    gmtOff = models.CharField(max_length=255, null=True, blank=True, db_column='gmtOff')
    dstOff = models.CharField(max_length=255, null=True, blank=True, db_column='dstOff')
    timeZone = models.CharField(max_length=255, null=True, blank=True, db_column='timeZone')
    region = models.CharField(max_length=255, null=True, blank=True, db_column='region')
    notes = models.TextField(null=True, blank=True, db_column='notes')
    tags = models.TextField(null=True, blank=True, db_column='tags')
    emailClientUsed = models.CharField(max_length=255, null=True, blank=True, db_column='emailClientUsed')
    emailDomain = models.CharField(max_length=255, null=True, blank=True, db_column='email_domain')
    cc = models.CharField(max_length=255, null=True, blank=True, db_column='CC')
    leid = models.CharField(max_length=255, null=True, blank=True, db_column='LEID')
    euid = models.CharField(max_length=255, null=True, blank=True, db_column='EUID')
    age = models.FloatField(null=True, blank=True, db_column='age')
    jobTitle = models.CharField(max_length=255, null=True, blank=True, db_column='jobTitle')
    emailPermissionStatusOther = models.CharField(max_length=255, null=True, blank=True, db_column='emailPermissionStatusOther')
    emailLists = models.CharField(max_length=255, null=True, blank=True, db_column='emailLists')
    selectDateFormat = models.CharField(max_length=255, null=True, blank=True, db_column='selectDateFormat')
    usDefaultLanguage = models.CharField(max_length=255, null=True, blank=True, db_column='us_default_language')
    isEmailValidate = models.CharField(max_length=255, null=True, blank=True, db_column='is_email_validate')
    storeCustomerId = models.CharField(max_length=255, null=True, blank=True, db_column='store_customer_id')
    subMemberId = models.BigIntegerField(null=True, blank=True, db_column='sub_member_id')
    dateRegistered = models.DateTimeField(null=True, blank=True, db_column='Date_Registered')
    optDate = models.DateTimeField(null=True, blank=True, db_column='optDate')
    optBackInDate = models.DateTimeField(null=True, blank=True, db_column='optBackInDate')
    optOutDate = models.DateTimeField(null=True, blank=True, db_column='optOutDate')
    dateAdded = models.DateTimeField(null=True, blank=True, db_column='dateAdded')
    dateLastModified = models.DateTimeField(null=True, blank=True, db_column='dateLastModified')
    confirmDateTime = models.DateTimeField(null=True, blank=True, db_column='confirmDateTime')
    typeEmail = models.CharField(max_length=255, null=True, blank=True, db_column='type_email')
    typeSms = models.CharField(max_length=255, null=True, blank=True, db_column='type_sms')
    sendToEmailVerification = models.CharField(max_length=255, default='No', db_column='send_to_email_verification')

    class Meta:
        managed = False
        db_table = 'tbl_userlist'

class Udf(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='id')
    groupId = models.BigIntegerField(db_column='group_id')
    udf = models.CharField(max_length=255, db_column='udf')
    udfLabel = models.IntegerField(db_column='udf_label')

    class Meta:
        managed = False
        db_table = 'tbl_udf'

class CampaignTransaction(models.Model):
    tranId = models.BigAutoField(primary_key=True, db_column='tranId')
    tranCampaignId = models.BigIntegerField(db_column='tranCampaignId')
    tranCampaignName = models.CharField(max_length=255, db_column='tranCampaignName')
    tranCampaignDate = models.DateTimeField(db_column='tranCampaignDate')
    tranTotalMember = models.BigIntegerField(db_column='tranTotalMember')
    tranType = models.CharField(max_length=255, db_column='tranType')
    tranInvoicedId = models.BigIntegerField(db_column='tranInvoicedId')
    tranInvoicedStatus = models.CharField(max_length=255, db_column='tranInvoicedStatus')
    tranInvoicedDate = models.DateField(null=True, blank=True, db_column='tranInvoicedDate')
    memberId = models.BigIntegerField(db_column='Member_Id')
    tranBillType = models.CharField(max_length=255, db_column='tranBillType')
    tranTotalAmount = models.FloatField(db_column='tranTotalAmount')
    tranMemberRate = models.FloatField(db_column='tranMemberRate')
    tranCountTotalSms = models.BigIntegerField(db_column='tranCountTotalSms')
    tranPollFormNo = models.CharField(max_length=255, null=True, blank=True, db_column='tranPollFormNo')
    tranPollToNo = models.CharField(max_length=255, null=True, blank=True, db_column='tranPollToNo')
    subMemberId = models.BigIntegerField(db_column='sub_member_id')

    class Meta:
        managed = False
        db_table = 'tbl_campaign_transaction'

class Admin(models.Model):
    memberId = models.BigAutoField(primary_key=True, db_column='Member_Id')
    userName = models.CharField(max_length=255, db_column='User_Name')
    password = models.CharField(max_length=255, db_column='Password')
    firstName = models.CharField(max_length=255, null=True, blank=True, db_column='First_Name')
    lastName = models.CharField(max_length=255, null=True, blank=True, db_column='Last_Name')
    email = models.CharField(max_length=255, db_column='Email')
    active = models.CharField(max_length=1, default='Y', db_column='Active')
    dateRegistered = models.DateTimeField(null=True, blank=True, db_column='Date_Registered')
    lastLoggedIn = models.DateTimeField(null=True, blank=True, db_column='Last_Loggedin')
    userType = models.IntegerField(db_column='usertype')

    @property
    def is_authenticated(self):
        return True

    class Meta:
        managed = False
        db_table = 'tbl_admin'

class AdminType(models.Model):
    styId = models.BigAutoField(primary_key=True, db_column='aty_id')
    styName = models.CharField(max_length=255, db_column='aty_name')
    styCreatedDate = models.DateTimeField(null=True, blank=True, db_column='aty_created_date')

    class Meta:
        managed = False
        db_table = 'tbl_admin_type'

class AffiliateProgram(models.Model):
    apId = models.BigAutoField(primary_key=True, db_column='ap_id')
    apTitle = models.CharField(max_length=255, db_column='ap_title')
    apCommission = models.FloatField(db_column='ap_commission')
    apCommissionType = models.IntegerField(db_column='ap_commission_type', default=1)
    apCode = models.CharField(max_length=255, db_column='ap_code', null=True, blank=True)
    apIsActive = models.CharField(max_length=255, db_column='ap_is_active', default='N')
    apDate = models.DateTimeField(db_column='ap_date', null=True, blank=True)
    apExpiryDate = models.DateField(db_column='ap_expiry_date', null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'affiliate_program'

class AdminPage(models.Model):
    pgId = models.BigAutoField(primary_key=True, db_column='pg_id')
    pgName = models.CharField(max_length=255, null=True, blank=True, db_column='pg_name')
    pgMenuName = models.CharField(max_length=255, null=True, blank=True, db_column='pg_menu_name')
    pgModuleName = models.CharField(max_length=255, null=True, blank=True, db_column='pg_module_name')

    class Meta:
        managed = False
        db_table = 'tbl_admin_page'

class AdminPageDetails(models.Model):
    pgdId = models.BigAutoField(primary_key=True, db_column='pgd_id')
    pgdPgId = models.BigIntegerField(null=True, blank=True, db_column='pgd_pg_id')
    pgdActionName = models.CharField(max_length=255, null=True, blank=True, db_column='pgd_action_name')

    class Meta:
        managed = False
        db_table = 'tbl_admin_page_details'


class AdminPagePermission(models.Model):
    perId = models.BigAutoField(primary_key=True, db_column='per_id')
    perPgId = models.BigIntegerField(null=True, blank=True, db_column='per_pg_id')
    perActionName = models.CharField(max_length=255, null=True, blank=True, db_column='per_action_name')
    perStyId = models.BigIntegerField(null=True, blank=True, db_column='per_sty_id')
    perMemberId = models.BigIntegerField(null=True, blank=True, db_column='per_member_id')

    class Meta:
        managed = False
        db_table = 'tbl_admin_page_permission'


class CampaignsEmailSend(models.Model):
    id = models.BigAutoField(primary_key=True)
    bounceUids = models.TextField(null=True, blank=True, db_column='bounce_uids')
    byAutoManual = models.CharField(max_length=10, null=True, blank=True, db_column='byAutoManual')
    byMeasure = models.CharField(max_length=10, null=True, blank=True, db_column='byMeasure')
    byNumber = models.IntegerField(null=True, blank=True, db_column='byNumber')
    byType = models.CharField(max_length=10, null=True, blank=True, db_column='byType')
    campDesc = models.TextField(null=True, blank=True, db_column='camp_desc')
    campDetail = models.TextField(null=True, blank=True, db_column='camp_detail')
    campDetailB = models.TextField(null=True, blank=True, db_column='camp_detail_B')
    campEmailServers = models.CharField(max_length=255, default='EmailsAndSurveys.com', db_column='camp_email_servers')
    campGroup = models.CharField(max_length=10, null=True, blank=True, db_column='camp_group')
    campId = models.IntegerField(null=True, blank=True, db_column='camp_id')
    campMainType = models.IntegerField(null=True, blank=True, db_column='camp_main_type')
    campName = models.TextField(db_column='camp_name')
    campType = models.IntegerField(default=0, db_column='camp_type')
    emailEndTime = models.DateTimeField(null=True, blank=True, db_column='email_end_time')
    emailServerIp = models.CharField(max_length=255, null=True, blank=True, db_column='email_server_ip')
    emailSetting = models.CharField(max_length=255, null=True, blank=True, db_column='email_setting')
    emailStartTime = models.DateTimeField(null=True, blank=True, db_column='email_start_time')
    fromAdd = models.CharField(max_length=255, db_column='from_add')
    fromName = models.CharField(max_length=255, null=True, blank=True, db_column='from_name')
    fromNameB = models.CharField(max_length=255, null=True, blank=True, db_column='from_name_B')
    groupList = models.TextField(db_column='grouplist')
    incrementalUpdates = models.CharField(max_length=10, null=True, blank=True, db_column='incremental_updates')
    isCompletedAB = models.CharField(max_length=1, default='N', db_column='is_completed_AB')
    isProcessed = models.CharField(max_length=1, default='N', db_column='is_processed')
    isSend = models.CharField(max_length=1, null=True, blank=True, db_column='is_send')
    lastClicked = models.DateTimeField(null=True, blank=True, db_column='last_clicked')
    lastOpened = models.DateTimeField(null=True, blank=True, db_column='last_opened')
    logo = models.CharField(max_length=255, null=True, blank=True, db_column='logo')
    lookSerUrl = models.TextField(null=True, blank=True, db_column='look_ser_url')
    mailType = models.CharField(max_length=255, default='Newsletter', db_column='mail_type')
    mailServer = models.TextField(null=True, blank=True, db_column='mailServer')
    memberList = models.TextField(null=True, blank=True, db_column='memberlist')
    mySerReqAuth = models.CharField(max_length=255, db_column='my_ser_req_auth')
    mypageId = models.BigIntegerField(null=True, blank=True, db_column='MYPAGEID')
    mypageIdB = models.BigIntegerField(null=True, blank=True, db_column='MYPAGEIDB')
    ppassword = models.CharField(max_length=255, null=True, blank=True, db_column='ppassword')
    processedEmails = models.TextField(null=True, blank=True, db_column='processed_emails')
    processedEmailsCount = models.BigIntegerField(default=0, db_column='processed_emails_count')
    publicWebAdd = models.CharField(max_length=255, null=True, blank=True, db_column='public_web_add')
    pusername = models.CharField(max_length=255, null=True, blank=True, db_column='pusername')
    ranQues = models.CharField(max_length=2, default='N', db_column='ran_ques')
    readMemberList = models.TextField(null=True, blank=True, db_column='readMemberList')
    readyToMail = models.CharField(max_length=1, default='N', db_column='readyToMail')
    remaingroupper = models.IntegerField(null=True, blank=True, db_column='remaingroupper')
    replyToAdd = models.CharField(max_length=255, db_column='reply_to_add')
    resendDuration = models.IntegerField(null=True, blank=True, db_column='resendDuration')
    resendTillOpen = models.CharField(max_length=3, default='No', db_column='resendTillOpen')
    resultTie = models.CharField(max_length=10, null=True, blank=True, db_column='result_tie')
    rndQuesTxt = models.IntegerField(default=0, db_column='rnd_ques_txt')
    scheduleTypeB = models.IntegerField(null=True, blank=True, db_column='scheduleTypeB')
    selectgroupper = models.IntegerField(null=True, blank=True, db_column='selectgroupper')
    sendDate = models.DateTimeField(db_column='send_date')
    sendOnDate = models.DateTimeField(null=True, blank=True, db_column='sendOnDate')
    sendOnDateB = models.DateTimeField(null=True, blank=True, db_column='sendOnDateB')
    sendOnTime = models.DurationField(null=True, blank=True, db_column='sendOnTime')
    sendOnTimeB = models.DurationField(null=True, blank=True, db_column='sendOnTimeB')
    subMemberId = models.BigIntegerField(default=0, db_column='sub_member_id')
    subject = models.CharField(max_length=255, db_column='subject')
    subjectB = models.CharField(max_length=255, null=True, blank=True, db_column='subjectB')
    templateName = models.CharField(max_length=255, default='demo1', db_column='template_name')
    testingType = models.IntegerField(null=True, blank=True, db_column='testing_type')
    tries = models.IntegerField(null=True, blank=True, db_column='tries')
    triesCount = models.IntegerField(null=True, blank=True, db_column='tries_count')
    tt = models.IntegerField(null=True, blank=True, db_column='tt')
    unsubscribeUid = models.TextField(null=True, blank=True, db_column='unsubscribe_uid')
    memberId = models.BigIntegerField(db_column='Member_Id', null=True, blank=True)

    isProccessedByLoadbalancer = models.IntegerField(default=0, db_column='is_proccessed_by_loadbalancer')
    archiveYn = models.CharField(max_length=1, default='N', db_column='archive_yn')
    totalQueued = models.IntegerField(default=0, db_column='total_queued')
    totalQueuedB = models.IntegerField(default=0, db_column='total_queued_b')
    totalQueuedO = models.IntegerField(default=0, db_column='total_queued_o')
    retrySendDateTime = models.DateTimeField(null=True, blank=True, db_column='retry_send_date_time')
    maxBounceEmail = models.IntegerField(default=0, db_column='max_bounce_email')
    retrySendCount = models.IntegerField(default=0, db_column='retry_send_count')
    throttling = models.CharField(max_length=1, null=True, blank=True, db_column='throttling')
    throttlingType = models.CharField(max_length=500, null=True, blank=True, db_column='throttling_type')
    throttlingValue = models.IntegerField(null=True, blank=True, db_column='throttling_value')
    throttlingNextDate = models.DateTimeField(null=True, blank=True, db_column='throttling_next_date')
    stopStatus = models.TextField(null=True, blank=True, db_column='stop_status')

    class Meta:
        managed = False
        db_table = 'tbl_campaigns_email_send'




class SmtpServer(models.Model):
    serverId = models.AutoField(primary_key=True, db_column='id')
    serverName = models.CharField(max_length=45, null=True, blank=True, db_column='server_name')
    serverStatus = models.CharField(max_length=10, null=True, blank=True, db_column='server_status')
    serverDomain = models.CharField(max_length=255, null=True, blank=True, db_column='server_domain')
    capacityHr = models.BigIntegerField(null=True, blank=True, db_column='capacity_hr')
    capacityDay = models.BigIntegerField(null=True, blank=True, db_column='capacity_day')
    weightHr = models.BigIntegerField(null=True, blank=True, db_column='weight_hr')
    weightDay = models.BigIntegerField(null=True, blank=True, db_column='weight_day')
    reactiveTime = models.DateTimeField(null=True, blank=True, db_column='reactive_time')
    activeDate = models.DateField(null=True, blank=True, db_column='active_date')
    location = models.CharField(max_length=255, null=True, blank=True, db_column='location')
    country = models.CharField(max_length=255, null=True, blank=True, db_column='country')
    threads = models.IntegerField(null=True, blank=True, db_column='threads')
    mps = models.FloatField(null=True, blank=True, db_column='mps')
    isActive = models.IntegerField(db_column='is_active')
    pctFailure = models.FloatField(null=True, blank=True, db_column='pct_failure_10min')
    currentFailureRate = models.FloatField(null=True, blank=True, db_column='current_failure_rate')

    class Meta:
        managed = False
        db_table = 'tbl_smtp_servers'


class SubaccountPage(models.Model):
    pgId = models.BigAutoField(primary_key=True, db_column='pg_id')
    pgName = models.CharField(max_length=255, null=True, blank=True, db_column='pg_name')
    pgMenuName = models.CharField(max_length=255, null=True, blank=True, db_column='pg_menu_name')
    pgModuleName = models.CharField(max_length=255, null=True, blank=True, db_column='pg_module_name')

    class Meta:
        managed = False
        db_table = 'tbl_subaccount_page'


class SubaccountPageDetails(models.Model):
    pgdId = models.BigAutoField(primary_key=True, db_column='pgd_id')
    pgdPgId = models.BigIntegerField(null=True, blank=True, db_column='pgd_pg_id')
    pgdActionName = models.CharField(max_length=255, null=True, blank=True, db_column='pgd_action_name')

    class Meta:
        managed = False
        db_table = 'tbl_subaccount_page_details'


class FreeTemplate(models.Model):
    ftId = models.BigAutoField(primary_key=True, db_column='ft_id')
    ftName = models.CharField(max_length=255, null=True, blank=True, db_column='ft_name')
    ftFolderName = models.CharField(max_length=255, null=True, blank=True, db_column='ft_foldername')
    ftStage = models.IntegerField(db_column='ft_stage')
    ftCatId = models.BigIntegerField(null=True, blank=True, db_column='ft_cat_id')
    ftTags = models.TextField(null=True, blank=True, db_column='ft_tags')

    class Meta:
        managed = False
        db_table = 'tbl_freetemplate'


class Invoice(models.Model):
    invId = models.BigAutoField(primary_key=True, db_column='invId')
    invNo = models.BigIntegerField(default=0, db_column='invNo')
    invAdjustmentsAmount = models.FloatField(default=0.0, db_column='invAdjustmentsAmount')
    invAssessmentAmount = models.FloatField(default=0.0, db_column='invAssessmentAmount')
    invAssessmentPrice = models.FloatField(default=0.0, db_column='invAssessmentPrice')
    invBuildItForMeAmount = models.FloatField(default=0.0, db_column='invBuildItForMeAmount')
    invBuildItForMePrice = models.FloatField(default=0.0, db_column='invBuildItForMePrice')
    invCallAmount = models.FloatField(default=0.0, db_column='invCallAmount')
    invCallPrice = models.FloatField(default=0.0, db_column='invCallPrice')
    invCampaignAmount = models.FloatField(default=0.0, db_column='invCampaignAmount')
    invCampaignPrice = models.FloatField(default=0.0, db_column='invCampaignprice')
    invClientName = models.CharField(max_length=255, null=True, blank=True, db_column='invClientName')
    invCountryId = models.BigIntegerField(default=100, db_column='invCountryId')
    invCurrentContacts = models.BigIntegerField(default=0, db_column='invCurrentContacts')
    invDate = models.DateField(null=True, blank=True, db_column='invDate')
    invIndividualAmount = models.FloatField(default=0.0, db_column='invIndividualAmount')
    invIndividualPrice = models.FloatField(default=0.0, db_column='invIndividualPrice')
    invMonthlyEmailAmount = models.FloatField(default=0.0, db_column='invMonthlyEmailAmount')
    invMonthlyIndividualAmount = models.FloatField(default=0.0, db_column='invMonthlyIndividualAmount')
    invMonthlySmsAmount = models.FloatField(default=0.0, db_column='invMonthlySmsAmount')
    invMonthlySocialMediaAmount = models.FloatField(default=0.0, db_column='invMonthlySocialMediaAmount')
    invMonthlySurveyAmount = models.FloatField(default=0.0, db_column='invMonthlySurveyAmount')
    invMonthlyYN = models.CharField(max_length=1, default='N', db_column='invMonthlyYN')
    invPageTransAmount = models.FloatField(default=0.0, db_column='invPageTransAmount')
    invPageTransPrice = models.FloatField(default=0.0, db_column='invPageTransPrice')
    invPayCardNo = models.CharField(max_length=255, null=True, blank=True, db_column='invPayCardNo')
    invSendMail = models.CharField(max_length=1, null=True, blank=True, db_column='invSendMail')
    invSmsAmount = models.FloatField(default=0.0, db_column='invSmsAmount')
    invSMSConversationsAmount = models.FloatField(default=0.0, db_column='invSMSConversationsAmount')
    invSMSConversationsPrice = models.FloatField(default=0.0, db_column='invSMSConversationsPrice')
    invSmsPollAmount = models.FloatField(default=0.0, db_column='invSmsPollAmount')
    invSmsPollPrice = models.FloatField(default=0.0, db_column='invSmsPollPrice')
    invSmsPrice = models.FloatField(default=0.0, db_column='invSmsPrice')
    invSocialMediaAmount = models.FloatField(default=0.0, db_column='invSocialMediaAmount')
    invSocialMediaPrice = models.FloatField(default=0.0, db_column='invSocialMediaPrice')
    invSubTotal = models.FloatField(default=0.0, db_column='invSubTotal')
    invSurveyAmount = models.FloatField(default=0.0, db_column='invSurveyAmount')
    invSurveyPrice = models.FloatField(default=0.0, db_column='invSurveyprice')
    invTotalAmount = models.FloatField(default=0.0, db_column='invTotalAmount')
    invTransationId = models.CharField(max_length=500, null=True, blank=True, db_column='invTransationId')
    subMemberId = models.BigIntegerField(default=0, db_column='sub_member_id')
    memberId = models.BigIntegerField(default=0, db_column='Member_Id')
    invPlanId = models.BigIntegerField(default=0, db_column='invPlanId')
    invPlanName = models.CharField(max_length=255, null=True, blank=True, db_column='invPlanName')
    invPlanPrice = models.FloatField(default=0.0, db_column='invPlanPrice')
    invShareAppointmentAmount = models.FloatField(default=0.0, db_column='invShareAppointmentAmount')
    invSmsCalendarAmount = models.FloatField(default=0.0, db_column='invSmsCalendarAmount')
    invShareAppointmentPrice = models.FloatField(default=0.0, db_column='invShareAppointmentPrice')
    invSmsCalendarPrice = models.FloatField(default=0.0, db_column='invSmsCalendarPrice')
    invAdditionalContactsAmount = models.FloatField(default=0.0, db_column='invAdditionalContactsAmount')
    invAdditionalContactsPrice = models.FloatField(default=0.0, db_column='invAdditionalContactsPrice')
    inv10DLCAmount = models.FloatField(default=0.0, db_column='inv10DLCAmount')
    invWarmupAmount = models.FloatField(default=0.0, db_column='invWarmupAmount')
    invEmailVerificationAmount = models.FloatField(default=0.0, db_column='invEmailVerificationAmount')
    invEmailVerificationPrice = models.FloatField(default=0.0, db_column='invEmailVerificationPrice')

    class Meta:
        managed = False
        db_table = 'tbl_invoice'


class MonthlyCurrentPlan(models.Model):
    cpId = models.BigAutoField(primary_key=True, db_column='cp_id')
    cpMemberId = models.BigIntegerField(db_column='cp_member_id')
    cpEmailQty = models.BigIntegerField(db_column='cp_email_qty')
    cpSmsQty = models.BigIntegerField(db_column='cp_sms_qty')
    cpSurveyQty = models.BigIntegerField(db_column='cp_survey_qty')
    cpFormQty = models.BigIntegerField(db_column='cp_form_qty')
    cpSocialMediaQty = models.BigIntegerField(db_column='cp_socialmedia_qty')
    cpEmailPrice = models.FloatField(db_column='cp_email_price')
    cpSmsPrice = models.FloatField(db_column='cp_sms_price')
    cpSurveyPrice = models.FloatField(db_column='cp_survey_price')
    cpFormPrice = models.FloatField(db_column='cp_form_price')
    cpSocialMediaPrice = models.FloatField(db_column='cp_socialmedia_price')
    cpTotalAmt = models.FloatField(db_column='cp_total_amt')
    cpEmailActive = models.CharField(max_length=1, default='N', db_column='cp_email_active')
    cpSmsActive = models.CharField(max_length=1, default='N', db_column='cp_sms_active')
    cpSurveyActive = models.CharField(max_length=1, default='N', db_column='cp_survey_active')
    cpFormActive = models.CharField(max_length=1, default='N', db_column='cp_form_active')
    cpSocialMediaActive = models.CharField(max_length=1, default='N', db_column='cp_socialmedia_active')
    cpNtMnEmailActive = models.CharField(max_length=1, default='N', db_column='cp_nt_mn_email_active')
    cpNtMnSmsActive = models.CharField(max_length=1, default='N', db_column='cp_nt_mn_sms_active')
    cpNtMnSurveyActive = models.CharField(max_length=1, default='N', db_column='cp_nt_mn_survey_active')
    cpNtMnFormActive = models.CharField(max_length=1, default='N', db_column='cp_nt_mn_form_active')
    cpNtMnSocialMediaActive = models.CharField(max_length=1, default='N', db_column='cp_nt_mn_socialmedia_active')
    cpAddedDate = models.DateTimeField(db_column='cp_added_date', null=True, blank=True)
    cpUpdateDate = models.DateTimeField(db_column='cp_update_date', null=True, blank=True)
    cpExpiredPlanDate = models.DateTimeField(db_column='cp_expired_plan_date', null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'tbl_monthly_current_plan'


class MonthlyPlanLogs(models.Model):
    mplId = models.BigAutoField(primary_key=True, db_column='mpl_id')
    mplMemberId = models.BigIntegerField(db_column='mpl_member_id')
    mplPlanEmailQty = models.BigIntegerField(db_column='mpl_plan_email_qty')
    mplPlanSmsQty = models.BigIntegerField(db_column='mpl_plan_sms_qty')
    mplPlanSurveyQty = models.BigIntegerField(db_column='mpl_plan_survey_qty')
    mplPlanFormQty = models.BigIntegerField(db_column='mpl_plan_form_qty')
    mplPlanSocialMediaQty = models.BigIntegerField(db_column='mpl_plan_socialmedia_qty')
    mplPlanEmailPrice = models.FloatField(db_column='mpl_plan_email_price')
    mplPlanSmsPrice = models.FloatField(db_column='mpl_plan_sms_price')
    mplPlanSurveyPrice = models.FloatField(db_column='mpl_plan_survey_price')
    mplPlanFormPrice = models.FloatField(db_column='mpl_plan_form_price')
    mplPlanSocialMediaPrice = models.FloatField(db_column='mpl_plan_socialmedia_price')
    mplPlanTotalAmt = models.FloatField(db_column='mpl_plan_total_amt')
    mplAddedDate = models.DateTimeField(db_column='mpl_added_date', null=True, blank=True)
    mplInvId = models.BigIntegerField(db_column='mpl_inv_id')

    class Meta:
        managed = False
        db_table = 'tbl_monthly_plan_logs'


class MonthlyPlan(models.Model):
    mpId = models.BigAutoField(primary_key=True, db_column='mp_id')
    mpMemberId = models.BigIntegerField(db_column='mp_member_id')
    mpEmailQty = models.BigIntegerField(db_column='mp_email_qty')
    mpSmsQty = models.BigIntegerField(db_column='mp_sms_qty')
    mpSurveyQty = models.BigIntegerField(db_column='mp_survey_qty')
    mpFormQty = models.BigIntegerField(db_column='mp_form_qty')
    mpSocialMediaQty = models.BigIntegerField(db_column='mp_socialmedia_qty')
    mpIsActive = models.CharField(max_length=1, db_column='mp_is_active')
    mpAddedDate = models.DateTimeField(db_column='mp_added_date', null=True, blank=True)
    mpUpdateDate = models.DateTimeField(db_column='mp_update_date', null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'tbl_monthly_plan'


class Plan(models.Model):
    planId = models.BigAutoField(primary_key=True, db_column='plan_id')
    planName = models.CharField(max_length=255, db_column='plan_name')
    planActive = models.CharField(max_length=255, db_column='plan_active')
    planVisibility = models.CharField(max_length=255, default='Public', db_column='plan_visibility')
    planAddedDate = models.DateTimeField(db_column='plan_added_date', null=True, blank=True)
    planPmIdList = models.CharField(max_length=255, db_column='plan_pm_id_list', null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'tbl_plan'


class Settings(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='id')
    adminName = models.CharField(max_length=255, db_column='admin_name')
    adminEmail = models.CharField(max_length=255, db_column='admin_email')
    facebookLink = models.CharField(max_length=255, db_column='facebook_link', null=True, blank=True)
    twitterLink = models.CharField(max_length=255, db_column='twitter_link', null=True, blank=True)
    gplusLink = models.CharField(max_length=255, db_column='gplus_link', null=True, blank=True)
    linkinLink = models.CharField(max_length=255, db_column='linkin_link', null=True, blank=True)
    siteOnOff = models.CharField(max_length=255, db_column='site_on_off')
    logoName = models.CharField(max_length=255, db_column='logo_name')
    logoSystemName = models.CharField(max_length=255, db_column='logo_system_name')
    paymentSwitch = models.CharField(max_length=255, db_column='payment_switch')
    billPeriod = models.CharField(max_length=255, db_column='bill_period')
    assessmentPrice = models.FloatField(db_column='assessmentPrice')
    surveyPrice = models.FloatField(db_column='surveyPrice')
    individualPrice = models.FloatField(db_column='individualPrice')

    class Meta:
        managed = False
        db_table = 'tbl_settings'


class Surveys(models.Model):
    sryId = models.BigAutoField(primary_key=True, db_column='sry_id')
    sryName = models.CharField(max_length=255, db_column='sry_name')
    sryDescription = models.TextField(db_column='sry_description')
    sryData = models.TextField(db_column='sry_data')
    sryStCategoryPageList = models.TextField(db_column='sry_st_category_page_list')
    sryCountryList = models.TextField(db_column='sry_country_list')
    sryStatus = models.IntegerField(db_column='sry_status')
    sryTinyUrl = models.TextField(db_column='sry_tinyurl')
    sryStId = models.BigIntegerField(db_column='sry_st_id')
    sryStTotalQuestions = models.IntegerField(default=0, db_column='sry_st_total_questions')
    memberId = models.BigIntegerField(db_column='member_id')
    subMemberId = models.BigIntegerField(default=0, db_column='sub_member_id')
    sryCreatedDate = models.DateField(db_column='sry_created_date', null=True, blank=True)
    sryUpdateDate = models.DateField(db_column='sry_update_date', null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'tbl_surveys'


class SpTransLog(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='id')
    smspollingId = models.BigIntegerField(db_column='smspolling_id')
    memberId = models.BigIntegerField(db_column='member_id')
    quesId = models.BigIntegerField(db_column='ques_id')
    question = models.TextField(db_column='question')
    userReply = models.TextField(db_column='user_reply')
    fromNo = models.CharField(max_length=255, db_column='from_no')
    toNo = models.CharField(max_length=255, db_column='to_no')
    smsDate = models.DateTimeField(db_column='sms_date', null=True, blank=True)
    transRate = models.FloatField(db_column='trans_rate')
    transAmt = models.FloatField(db_column='trans_amt')
    memberSend = models.CharField(max_length=255, db_column='member_send')
    fromCountry = models.CharField(max_length=255, db_column='from_country')
    fromState = models.CharField(max_length=255, db_column='from_state')
    fromCity = models.CharField(max_length=255, db_column='from_city')
    fromZip = models.CharField(max_length=255, db_column='from_zip')
    tranId = models.BigIntegerField(default=0, db_column='tranId')
    msgContains = models.TextField(db_column='msgContains')
    questionSend = models.CharField(max_length=255, db_column='questionSend')
    subMemberId = models.BigIntegerField(default=0, db_column='sub_member_id')

    class Meta:
        managed = False
        db_table = 'tbl_sp_trans_log'


class SpQuestions(models.Model):
    queId = models.BigAutoField(primary_key=True, db_column='Que_Id')
    iSmspollingId = models.BigIntegerField(db_column='iSmspolling_Id')
    queTypeId = models.BigIntegerField(db_column='Que_Type_Id')
    question = models.TextField(db_column='Question')
    noOfOptions = models.IntegerField(db_column='No_Of_Options')
    queOrder = models.IntegerField(default=0, db_column='Que_Order')
    disOrder = models.BigIntegerField(db_column='disOrder')
    ddQue = models.IntegerField(default=0, db_column='Dd_Que')
    catId = models.IntegerField(db_column='Cat_Id')

    class Meta:
        managed = False
        db_table = 'tbl_sp_questions'


class SpOptions(models.Model):
    optId = models.BigAutoField(primary_key=True, db_column='Opt_Id')
    optTypeId = models.BigIntegerField(db_column='Opt_Type_Id')
    queId = models.BigIntegerField(db_column='Que_Id')
    optionVal = models.TextField(db_column='OptionVal')
    optOrder = models.IntegerField(default=0, db_column='Opt_Order')
    ansAnalysis = models.TextField(db_column='ans_analysis')
    condQue = models.IntegerField(db_column='cond_que')
    regReq = models.IntegerField(db_column='reg_req')

    class Meta:
        managed = False
        db_table = 'tbl_sp_options'


class SpReply(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='id')
    smsPollingId = models.BigIntegerField(db_column='smspolling_id')
    quesId = models.IntegerField(db_column='ques_id')
    question = models.TextField(db_column='question')
    ansId = models.IntegerField(db_column='ans_id')
    ansVal = models.CharField(max_length=255, db_column='ans_val')
    userReply = models.TextField(db_column='user_reply')
    fromNo = models.CharField(max_length=255, db_column='from_no')
    toNo = models.CharField(max_length=255, db_column='to_no')
    sid = models.CharField(max_length=255, db_column='sid')
    sendDate = models.DateTimeField(db_column='senddate', null=True, blank=True)
    replyDate = models.DateTimeField(db_column='replydate', null=True, blank=True)
    fromCountry = models.CharField(max_length=255, db_column='from_country')
    fromState = models.CharField(max_length=255, db_column='from_state')
    fromCity = models.CharField(max_length=255, db_column='from_city')
    fromZip = models.CharField(max_length=255, db_column='from_zip')
    tranId = models.BigIntegerField(default=0, db_column='tranId')

    class Meta:
        managed = False
        db_table = 'tbl_sp_reply'


class DeleteAccount(models.Model):
    daId = models.BigAutoField(primary_key=True, db_column='daId')
    daAccountId = models.BigIntegerField(db_column='daAccountId')
    daAccountName = models.CharField(max_length=255, db_column='daAccountName')
    daEmail = models.CharField(max_length=255, db_column='daEmail')
    daIpAddress = models.CharField(max_length=255, db_column='daIpAddress')
    daDateTime = models.CharField(max_length=255, db_column='daDateTime')
    daLeavingDetails = models.TextField(db_column='daLeavingDetails')
    daACN = models.TextField(db_column='daACN')

    class Meta:
        managed = False
        db_table = 'tbl_delete_account'


class MemberStatus(models.Model):
    msId = models.BigAutoField(primary_key=True, db_column='msID')
    status = models.IntegerField(db_column='status')
    reason = models.CharField(max_length=255, db_column='reason', null=True, blank=True)
    memberId = models.BigIntegerField(db_column='memberID')
    changeDate = models.DateField(db_column='changedate', null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'tbl_member_status'


class Group(models.Model):
    groupId = models.BigAutoField(primary_key=True, db_column='Group_Id')
    groupName = models.CharField(max_length=75, db_column='Group_Name')
    storeName = models.CharField(max_length=255, db_column='Store_Name', null=True, blank=True)
    ecomCustListType = models.CharField(max_length=50, db_column='ecom_cust_list_type', null=True, blank=True)
    dateRegistered = models.DateTimeField(db_column='Date_Registered', default=timezone.now)
    subMemberId = models.BigIntegerField(db_column='sub_member_id', default=0)
    memberId = models.BigIntegerField(db_column='Member_Id', null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'tbl_groups'


class GroupSegment(models.Model):
    segId = models.BigAutoField(primary_key=True, db_column='segId')
    segName = models.CharField(max_length=255, db_column='segName', null=True, blank=True)
    groupId = models.BigIntegerField(db_column='Group_Id', null=True, blank=True)
    memberId = models.BigIntegerField(db_column='Member_id', null=True, blank=True)
    segQuery = models.TextField(db_column='segQuery', null=True, blank=True)
    segDateAdded = models.DateTimeField(db_column='segAddedDate', default=timezone.now)
    subMemberId = models.BigIntegerField(db_column='sub_member_id', null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'tbl_segment'


class GroupSegmentField(models.Model):
    segfId = models.BigAutoField(primary_key=True, db_column='segfId')
    segId = models.BigIntegerField(db_column='segId', null=True, blank=True)
    segFieldName = models.CharField(max_length=255, db_column='segfFeildsName', null=True, blank=True)
    segFieldOperator = models.CharField(max_length=255, db_column='segfOperator', null=True, blank=True)
    segFieldValue = models.CharField(max_length=255, db_column='segFeildsValue', null=True, blank=True)
    segConditions = models.CharField(max_length=255, db_column='segfConditions', null=True, blank=True)
    segDisplayOrder = models.BigIntegerField(db_column='segfDisplayOrder', null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'tbl_segment_fields'


class TempUserlist(models.Model):
    emailId = models.BigAutoField(primary_key=True, db_column='Email_Id')
    age = models.FloatField(null=True, blank=True, db_column='age')
    birthday = models.CharField(max_length=255, null=True, blank=True, db_column='birthday')
    cc = models.CharField(max_length=255, null=True, blank=True, db_column='CC')
    city = models.CharField(max_length=255, null=True, blank=True, db_column='city')
    confirmDateTime = models.CharField(max_length=255, null=True, blank=True, db_column='confirmDateTime')
    confirmIP = models.CharField(max_length=255, null=True, blank=True, db_column='confirmIP')
    contactRating = models.BigIntegerField(null=True, blank=True, db_column='contactRating')
    country = models.CharField(max_length=255, null=True, blank=True, db_column='country')
    dateAdded = models.CharField(max_length=255, null=True, blank=True, db_column='dateAdded')
    dateLastModified = models.CharField(max_length=255, null=True, blank=True, db_column='dateLastModified')
    dstOff = models.CharField(max_length=255, null=True, blank=True, db_column='dstOff')
    email = models.CharField(max_length=255, null=True, blank=True, db_column='Email')
    emailClientUsed = models.CharField(max_length=255, null=True, blank=True, db_column='emailClientUsed')
    emailLists = models.CharField(max_length=255, null=True, blank=True, db_column='emailLists')
    emailPermissionStatusOther = models.CharField(max_length=255, null=True, blank=True, db_column='emailPermissionStatusOther')
    euid = models.CharField(max_length=255, null=True, blank=True, db_column='EUID')
    firstName = models.CharField(max_length=250, null=True, blank=True, db_column='First_Name')
    gender = models.CharField(max_length=255, null=True, blank=True, db_column='gender')
    gmtOff = models.CharField(max_length=255, null=True, blank=True, db_column='gmtOff')
    jobTitle = models.CharField(max_length=255, null=True, blank=True, db_column='jobTitle')
    lastName = models.CharField(max_length=250, null=True, blank=True, db_column='Last_Name')
    latitude = models.CharField(max_length=255, null=True, blank=True, db_column='latitude')
    leid = models.CharField(max_length=255, null=True, blank=True, db_column='LEID')
    longitude = models.CharField(max_length=255, null=True, blank=True, db_column='longitude')
    notes = models.TextField(null=True, blank=True, db_column='notes')
    optDate = models.CharField(max_length=255, null=True, blank=True, db_column='optDate')
    optInIPAddress = models.CharField(max_length=255, null=True, blank=True, db_column='optInIPAddress')
    optOutIpAddress = models.CharField(max_length=255, null=True, blank=True, db_column='optOutIpAddress')
    phoneNumber = models.CharField(max_length=255, null=True, blank=True, db_column='phoneNumber')
    region = models.CharField(max_length=255, null=True, blank=True, db_column='region')
    selectDateFormat = models.CharField(max_length=255, null=True, blank=True, db_column='selectDateFormat')
    signupSource = models.CharField(max_length=255, null=True, blank=True, db_column='signupSource')
    stateProvRegion = models.CharField(max_length=255, null=True, blank=True, db_column='stateProvRegion')
    status = models.CharField(max_length=255, null=True, blank=True, db_column='status')
    streetAddress1 = models.TextField(null=True, blank=True, db_column='street_address1')
    streetAddress2 = models.TextField(null=True, blank=True, db_column='street_address2')
    fullName = models.CharField(max_length=255, null=True, blank=True, db_column='full_name')
    phone = models.CharField(max_length=255, null=True, blank=True, db_column='phone')
    subMemberId = models.BigIntegerField(null=True, blank=True, db_column='sub_member_id')
    tags = models.TextField(null=True, blank=True, db_column='tags')
    timeZone = models.CharField(max_length=255, null=True, blank=True, db_column='timeZone')
    transId = models.CharField(max_length=500, null=True, blank=True, db_column='Trans_Id')
    udf1 = models.CharField(max_length=250, null=True, blank=True, db_column='udf1')
    udf2 = models.CharField(max_length=250, null=True, blank=True, db_column='udf2')
    udf3 = models.CharField(max_length=250, null=True, blank=True, db_column='udf3')
    udf4 = models.CharField(max_length=250, null=True, blank=True, db_column='udf4')
    udf5 = models.CharField(max_length=250, null=True, blank=True, db_column='udf5')
    udf6 = models.CharField(max_length=250, null=True, blank=True, db_column='udf6')
    udf7 = models.CharField(max_length=250, null=True, blank=True, db_column='udf7')
    udf8 = models.CharField(max_length=250, null=True, blank=True, db_column='udf8')
    udf9 = models.CharField(max_length=250, null=True, blank=True, db_column='udf9')
    udf10 = models.CharField(max_length=250, null=True, blank=True, db_column='udf10')
    zipPostalCode = models.CharField(max_length=255, null=True, blank=True, db_column='zipPostalCode')
    memberId = models.BigIntegerField(null=True, blank=True, db_column='Member_Id')
    usDefaultLanguage = models.CharField(max_length=255, null=True, blank=True, db_column='us_default_language')

    class Meta:
        managed = False
        db_table = 'tbl_temp_userlist'


class TempCronUserListTotal(models.Model):
    cronId = models.BigAutoField(primary_key=True, db_column='cronId')
    cronMemberId = models.BigIntegerField(db_column='cronMemberId')
    cronGroupId = models.BigIntegerField(db_column='cronGroupId')
    cronStartId = models.BigIntegerField(db_column='cronStartId')
    cronEndId = models.BigIntegerField(db_column='cronEndId')
    cronProcess = models.CharField(max_length=255, null=True, blank=True, db_column='cronProcess')
    cronProcessFinished = models.CharField(max_length=1, null=True, blank=True, db_column='cronProcessFinished')
    cronOptInMessage = models.TextField(null=True, blank=True, db_column='cronOptInMessage')

    class Meta:
        managed = False
        db_table = 'tbl_temp_cron_userlist_total'


class RegistrationLinkLogs(models.Model):
    lnkId = models.BigAutoField(primary_key=True, db_column='lnk_id')
    lnkLink = models.TextField(db_column='lnk_link', null=True, blank=True)
    lnkExpiryDateTime = models.DateTimeField(db_column='lnk_expiry_date_time', null=True, blank=True)
    lnkPlanId = models.BigIntegerField(db_column='lnk_plan_id', default=0)
    lnkCountrySettingId = models.BigIntegerField(db_column='lnk_country_setting_id', default=0)
    lnkDateTime = models.DateTimeField(db_column='lnk_date_time', null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'tbl_registration_link_logs'


class EmailVerificationPrice(models.Model):
    evpId = models.BigAutoField(primary_key=True, db_column='evp_id')
    evpContactTotal = models.BigIntegerField(db_column='evp_contact_total', default=0)
    evpRate = models.FloatField(db_column='evp_rate', default=0.0)
    evpCntyId = models.BigIntegerField(db_column='evp_cnty_id', default=0)

    class Meta:
        managed = False
        db_table = 'tbl_email_verification_price'


class PlanModule(models.Model):
    pmId = models.BigAutoField(primary_key=True, db_column='pm_id')
    pmTitle = models.CharField(max_length=255, db_column='pm_title', null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'tbl_plan_module'


class CancelRegistrationLog(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='id')
    username = models.CharField(max_length=255, null=True, blank=True, db_column='username')
    firstName = models.CharField(max_length=255, null=True, blank=True, db_column='first_name')
    lastName = models.CharField(max_length=255, null=True, blank=True, db_column='last_name')
    email = models.CharField(max_length=255, null=True, blank=True, db_column='email')
    cell = models.CharField(max_length=255, null=True, blank=True, db_column='cell')
    step = models.IntegerField(default=1, db_column='step')
    createdDate = models.DateTimeField(null=True, blank=True, db_column='created_date')
    status = models.CharField(max_length=255, default='Leaving', db_column='status')

    class Meta:
        managed = False
        db_table = 'tbl_registration_logs'


class TenDLCLogs(models.Model):
    dlcId = models.BigAutoField(primary_key=True, db_column='dlc_id')
    memberId = models.BigIntegerField(db_column='member_id', null=True, blank=True)
    dlcStatus = models.CharField(max_length=255, db_column='dlc_status', null=True, blank=True)
    dlcDate = models.DateTimeField(db_column='dlc_date', null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'tbl_10dlc_logs'


class TenDLCRenew(models.Model):
    rnwId = models.BigAutoField(primary_key=True, db_column='rnw_id')
    rnwMemberId = models.BigIntegerField(db_column='rnw_member_id', null=True, blank=True)
    rnwContinue = models.CharField(max_length=255, db_column='rnw_continue', null=True, blank=True)
    rnwDate = models.DateField(db_column='rnw_date', null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'tbl_10dlc_renew'


class TenDLCData(models.Model):
    datId = models.BigAutoField(primary_key=True, db_column='dat_id')
    datMemberId = models.BigIntegerField(db_column='dat_member_id', null=True, blank=True)
    datBrandName = models.CharField(max_length=255, db_column='dat_brand_name', null=True, blank=True)
    datCampaignType = models.CharField(max_length=255, db_column='dat_campaign_type', null=True, blank=True)
    datIsActive = models.CharField(max_length=255, db_column='dat_is_active', null=True, blank=True)
    datRegistrationDate = models.DateField(db_column='dat_registration_date', null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'tbl_10dlc_data'


class PlanLogs(models.Model):
    plogsId = models.BigAutoField(primary_key=True, db_column='plogs_id')
    plogsMemberId = models.BigIntegerField(db_column='plogs_member_id', null=True, blank=True)
    plogsPlanId = models.BigIntegerField(db_column='plogs_plan_id', null=True, blank=True)
    plogsAdditionalContacts = models.IntegerField(db_column='plogs_additional_contacts', null=True, blank=True)
    plogsAddedDate = models.DateTimeField(db_column='plogs_added_date', null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'tbl_plan_logs'


class MonthlyPrice(models.Model):
    mnpId = models.BigAutoField(primary_key=True, db_column='mnp_id')
    mnpType = models.CharField(max_length=255, null=True, blank=True, db_column='mnp_type')
    mnpQty = models.BigIntegerField(null=True, blank=True, db_column='mnp_qty')
    mnpPrice = models.FloatField(null=True, blank=True, db_column='mnp_price')
    mnpCountryId = models.BigIntegerField(null=True, blank=True, db_column='mnp_country_id')

    class Meta:
        managed = False
        db_table = 'tbl_monthly_price'


class CampaignsSendEmail(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='id')
    campId = models.BigIntegerField(null=True, blank=True, db_column='camp_id')
    campSendId = models.BigIntegerField(default=0, db_column='camp_send_id')
    memberId = models.BigIntegerField(null=True, blank=True, db_column='member_id')
    email = models.CharField(max_length=500, null=True, blank=True, db_column='email')
    emailId = models.BigIntegerField(null=True, blank=True, db_column='email_id')
    isSend = models.CharField(max_length=1, default='N', db_column='is_send')
    isRead = models.CharField(max_length=1, null=True, blank=True, db_column='is_read')
    isBounced = models.CharField(max_length=1, null=True, blank=True, db_column='is_bounced')
    isUnsubscribed = models.CharField(max_length=1, null=True, blank=True, db_column='is_unsubscribed')
    firstName = models.CharField(max_length=255, null=True, blank=True, db_column='first_name')
    lastName = models.CharField(max_length=255, null=True, blank=True, db_column='last_name')
    emailDomain = models.CharField(max_length=45, null=True, blank=True, db_column='email_domain')
    csDefaultLanguage = models.CharField(max_length=255, default='en', db_column='cs_default_language')
    smtpServerHost = models.CharField(max_length=255, null=True, blank=True, db_column='smtp_server_host')
    isProcessed = models.CharField(max_length=1, default='N', db_column='is_processed')
    emailQId = models.CharField(max_length=255, null=True, blank=True, db_column='email_q_id')
    emailStatus = models.CharField(max_length=255, null=True, blank=True, db_column='email_status')
    cronStatus = models.CharField(max_length=255, default='active', db_column='cron_status')
    splitGroup = models.CharField(max_length=1, null=True, blank=True, db_column='split_group')
    groupWinner = models.CharField(max_length=1, null=True, blank=True, db_column='group_winner')
    msgPriority = models.IntegerField(default=0, db_column='msg_priority')
    subMemberId = models.BigIntegerField(default=0, db_column='sub_member_id')

    class Meta:
        managed = False
        db_table = 'tbl_campaign_send_email'


class CampaignsSendEmailArchive(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='id')
    campId = models.BigIntegerField(null=True, blank=True, db_column='camp_id')
    campSendId = models.BigIntegerField(default=0, db_column='camp_send_id')
    memberId = models.BigIntegerField(null=True, blank=True, db_column='member_id')
    email = models.CharField(max_length=500, null=True, blank=True, db_column='email')
    emailId = models.BigIntegerField(null=True, blank=True, db_column='email_id')
    isSend = models.CharField(max_length=1, default='N', db_column='is_send')
    isRead = models.CharField(max_length=1, null=True, blank=True, db_column='is_read')
    isBounced = models.CharField(max_length=1, null=True, blank=True, db_column='is_bounced')
    isUnsubscribed = models.CharField(max_length=1, null=True, blank=True, db_column='is_unsubscribed')
    firstName = models.CharField(max_length=255, null=True, blank=True, db_column='first_name')
    lastName = models.CharField(max_length=255, null=True, blank=True, db_column='last_name')
    emailDomain = models.CharField(max_length=45, null=True, blank=True, db_column='email_domain')
    csDefaultLanguage = models.CharField(max_length=255, default='en', db_column='cs_default_language')
    smtpServerHost = models.CharField(max_length=255, null=True, blank=True, db_column='smtp_server_host')
    isProcessed = models.CharField(max_length=1, default='N', db_column='is_processed')
    emailQId = models.CharField(max_length=255, null=True, blank=True, db_column='email_q_id')
    emailStatus = models.CharField(max_length=255, null=True, blank=True, db_column='email_status')
    cronStatus = models.CharField(max_length=255, default='active', db_column='cron_status')
    splitGroup = models.CharField(max_length=1, null=True, blank=True, db_column='split_group')
    groupWinner = models.CharField(max_length=1, null=True, blank=True, db_column='group_winner')
    msgPriority = models.IntegerField(default=0, db_column='msg_priority')
    subMemberId = models.BigIntegerField(default=0, db_column='sub_member_id')

    class Meta:
        managed = False
        db_table = 'tbl_campaign_send_email_archive'


class AutomationSendContact(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='id')
    campaignId = models.BigIntegerField(null=True, blank=True, db_column='campaign_id')
    status = models.CharField(max_length=255, null=True, blank=True, db_column='status')

    class Meta:
        managed = False
        db_table = 'tbl_automation_send_contact'


class CampaignLinks(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='id')
    campId = models.BigIntegerField(null=True, blank=True, db_column='camp_id')
    campLink = models.TextField(null=True, blank=True, db_column='camp_link')
    linkCount = models.IntegerField(default=0, db_column='link_count')
    splitGroup = models.CharField(max_length=1, null=True, blank=True, db_column='split_group')

    class Meta:
        managed = False
        db_table = 'tbl_campaign_links'


class CampaignLinkClick(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='id')
    userId = models.BigIntegerField(null=True, blank=True, db_column='user_id')
    linkId = models.IntegerField(db_column='link_id')
    linkCount = models.IntegerField(db_column='link_count')
    city = models.CharField(max_length=255, null=True, blank=True, db_column='City')
    clickDate = models.DateTimeField(null=True, blank=True, db_column='click_date')
    sources = models.CharField(max_length=255, null=True, blank=True, db_column='sources')
    sourceDetails = models.TextField(null=True, blank=True, db_column='source_details')

    class Meta:
        managed = False
        db_table = 'tbl_camp_link_click'


class CampaignSubscriber(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='id')
    campId = models.BigIntegerField(null=True, blank=True, db_column='camp_id')
    subId = models.BigIntegerField(null=True, blank=True, db_column='sub_id')
    totalOpen = models.BigIntegerField(null=True, blank=True, db_column='total_open')
    lastOpened = models.DateTimeField(null=True, blank=True, db_column='last_opened')
    osInfo = models.TextField(null=True, blank=True, db_column='os_info')

    class Meta:
        managed = False
        db_table = 'tbl_campaign_subscriber'










