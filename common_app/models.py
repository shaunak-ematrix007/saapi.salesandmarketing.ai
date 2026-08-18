from django.db import models
from django.utils import timezone

class Language(models.Model):
    lgId = models.BigAutoField(primary_key=True, db_column='LG_ID')
    lgDisOrder = models.BigIntegerField(null=True, blank=True, db_column='LG_DIS_ORDER')
    lgLongName = models.CharField(max_length=255, null=True, blank=True, db_column='LG_LONG_NAME')
    lgName = models.CharField(max_length=255, null=True, blank=True, db_column='LG_NAME')

    class Meta:
        managed = False
        db_table = 'LANGUAGES'

class SecurityQuestion(models.Model):
    secId = models.BigAutoField(primary_key=True, db_column='SEC_ID')
    secQuestion = models.CharField(max_length=255, null=True, blank=True, db_column='SEC_QUESTION')

    class Meta:
        managed = False
        db_table = 'SECURITY_QUESTIONS'

class Country(models.Model):
    id = models.AutoField(primary_key=True, db_column='COUNTRY_ID')
    cntCode = models.CharField(max_length=255, null=True, blank=True, db_column='CNT_CODE')
    cntName = models.CharField(max_length=80, db_column='CNTNAME')
    iso2 = models.CharField(max_length=2, null=True, blank=True, db_column='ISO2')
    longName = models.CharField(max_length=80, db_column='LONG_NAME')
    oid = models.IntegerField(null=True, blank=True, db_column='OID')
    phoneMinLength = models.IntegerField(db_column='PHONE_MIN_LENGTH')
    phoneMaxLength = models.IntegerField(db_column='PHONE_MAX_LENGTH')
    embedding = models.JSONField(null=True, blank=True, db_column='EMBEDDING')

    class Meta:
        managed = False
        db_table = 'COUNTRY'

class CountryToState(models.Model):
    countryToStateId = models.BigAutoField(primary_key=True, db_column='COUNTRY_TO_STATE_ID')
    fkCountryId = models.BigIntegerField(db_column='FK_COUNTRY_ID')
    stateCapital = models.CharField(max_length=100, null=True, blank=True, db_column='STATE_CAPITAL')
    stateLong = models.CharField(max_length=100, null=True, blank=True, db_column='STATE_LONG')
    stateShort = models.CharField(max_length=10, null=True, blank=True, db_column='STATE_SHORT')

    class Meta:
        managed = False
        db_table = 'COUNTRY_TO_STATE'

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
    id = models.BigAutoField(primary_key=True, db_column='ID')
    cntyId = models.BigIntegerField(db_column='CNTY_ID', null=True, blank=True)
    cntyISO2 = models.CharField(max_length=255, db_column='CNTY_ISO2', null=True, blank=True)
    cntyName = models.CharField(max_length=255, db_column='CNTY_NAME', null=True, blank=True)
    cntyPriceSymbol = models.CharField(max_length=255, db_column='CNTY_PRICE_SYMBOL', null=True, blank=True)
    cntyAssessmentPrice = models.FloatField(db_column='CNTY_ASSESSMENT_PRICE', default=0.0)
    cntySurveyPrice = models.FloatField(db_column='CNTY_SURVEY_PRICE', default=0.0)
    cntyIndividualPrice = models.FloatField(db_column='CNTY_INDIVIDUAL_PRICE', default=0.0)
    cntySocialMediaPrice = models.FloatField(db_column='CNTY_SOCIALMEDIA_PRICE', default=0.0)
    cntyCampaignPerPrice = models.FloatField(db_column='CNTY_CAMPAIGN_PER_PRICE', default=0.0)
    cntySurveyPerPrice = models.FloatField(db_column='CNTY_SURVEY_PER_PRICE', default=0.0)
    cntyAssessmentPerPrice = models.FloatField(db_column='CNTY_ASSESSMENT_PER_PRICE', default=0.0)
    cntyMMSPerPrice = models.FloatField(db_column='CNTY_MMS_PER_PRICE', default=0.0)
    cntySMSPerPrice = models.FloatField(db_column='CNTY_SMS_PER_PRICE', default=0.0)
    cntySMSNumberPerPrice = models.FloatField(db_column='CNTY_SMS_NUMBER_PER_PRICE', default=0.0)
    cntyFirstInvFreeAmt = models.FloatField(db_column='CNTY_FIRST_INV_FREE_AMT', default=0.0)
    cntyInvLessAmtNotCharge = models.FloatField(db_column='CNTY_INV_LESS_AMT_NOT_CHARGE', default=0.0)
    cntyTranslateCharCharge = models.FloatField(db_column='CNTY_TRANSLATE_CHAR_CHARGE', default=0.0)
    cntySMSConversationsPerPrice = models.FloatField(db_column='CNTY_SMS_CONVERSATIONS_PER_PRICE', default=0.0)
    cntyCallPerMinPrice = models.FloatField(db_column='CNTY_CALL_PERM_IN_PRICE', default=0.0)
    cntyContactsIncluded = models.BigIntegerField(db_column='CNTY_CONTACTS_INCLUDED', null=True, blank=True)
    cntyMaxNumberOfEmail = models.BigIntegerField(db_column='CNTY_MAX_NUMBER_OF_EMAIL', null=True, blank=True)
    cntyPlanId = models.BigIntegerField(db_column='CNTY_PLAN_ID', null=True, blank=True)
    cntyPlanPrice = models.FloatField(db_column='CNTY_PLAN_PRICE', default=0.0)
    cntySupport = models.TextField(db_column='CNTY_SUPPORT', null=True, blank=True)
    cntyMultiUser = models.CharField(max_length=255, db_column='CNTY_MULTI_USER', null=True, blank=True)
    cntyAutomation = models.CharField(max_length=255, db_column='CNTY_AUTOMATION', null=True, blank=True)
    cntyWhiteListing = models.CharField(max_length=255, db_column='CNTY_WHITE_LISTING', null=True, blank=True)
    cntyCalendar = models.CharField(max_length=255, db_column='CNTY_CALENDAR', null=True, blank=True)
    cntyZoomConferences = models.CharField(max_length=255, db_column='CNTY_ZOOM_CONFERENCES', null=True, blank=True)
    cntySocialMedia = models.CharField(max_length=255, db_column='CNTY_SOCIAL_MEDIA', null=True, blank=True)
    cntySmsInbox = models.CharField(max_length=255, db_column='CNTY_SMS_INBOX', null=True, blank=True)
    cntyAbTesting = models.CharField(max_length=255, db_column='CNTY_AB_TESTING', null=True, blank=True)
    cntyPlanPopular = models.CharField(max_length=255, db_column='CNTY_PLAN_POPULAR', null=True, blank=True)
    cntyPlanDisplayOrder = models.IntegerField(db_column='CNTY_PLAN_DISPLAY_ORDER', null=True, blank=True)
    cntyFormResponse = models.FloatField(db_column='CNTY_FORM_RESPONSE', default=0.0)
    cntyAdditionalContacts = models.IntegerField(db_column='CNTY_ADDITIONAL_CONTACTS', null=True, blank=True)
    cntyAdditionalContactsPrice = models.FloatField(db_column='CNTY_ADDITIONAL_CONTACTS_PRICE', default=0.0)
    cnty10DLCPrice = models.FloatField(db_column='CNTY_10DLC_PRICE', default=0.0)
    cnty10DLCCampaignTypeCharge = models.FloatField(db_column='CNTY_10DLC_CAMPAIGN_TYPE_CHARGE', default=0.0)
    cnty10DLCOtherCharge = models.FloatField(db_column='CNTY_10DLC_OTHER_CHARGE', default=0.0)
    cntyWarmupPrice = models.FloatField(db_column='CNTY_WARMUP_PRICE', default=0.0)
    ctnyAiGeneratedImage = models.FloatField(db_column='CTNY_AI_GENERATED_IMAGE', default=0.0)
    ctnyAiEditedImage = models.FloatField(db_column='CTNY_AI_EDITED_IMAGE', default=0.0)
    ctnyContactPerPrice = models.FloatField(db_column='CTNY_CONTACT_PER_PRICE', default=0.0)
    cntyLinkExpiryDateTime = models.DateTimeField(db_column='CNTY_LINK_EXPIRY_DATETIME', null=True, blank=True)
    cntyUpdateDateTime = models.DateTimeField(db_column='CNTY_UPDATE_DATETIME', null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'COUNTRY_SETTING'

class CampaignsEmail(models.Model):
    campId = models.BigAutoField(primary_key=True, db_column='CE_ID')
    byAutoManual = models.CharField(max_length=10, null=True, blank=True, db_column='CE_BY_AUTO_MANUAL')
    byMeasure = models.CharField(max_length=10, null=True, blank=True, db_column='CE_BY_MEASURE')
    byNumber = models.IntegerField(null=True, blank=True, db_column='CE_BY_NUMBER')
    byType = models.CharField(max_length=10, null=True, blank=True, db_column='CE_BY_TYPE')
    campDetail = models.TextField(db_column='CE_DETAIL')
    campDetailB = models.TextField(null=True, blank=True, db_column='CE_DETAIL_B')
    campMainType = models.IntegerField(null=True, blank=True, db_column='CE_MAIN_TYPE')
    campName = models.TextField(db_column='CE_CAMP_NAME')
    campStatus = models.IntegerField(null=True, blank=True, db_column='CE_STATUS')
    campType = models.IntegerField(db_column='CE_CAMP_TYPE')
    fromAdd = models.CharField(max_length=255, db_column='CE_FROM_ADD')
    fromName = models.CharField(max_length=255, null=True, blank=True, db_column='CE_FROM_NAME')
    fromNameB = models.CharField(max_length=255, null=True, blank=True, db_column='CE_FROM_NAME_B')
    groupList = models.TextField(db_column='CE_GROUP_LIST')
    incrementalUpdates = models.CharField(max_length=10, null=True, blank=True, db_column='CE_INCREMENTAL_UPDATES')
    mailType = models.CharField(max_length=255, null=True, blank=True, db_column='CE_MAIL_TYPE')
    memberList = models.TextField(null=True, blank=True, db_column='CE_MEMBER_LIST')
    mypageId = models.BigIntegerField(null=True, blank=True, db_column='CE_MY_PAGE_ID')
    mypageIdB = models.BigIntegerField(null=True, blank=True, db_column='CE_MY_PAGE_ID_B')
    remainGroupPer = models.IntegerField(null=True, blank=True, db_column='CE_REMAIN_GROUP_PER')
    replyToAdd = models.CharField(max_length=255, db_column='CE_REPLY_TO_ADD')
    resultTie = models.CharField(max_length=10, null=True, blank=True, db_column='CE_RESULT_TIE')
    scheduleType = models.IntegerField(null=True, blank=True, db_column='CE_SCHEDULE_TYPE')
    scheduleTypeB = models.IntegerField(null=True, blank=True, db_column='CE_SCHEDULE_TYPE_B')
    segId = models.BigIntegerField(null=True, blank=True, db_column='CE_SEGID')
    selectGroupPer = models.IntegerField(null=True, blank=True, db_column='CE_SELECT_GROUP_PER')
    sendDate = models.DateTimeField(db_column='CE_SEND_DATE')
    sendOnDate = models.DateTimeField(null=True, blank=True, db_column='CE_SEND_ON_DATE')
    sendOnDateB = models.DateTimeField(null=True, blank=True, db_column='CE_SEND_ON_DATE_B')
    sendOnTime = models.TimeField(null=True, blank=True, db_column='CE_SEND_ON_TIME')
    sendOnTimeB = models.TimeField(null=True, blank=True, db_column='CT_TRAN_CAMPAIGN_NAME')
    subject = models.CharField(max_length=255, db_column='CE_SUBJECT')
    subjectB = models.CharField(max_length=255, null=True, blank=True, db_column='CE_SUBJECT_B')
    testingType = models.IntegerField(null=True, blank=True, db_column='CE_TESTING_TYPE')
    tries = models.IntegerField(null=True, blank=True, db_column='CE_TRIES')
    triesCount = models.IntegerField(null=True, blank=True, db_column='CE_TRIES_COUNT')
    memberId = models.BigIntegerField(db_column='CE_CLIENT_ID')
    archiveYn = models.CharField(max_length=1, default='N', db_column='CE_ARCHIVE_YN')
    embedding = models.JSONField(null=True, blank=True, db_column='CE_TRANS_EMBEDDING')

    class Meta:
        managed = False
        db_table = 'CAMPAIGN_EMAILS'

class Userlist(models.Model):
    emailId = models.BigAutoField(primary_key=True, db_column='UL_EMAIL_ID')
    evId = models.BigIntegerField(db_column='UL_EV_ID', default=0, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True, db_column='UL_EMAIL')
    firstName = models.CharField(max_length=255, null=True, blank=True, db_column='UL_FIRST_NAME')
    lastName = models.CharField(max_length=255, null=True, blank=True, db_column='UL_LAST_NAME')
    phoneNumber = models.CharField(max_length=255, null=True, blank=True, db_column='UL_PHONE_NUMBER')
    udf1 = models.CharField(max_length=255, null=True, blank=True, db_column='UL_UDF1')
    udf2 = models.CharField(max_length=255, null=True, blank=True, db_column='UL_UDF2')
    udf3 = models.CharField(max_length=255, null=True, blank=True, db_column='UL_UDF3')
    udf4 = models.CharField(max_length=255, null=True, blank=True, db_column='UL_UDF4')
    udf5 = models.CharField(max_length=255, null=True, blank=True, db_column='UL_UDF5')
    udf6 = models.CharField(max_length=255, null=True, blank=True, db_column='UL_UDF6')
    udf7 = models.CharField(max_length=255, null=True, blank=True, db_column='UL_UDF7')
    udf8 = models.CharField(max_length=255, null=True, blank=True, db_column='UL_UDF8')
    udf9 = models.CharField(max_length=255, null=True, blank=True, db_column='UL_UDF9')
    udf10 = models.CharField(max_length=255, null=True, blank=True, db_column='UL_UDF10')
    groupId = models.BigIntegerField(db_column='UL_GROUP_ID', default=0, null=True, blank=True)
    memberId = models.BigIntegerField(db_column='UL_CLIENT_ID', default=0,null=True, blank=True)
    status = models.CharField(max_length=255, db_column='UL_STATUS', default='Yes', null=True, blank=True)
    smsStatus = models.CharField(max_length=255, db_column='UL_SMS_STATUS', default='Subscribed',null=True, blank=True)
    badEmail = models.CharField(max_length=1, db_column='UL_BAD_EMAIL', default='N')
    badPhoneNumber = models.CharField(max_length=1, db_column='UL_BAD_PHONE_NUMBER', default='N')
    optId = models.BigIntegerField(db_column='UL_OPT_ID', null=True, blank=True)
    bounceReason = models.TextField(null=True, blank=True, db_column='UL_BOUNCE_REASON')
    tempCronId = models.BigIntegerField(null=True, blank=True, db_column='UL_TEMP_CRON_ID')
    smsSid = models.CharField(max_length=255, null=True, blank=True, db_column='UL_SMS_ID')
    streetAddress1 = models.TextField(null=True, blank=True, db_column='UL_STREET_ADDRESS1')
    streetAddress2 = models.TextField(null=True, blank=True, db_column='UL_STREET_ADDRESS2')
    fullName = models.CharField(max_length=255, null=True, blank=True, db_column='UL_FULL_NAME')
    phone = models.CharField(max_length=255, null=True, blank=True, db_column='UL_PHONE')
    city = models.CharField(max_length=255, null=True, blank=True, db_column='UL_CITY')
    stateProvRegion = models.CharField(max_length=255, null=True, blank=True, db_column='UL_STATE_PROV_REGION')
    zipPostalCode = models.CharField(max_length=255, null=True, blank=True, db_column='UL_ZIP_POSTAL_CODE')
    country = models.CharField(max_length=255, null=True, blank=True, db_column='UL_COUNTRY')
    birthday = models.CharField(max_length=255, null=True, blank=True, db_column='UL_BIRTHDAY')
    gender = models.CharField(max_length=255, null=True, blank=True, db_column='UL_GENDER')
    emailVerificationStatus = models.CharField(max_length=255, null=True, blank=True, default='done',db_column='UL_EMAIL_VERIFICATION_STATUS')
    tags = models.TextField(null=True, blank=True, db_column='UL_TAGS')
    emailDomain = models.CharField(max_length=255, null=True, blank=True, db_column='UL_EMAIL_DOMAIN')
    usDefaultLanguage = models.CharField(max_length=255, null=True, blank=True, default='en',db_column='UL_US_DEFAULT_LANGUAGE')
    isEmailValidate = models.CharField(max_length=255, null=True, blank=True, default='N', db_column='UL_IS_EMAIL_VALIDATE')
    isPhoneValidate = models.CharField(max_length=1, null=True, blank=True, default='N',db_column='UL_IS_PHONE_NUMBER_VALIDATE')
    smtpHost = models.CharField(max_length=255, null=True, blank=True, db_column='UL_SMTP_HOST')
    dateRegistered = models.DateTimeField(null=True, blank=True, db_column='UL_DATE_REGISTERED')
    optDate = models.DateTimeField(null=True, blank=True, db_column='UL_OPT_DATE')
    optBackInDate = models.DateTimeField(null=True, blank=True, db_column='UL_OPT_BACK_IN_DATE')
    optOutDate = models.DateTimeField(null=True, blank=True, db_column='UL_OPT_OUT_DATE')
    dateAdded = models.DateTimeField(null=True, blank=True, db_column='UL_DATE_ADDED')
    dateLastModified = models.DateTimeField(null=True, blank=True, db_column='UL_DATE_LAST_MODIFIED')
    typeEmail = models.CharField(max_length=255, null=True, blank=True, default='done', db_column='UL_TYPE_EMAIL')
    typeSms = models.CharField(max_length=255, null=True, blank=True, default='done', db_column='UL_TYPE_SMS')
    sendToEmailVerification = models.CharField(max_length=255, default='No', db_column='UL_SEND_TO_EMAIL_VERIFICATION')
    embedding = models.JSONField(null=True, blank=True, db_column='UL_EMBEDDING')

    class Meta:
        managed = False
        db_table = 'tbl_userlist'

class Udf(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='UDF_ID')
    groupId = models.BigIntegerField(db_column='UDF_GROUP_ID')
    udf = models.CharField(max_length=255, db_column='UDF_UDF')
    udfLabel = models.IntegerField(db_column='UDF_UDF_LABEL')
    udfCol = models.CharField(max_length=45, db_column='UDF_UDFCOL')

    class Meta:
        managed = False
        db_table = 'UDFS'

class CampaignTransaction(models.Model):
    tranId = models.BigAutoField(primary_key=True, db_column='CT_TRANS_ID')
    tranCampaignId = models.BigIntegerField(db_column='CT_TRAN_CAMPAIGN_ID')
    tranCampaignName = models.CharField(max_length=255, db_column='CT_TRAN_CAMPAIGN_NAME')
    tranCampaignDate = models.DateTimeField(db_column='CT_TRAN_CAMPAIGN_DATE')
    tranTotalMember = models.BigIntegerField(db_column='CT_TRAN_TOTAL_MEMBER')
    tranType = models.CharField(max_length=255, db_column='CT_TRAN_TYPE')
    tranInvoicedId = models.BigIntegerField(db_column='CT_TRAN_INVOICED_ID')
    tranInvoicedStatus = models.CharField(max_length=255, db_column='CT_TRAN_INVOICED_STATUS')
    tranInvoicedDate = models.DateField(null=True, blank=True, db_column='CT_TRAN_INVOICED_DATE')
    memberId = models.BigIntegerField(db_column='CT_CLIENT_ID')
    tranBillType = models.CharField(max_length=255, db_column='CT_TRAN_BILL_TYPE', default='0')
    tranTotalAmount = models.FloatField(db_column='CT_TRAN_TOTAL_AMOUNT')
    tranMemberRate = models.FloatField(db_column='CT_TRAN_MEMBER_RATE')
    tranCountTotalSms = models.BigIntegerField(db_column='CT_TRAN_COUNT_TOTAL_SMS')
    tranPollFormNo = models.CharField(max_length=255, null=True, blank=True, db_column='CT_TRAN_POLL_FORM_NO')
    tranPollToNo = models.CharField(max_length=255, null=True, blank=True, db_column='CT_TRAN_POLL_TO_NO')
    subMemberId = models.BigIntegerField(db_column='SUB_MEMBER_ID', default=0)
    transEmbedding = models.JSONField(null=True, blank=True, db_column='CT_TRAN_EMBEDDING')

    class Meta:
        managed = False
        db_table = 'CAMPAIGN_BILLING'

class Admin(models.Model):
    memberId = models.BigAutoField(primary_key=True, db_column='MEMBER_ID')
    userName = models.CharField(max_length=255, db_column='USER_NAME')
    password = models.CharField(max_length=255, db_column='PASSWORD')
    firstName = models.CharField(max_length=255, null=True, blank=True, db_column='FIRST_NAME')
    lastName = models.CharField(max_length=255, null=True, blank=True, db_column='LAST_NAME')
    email = models.CharField(max_length=255, db_column='EMAIL')
    active = models.CharField(max_length=1, default='Y', db_column='ACTIVE')
    dateRegistered = models.DateTimeField(null=True, blank=True, db_column='DATE_REGISTERED')
    lastLoggedIn = models.DateTimeField(null=True, blank=True, db_column='LAST_LOGGEDIN')
    userType = models.IntegerField(db_column='USERTYPE')

    @property
    def is_authenticated(self):
        return True

    class Meta:
        managed = False
        db_table = 'tbl_admin'

class AdminType(models.Model):
    styId = models.BigAutoField(primary_key=True, db_column='ATY_ID')
    styName = models.CharField(max_length=255, db_column='ATY_NAME')
    styCreatedDate = models.DateTimeField(null=True, blank=True, db_column='ATY_CREATED_DATE')

    class Meta:
        managed = False
        db_table = 'ADMIN_TYPE'

class AffiliateProgram(models.Model):
    apId = models.BigAutoField(primary_key=True, db_column='AFF_PID')
    apTitle = models.CharField(max_length=255, db_column='AFF_PTITLE')
    apCommission = models.FloatField(db_column='AFF_PCOMMISSION')
    apCommissionType = models.IntegerField(db_column='AFF_PCOMMISSION_TYPE', default=1)
    apCode = models.CharField(max_length=255, db_column='AFF_PCODE', null=True, blank=True)
    apIsActive = models.CharField(max_length=255, db_column='AFF_PIS_ACTIVE', default='N')
    apDate = models.DateTimeField(db_column='ap_date', null=True, blank=True)
    apExpiryDate = models.DateField(db_column='ap_expiry_date', null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'AFFILIATE_PROGRAM'

class AdminPage(models.Model):
    pgId = models.BigAutoField(primary_key=True, db_column='PG_ID')
    pgName = models.CharField(max_length=255, null=True, blank=True, db_column='PG_NAME')
    pgMenuName = models.CharField(max_length=255, null=True, blank=True, db_column='PG_MENU_NAME')
    pgModuleName = models.CharField(max_length=255, null=True, blank=True, db_column='PG_MODULE_NAME')

    class Meta:
        managed = False
        db_table = 'ADMIN_PAGE'

class AdminPageDetails(models.Model):
    pgdId = models.BigAutoField(primary_key=True, db_column='PGD_ID')
    pgdPgId = models.BigIntegerField(null=True, blank=True, db_column='PGD_PG_ID')
    pgdActionName = models.CharField(max_length=255, null=True, blank=True, db_column='PGD_ACTION_NAME')

    class Meta:
        managed = False
        db_table = 'ADMIN_PAGE_DETAILS'


class AdminPagePermission(models.Model):
    perId = models.BigAutoField(primary_key=True, db_column='PER_ID')
    perPgId = models.BigIntegerField(null=True, blank=True, db_column='PER_PG_ID')
    perActionName = models.CharField(max_length=255, null=True, blank=True, db_column='PER_ACTION_NAME')
    perStyId = models.BigIntegerField(null=True, blank=True, db_column='PER_STY_ID')
    perMemberId = models.BigIntegerField(null=True, blank=True, db_column='PER_MEMBER_ID')

    class Meta:
        managed = False
        db_table = 'ADMIN_PAGE_PERMISSION'


class CampaignsEmailSend(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='CEQ_ID')
    byAutoManual = models.CharField(max_length=10, null=True, blank=True, db_column='CEQ_BY_AUTO_MANUAL')
    byMeasure = models.CharField(max_length=10, null=True, blank=True, db_column='CEQ_BY_MEASURE')
    byNumber = models.IntegerField(null=True, blank=True, db_column='CEQ_BY_NUMBER')
    byType = models.CharField(max_length=10, null=True, blank=True, db_column='CEQ_BY_TYPE')
    campDetail = models.TextField(null=True, blank=True, db_column='CEQ_CAMP_DETAIL')
    campDetailB = models.TextField(null=True, blank=True, db_column='CEQ_CAMP_DETAIL_B')
    campId = models.IntegerField(null=True, blank=True, db_column='CEQ_CAMP_ID')
    campMainType = models.IntegerField(null=True, blank=True, db_column='CEQ_CAMP_MAIN_TYPE')
    campName = models.TextField(db_column='CEQ_CAMP_NAME')
    campType = models.IntegerField(default=0, db_column='CEQ_CAMP_TYPE')
    emailEndTime = models.DateTimeField(null=True, blank=True, db_column='CEQ_EMAIL_END_TIME')
    emailServerIp = models.CharField(max_length=255, null=True, blank=True, db_column='CEQ_EMAIL_SERVER_IP')
    emailStartTime = models.DateTimeField(null=True, blank=True, db_column='CEQ_EMAIL_START_TIME')
    fromAdd = models.CharField(max_length=255, db_column='CEQ_FROM_ADD')
    fromName = models.CharField(max_length=255, null=True, blank=True, db_column='CEQ_FROM_NAME')
    fromNameB = models.CharField(max_length=255, null=True, blank=True, db_column='CEQ_FROM_NAME_B')
    groupList = models.TextField(db_column='CEQ_GROUPLIST')
    incrementalUpdates = models.CharField(max_length=10, null=True, blank=True, db_column='CEQ_INCREMENTAL_UPDATES')
    isCompletedAB = models.CharField(max_length=1, default='N', db_column='CEQ_IS_COMPLETED_AB')
    lastOpened = models.DateTimeField(null=True, blank=True, db_column='CEQ_LAST_OPENED')
    mailType = models.CharField(max_length=255, default='Newsletter', db_column='CEQ_MAIL_TYPE')
    mypageId = models.BigIntegerField(null=True, blank=True, db_column='CEQ_MY_PAGE_ID')
    mypageIdB = models.BigIntegerField(null=True, blank=True, db_column='CEQ_MY_PAGE_ID_B')
    readyToMail = models.CharField(max_length=1, default='N', db_column='CEQ_READY_TO_MAIL')
    remaingroupper = models.IntegerField(null=True, blank=True, db_column='CEQ_REMAIN_GROUP_PER')
    replyToAdd = models.CharField(max_length=255, db_column='CEQ_REPLY_TO_ADD')
    resultTie = models.CharField(max_length=10, null=True, blank=True, db_column='CEQ_RESULT_TIE')
    scheduleTypeB = models.IntegerField(null=True, blank=True, db_column='CEQ_SCHEDULE_TYPE_B')
    selectgroupper = models.IntegerField(null=True, blank=True, db_column='CEQ_SELECT_GROUP_PER')
    sendDate = models.DateTimeField(db_column='CEQ_SEND_DATE')
    sendOnDate = models.DateTimeField(null=True, blank=True, db_column='CEQ_SEND_ON_DATE')
    sendOnDateB = models.DateTimeField(null=True, blank=True, db_column='CEQ_SEND_ON_DATE_B')
    sendOnTime = models.DurationField(null=True, blank=True, db_column='CEQ_SEND_ON_TIME')
    sendOnTimeB = models.DurationField(null=True, blank=True, db_column='CEQ_SEND_ON_TIME_B')
    subject = models.CharField(max_length=255, db_column='CEQ_SUBJECT')
    subjectB = models.CharField(max_length=255, null=True, blank=True, db_column='CEQ_SUBJECT_B')
    testingType = models.IntegerField(null=True, blank=True, db_column='CEQ_TESTING_TYPE')
    tries = models.IntegerField(null=True, blank=True, db_column='CEQ_TRIES')
    triesCount = models.IntegerField(null=True, blank=True, db_column='CEQ_TRIES_COUNT')
    unsubscribeUid = models.TextField(null=True, blank=True, db_column='CEQ_UNSUBSCRIBE_UID')
    memberId = models.BigIntegerField(db_column='CEQ_CLIENT_ID', null=True, blank=True)
    isProccessedByLoadbalancer = models.IntegerField(default=0, db_column='CEQ_IS_PROCCESSED_BY_LOADBALANCER')
    archiveYn = models.CharField(max_length=1, default='N', db_column='CEQ_ARCHIVE_YN')
    totalQueued = models.IntegerField(default=0, db_column='CEQ_TOTAL_QUEUED')
    totalQueuedB = models.IntegerField(default=0, db_column='CEQ_TOTAL_QUEUED_B')
    totalQueuedO = models.IntegerField(default=0, db_column='CEQ_TOTAL_QUEUED_O')
    retrySendDateTime = models.DateTimeField(null=True, blank=True, db_column='CEQ_RETRY_SEND_DATE_TIME')
    maxBounceEmail = models.IntegerField(default=0, db_column='CEQ_MAX_BOUNCE_EMAIL')
    retrySendCount = models.IntegerField(default=0, db_column='CEQ_RETRY_SEND_COUNT')
    throttling = models.CharField(max_length=1, null=True, blank=True, db_column='CEQ_THROTTLING')
    throttlingType = models.CharField(max_length=500, null=True, blank=True, db_column='CEQ_THROTTLING_TYPE')
    throttlingValue = models.IntegerField(null=True, blank=True, db_column='CEQ_THROTTLING_VALUE')
    throttlingNextDate = models.DateTimeField(null=True, blank=True, db_column='CEQ_THROTTLING_NEXT_DATE')
    stopStatus = models.TextField(null=True, blank=True, db_column='CEQ_STOP_STATUS')
    embedding = models.JSONField(null=True, blank=True, db_column='CEQ_TRANS_EMBEDDING')

    class Meta:
        managed = False
        db_table = 'CAMPAIGN_EMAIL_QUEUED'




class SmtpServer(models.Model):
    serverId = models.AutoField(primary_key=True, db_column='SS_ID')
    serverName = models.CharField(max_length=45, null=True, blank=True, db_column='SS_SERVER_NAME')
    serverStatus = models.CharField(max_length=10, null=True, blank=True, db_column='SS_SERVER_STATUS')
    serverDomain = models.CharField(max_length=255, null=True, blank=True, db_column='SS_SERVER_DOMAIN')
    capacityHr = models.BigIntegerField(null=True, blank=True, db_column='SS_CAPACITY_HR')
    capacityDay = models.BigIntegerField(null=True, blank=True, db_column='SS_CAPACITY_DAY')
    weightHr = models.BigIntegerField(null=True, blank=True, db_column='SS_WEIGHT_HR')
    weightDay = models.BigIntegerField(null=True, blank=True, db_column='SS_WEIGHT_DAY')
    reactiveTime = models.DateTimeField(null=True, blank=True, db_column='SS_REACTIVE_TIME')
    activeDate = models.DateField(null=True, blank=True, db_column='SS_ACTIVE_DATE')
    location = models.CharField(max_length=255, null=True, blank=True, db_column='SS_LOCATION')
    country = models.CharField(max_length=255, null=True, blank=True, db_column='SS_COUNTRY')
    threads = models.IntegerField(null=True, blank=True, db_column='SS_THREADS')
    mps = models.FloatField(null=True, blank=True, db_column='SS_MPS')
    isActive = models.IntegerField(db_column='SS_IS_ACTIVE')
    pctFailure = models.FloatField(null=True, blank=True, db_column='SS_PCT_FAILURE_10MIN')
    currentFailureRate = models.FloatField(null=True, blank=True, db_column='SS_CURRENT_FAILURE_RATE')
    qThresold = models.CharField(max_length=45, null=True, blank=True, db_column='SS_Q_THRESHOLD')
    isDedicatedIp = models.CharField(max_length=1, default='N',null=True, blank=True, db_column='SS_IS_DEDICATED_IP')
    clientId = models.BigIntegerField(default=0, db_column='SS_CLIENT_ID')
    relayerStatus = models.CharField(max_length=50, null=True, blank=True, db_column='SS_RELAYER_STATUS')
    privateIp = models.CharField(max_length=255, null=True, blank=True, db_column='SS_PRIVATE_IP')
    ociId = models.CharField(max_length=255, null=True, blank=True, db_column='SS_OCI_ID')

    class Meta:
        managed = False
        db_table = 'SMTP_SERVERS'


class SubaccountPage(models.Model):
    pgId = models.BigAutoField(primary_key=True, db_column='SP_ID')
    pgName = models.CharField(max_length=255, null=True, blank=True, db_column='SP_NAME')
    pgMenuName = models.CharField(max_length=255, null=True, blank=True, db_column='SP_MENU_NAME')
    pgModuleName = models.CharField(max_length=255, null=True, blank=True, db_column='SP_MODULE_NAME')

    class Meta:
        managed = False
        db_table = 'SUBACCOUNT_PAGE'


class SubaccountPageDetails(models.Model):
    pgdId = models.BigAutoField(primary_key=True, db_column='SPD_ID')
    pgdPgId = models.BigIntegerField(null=True, blank=True, db_column='SPD_SP_ID')
    pgdActionName = models.CharField(max_length=255, null=True, blank=True, db_column='SPD_ACTION_NAME')

    class Meta:
        managed = False
        db_table = 'SUBACCOUNT_PAGE_DETAILS'


class FreeTemplate(models.Model):
    ftId = models.BigAutoField(primary_key=True, db_column='FT_ID')
    ftName = models.CharField(max_length=255, null=True, blank=True, db_column='FT_NAME')
    ftFolderName = models.CharField(max_length=255, null=True, blank=True, db_column='FT_FOLDERNAME')
    ftStage = models.IntegerField(db_column='FT_STAGE')
    ftCatId = models.BigIntegerField(null=True, blank=True, db_column='FT_CAT_ID')
    ftTags = models.TextField(null=True, blank=True, db_column='FT_TAGS')

    class Meta:
        managed = False
        db_table = 'FREE_TEMPLATE'


class Invoice(models.Model):
    invId = models.BigAutoField(primary_key=True, db_column='INV_ID')
    invNo = models.BigIntegerField(default=0, db_column='INV_NO')
    invAdjustmentsAmount = models.FloatField(default=0.0, db_column='INV_ADJUSTMENTS_AMOUNT')
    invAssessmentAmount = models.FloatField(default=0.0, db_column='INV_ASSESSMENT_AMOUNT')
    invAssessmentPrice = models.FloatField(default=0.0, db_column='INV_ASSESSMENT_PRICE')
    invBuildItForMeAmount = models.FloatField(default=0.0, db_column='INV_BUILD_IT_FOR_ME_AMOUNT')
    invBuildItForMePrice = models.FloatField(default=0.0, db_column='INV_BUILD_IT_FOR_ME_PRICE')
    invCallAmount = models.FloatField(default=0.0, db_column='INV_CALL_AMOUNT')
    invCallPrice = models.FloatField(default=0.0, db_column='INV_CALL_PRICE')
    invCampaignAmount = models.FloatField(default=0.0, db_column='INV_CAMPAIGN_AMOUNT')
    invCampaignPrice = models.FloatField(default=0.0, db_column='INV_CAMPAIGN_PRICE')
    invClientName = models.CharField(max_length=255, null=True, blank=True, db_column='INV_CLIENT_NAME')
    invCountryId = models.BigIntegerField(default=100, db_column='INV_COUNTRY_ID')
    invCurrentContacts = models.BigIntegerField(default=0, db_column='INV_CURRENT_CONTACTS')
    invDate = models.DateField(null=True, blank=True, db_column='INV_DATE')
    invIndividualAmount = models.FloatField(default=0.0, db_column='INV_INDIVIDUAL_AMOUNT')
    invIndividualPrice = models.FloatField(default=0.0, db_column='INV_INDIVIDUAL_PRICE')
    invMonthlyEmailAmount = models.FloatField(default=0.0, db_column='INV_MONTHLY_EMAIL_AMOUNT')
    invMonthlyIndividualAmount = models.FloatField(default=0.0, db_column='INV_MONTHLY_INDIVIDUAL_AMOUNT')
    invMonthlySmsAmount = models.FloatField(default=0.0, db_column='INV_MONTHLY_SMS_AMOUNT')
    invMonthlySocialMediaAmount = models.FloatField(default=0.0, db_column='INV_MONTHLY_SOCIAL_MEDIA_AMOUNT')
    invMonthlySurveyAmount = models.FloatField(default=0.0, db_column='INV_MONTHLY_SURVEY_AMOUNT')
    invMonthlyYN = models.CharField(max_length=1, default='N', db_column='INV_MONTHLY_YN')
    invPageTransAmount = models.FloatField(default=0.0, db_column='INV_PAGE_TRANS_AMOUNT')
    invPageTransPrice = models.FloatField(default=0.0, db_column='INV_PAGE_TRANS_PRICE')
    invPayCardNo = models.CharField(max_length=255, null=True, blank=True, db_column='INV_PAY_CARDNO')
    invSendMail = models.CharField(max_length=1, null=True, blank=True, db_column='INV_SEND_MAIL')
    invSmsAmount = models.FloatField(default=0.0, db_column='INV_SMS_AMOUNT')
    invSMSConversationsAmount = models.FloatField(default=0.0, db_column='INV_SMS_CONVERSATIONS_AMOUNT')
    invSMSConversationsPrice = models.FloatField(default=0.0, db_column='INV_SMS_CONVERSATIONS_PRICE')
    invSmsPollAmount = models.FloatField(default=0.0, db_column='INV_SMS_POLL_AMOUNT')
    invSmsPollPrice = models.FloatField(default=0.0, db_column='INV_SMS_POLL_PRICE')
    invSmsPrice = models.FloatField(default=0.0, db_column='INV_SMS_PRICE')
    invSocialMediaAmount = models.FloatField(default=0.0, db_column='INV_SOCIAL_MEDIA_AMOUNT')
    invSocialMediaPrice = models.FloatField(default=0.0, db_column='INV_SOCIAL_MEDIA_PRICE')
    invSubTotal = models.FloatField(default=0.0, db_column='INV_SUBTOTAL')
    invSurveyAmount = models.FloatField(default=0.0, db_column='INV_SURVEY_AMOUNT')
    invSurveyPrice = models.FloatField(default=0.0, db_column='INV_SURVEY_PRICE')
    invTotalAmount = models.FloatField(default=0.0, db_column='INV_TOTAL_AMOUNT')
    invTransationId = models.CharField(max_length=500, null=True, blank=True, db_column='INV_TRANSATION_ID')
    memberId = models.BigIntegerField(default=0, db_column='INV_CLIENT_ID')
    invTenantId = models.BigIntegerField(default=0, db_column='INV_TENANT_ID')
    invPlanId = models.BigIntegerField(default=0, db_column='INV_PLAN_ID')
    invPlanName = models.CharField(max_length=255, null=True, blank=True, db_column='INV_PLAN_NAME')
    invPlanPrice = models.FloatField(default=0.0, db_column='INV_PLAN_PRICE')
    invShareAppointmentAmount = models.FloatField(default=0.0, db_column='INV_SHARE_APPOINTMENT_AMOUNT')
    invSmsCalendarAmount = models.FloatField(default=0.0, db_column='INV_SMS_CALENDAR_AMOUNT')
    invShareAppointmentPrice = models.FloatField(default=0.0, db_column='INV_SHARE_APPOINTMENT_PRICE')
    invSmsCalendarPrice = models.FloatField(default=0.0, db_column='INV_SMS_CALENDAR_PRICE')
    invSmsCalendarReminderAmount = models.FloatField(default=0.0, db_column='INV_SMS_CALENDAR_REMINDER_AMOUNT')
    invSmsCalendarReminderPrice = models.FloatField(default=0.0, db_column='INV_SMS_CALENDAR_REMINDER_PRICE')
    invPreviousUninvoicedAmount = models.FloatField(default=0.0, db_column='INV_PREVIOUS_UNINVOICED_AMOUNT')
    invPreviousUninvoicedPrice = models.FloatField(default=0.0, db_column='INV_PREVIOUS_UNINVOICED_PRICE')
    invAdditionalContactsAmount = models.FloatField(default=0.0, db_column='INV_ADDITIONAL_CONTACTS_AMOUNT')
    invAiAmount = models.FloatField(default=0.0, db_column='INV_AI_AMOUNT')
    invAiPrice = models.FloatField(default=0.0, db_column='INVAI_PRICE')
    invPerContactPrice = models.FloatField(default=0.0, db_column='INV_PER_CONTACT_PRICE')
    invAdditionalContactsPrice = models.FloatField(default=0.0, db_column='INV_ADDITIONAL_CONTACTS_PRICE')
    inv10DLCAmount = models.FloatField(default=0.0, db_column='INV_10DLC_AMOUNT')
    invWarmupAmount = models.FloatField(default=0.0, db_column='INV_WARMUP_AMOUNT')
    invEmailVerificationAmount = models.FloatField(default=0.0, db_column='INV_EMAIL_VERIFICATION_AMOUNT')
    invEmailVerificationPrice = models.FloatField(default=0.0, db_column='INV_EMAIL_VERIFICATION_PRICE')
    invEmbedding = models.JSONField(null=True, blank=True, db_column='INV_EMBEDDING')

    class Meta:
        managed = False
        db_table = 'INVOICES'


class Plan(models.Model):
    planId = models.BigAutoField(primary_key=True, db_column='PLAN_ID')
    planName = models.CharField(max_length=255, db_column='PLAN_NAME')
    planActive = models.CharField(max_length=255, db_column='PLAN_ACTIVE')
    planVisibility = models.CharField(max_length=255, default='Public', db_column='PLAN_VISIBILITY')
    planAddedDate = models.DateTimeField(db_column='PLAN_ADDED_DATE', null=True, blank=True)
    planPmIdList = models.CharField(max_length=255, db_column='PLAN_PM_ID_LIST', null=True, blank=True)
    planBeginDate = models.DateTimeField(db_column='PLAN_BEGIN_DATE', null=True, blank=True)
    planEndDate = models.DateTimeField(db_column='PLAN_END_DATE', null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'PLANS'


class Settings(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='ID')
    adminName = models.CharField(max_length=255, db_column='ADMIN_NAME')
    adminEmail = models.CharField(max_length=255, db_column='ADMIN_EMAIL')
    facebookLink = models.CharField(max_length=255, db_column='FACEBOOK_LINK', null=True, blank=True)
    twitterLink = models.CharField(max_length=255, db_column='TWITTER_LINK', null=True, blank=True)
    gplusLink = models.CharField(max_length=255, db_column='GPLUS_LINK', null=True, blank=True)
    linkinLink = models.CharField(max_length=255, db_column='LINKIN_LINK', null=True, blank=True)
    siteOnOff = models.CharField(max_length=255, db_column='SITE_ON_OFF')
    logoName = models.CharField(max_length=255, db_column='LOGO_NAME')
    logoSystemName = models.CharField(max_length=255, db_column='LOGO_SYSTEM_NAME')
    paymentSwitch = models.CharField(max_length=255, db_column='PAYMENT_SWITCH')
    billPeriod = models.CharField(max_length=255, db_column='BILL_PERIOD')
    assessmentPrice = models.FloatField(db_column='ASSESSMENTPRICE')
    surveyPrice = models.FloatField(db_column='SURVEYPRICE')
    individualPrice = models.FloatField(db_column='INDIVIDUALPRICE')
    emailBounceRate = models.IntegerField(default=6, db_column='EMAIL_BOUNCE_RATE')
    throttlingCountDays = models.IntegerField(default=0, db_column='THROTTLING_COUNT_DAYS')
    throttlingDomainCapacity = models.IntegerField(default=0, db_column='THROTTLING_DOMAIN_CAPACITY')
    throttlingLastTotalCampaigns = models.IntegerField(default=0, db_column='THROTTLING_LAST_TOTAL_CAMPAIGNS')
    throttlingBounceRatePercentage = models.IntegerField(default=0, db_column='THROTTLING_BOUNCE_RATE_PERCENTAGE')
    throttlingIncreaseDomainCapacityPercentage = models.IntegerField(default=0, db_column='THROTTLING_INCREASE_DOMAIN_CAPACITY_PERCENTAGE')

    class Meta:
        managed = False
        db_table = 'TENANT_SETTINGS'


class Surveys(models.Model):
    sryId = models.BigAutoField(primary_key=True, db_column='SUR_ID')
    sryName = models.CharField(max_length=255, db_column='SUR_NAME')
    sryDescription = models.TextField(db_column='SUR_DESCRIPTION')
    sryData = models.TextField(db_column='SUR_DATA')
    sryStCategoryPageList = models.TextField(db_column='SUR_CATEGORY_PAGE_LIST')
    sryCountryList = models.TextField(db_column='SUR_COUNTRY_LIST')
    sryStatus = models.IntegerField(db_column='SUR_STATUS')
    sryStId = models.BigIntegerField(db_column='SUR_ST_ID')
    sryStTotalQuestions = models.IntegerField(default=0, db_column='SUR_TOTAL_QUESTIONS')
    memberId = models.BigIntegerField(db_column='SUR_CLIENT_ID')
    sryCreatedDate = models.DateField(db_column='SUR_CREATED_DATE', null=True, blank=True)
    sryUpdateDate = models.DateField(db_column='SUR_UPDATE_DATE', null=True, blank=True)
    sryEmbedding = models.JSONField(null=True, blank=True, db_column='SUR_EMBEDDING')

    class Meta:
        managed = False
        db_table = 'SURVEYS'


class SpTransLog(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='PSR_ID')
    smspollingId = models.BigIntegerField(db_column='PSR_PS_ID')
    memberId = models.BigIntegerField(db_column='PSR_CLIENT_ID')
    quesId = models.BigIntegerField(db_column='PSR_QUES_ID')
    question = models.TextField(db_column='PSR_QUESTION')
    userReply = models.TextField(db_column='PSR_USER_REPLY')
    fromNo = models.CharField(max_length=255, db_column='PSR_FROM_NO')
    toNo = models.CharField(max_length=255, db_column='PSR_TO_NO')
    smsDate = models.DateTimeField(db_column='PSR_SMS_DATE', null=True, blank=True)
    transRate = models.FloatField(db_column='PSR_TRANS_RATE')
    transAmt = models.FloatField(db_column='PSR_TRANS_AMT')
    memberSend = models.CharField(max_length=255, db_column='PSR_MEMBER_SEND')
    fromCountry = models.CharField(max_length=255, db_column='PSR_FROM_COUNTRY')
    fromState = models.CharField(max_length=255, db_column='PSR_FROM_STATE')
    fromCity = models.CharField(max_length=255, db_column='PSR_FROM_CITY')
    fromZip = models.CharField(max_length=255, db_column='PSR_FROM_ZIP')
    tranId = models.BigIntegerField(default=0, db_column='PSR_CT_TRANS_ID')
    msgContains = models.TextField(db_column='PSR_MSG_CONTAINS')
    questionSend = models.CharField(max_length=1, default='N', db_column='PSR_QUESTION_SEND')
    psrEmbedding = models.JSONField(null=True, blank=True, db_column='PSA_EMBEDDING')

    class Meta:
        managed = False
        db_table = 'POLLING_SMS_REPORTING'


class SpQuestions(models.Model):
    queId = models.BigAutoField(primary_key=True, db_column='PSQ_ID')
    iSmspollingId = models.BigIntegerField(db_column='PSQ_PS_ID')
    queTypeId = models.BigIntegerField(db_column='PSQ_TYPE_ID')
    question = models.TextField(db_column='PSQ_QUESTION')
    noOfOptions = models.IntegerField(db_column='PSQ_NO_OF_OPTIONS')
    queOrder = models.IntegerField(default=0, db_column='PSQ_QUE_ORDER')
    disOrder = models.BigIntegerField(db_column='PSQ_DISORDER')
    ddQue = models.IntegerField(default=0, db_column='PSQ_DD_QUE')
    catId = models.IntegerField(db_column='PSQ_CAT_ID')

    class Meta:
        managed = False
        db_table = 'POLLING_SMS_QUESTIONS'


class SpOptions(models.Model):
    optId = models.BigAutoField(primary_key=True, db_column='PSA_ID')
    optTypeId = models.BigIntegerField(db_column='PSA_TYPE_ID', default=0)
    queId = models.BigIntegerField(db_column='PSA_QUE_ID', default=0)
    optionVal = models.CharField(max_length=255, db_column='PSA_ANSWER')
    optOrder = models.IntegerField(default=0, db_column='PSA_OPT_ORDER')
    ansAnalysis = models.TextField(db_column='PSA_ANALYSIS')
    condQue = models.IntegerField(db_column='PSA_COND_QUE')
    regReq = models.IntegerField(db_column='PSA_REG_REQ')
    psaEmbedding = models.JSONField(null=True, blank=True, db_column='PSA_EMBEDDING')

    class Meta:
        managed = False
        db_table = 'POLLING_SMS_ANSWERS'


class SpReply(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='PSR_ID')
    smsPollingId = models.BigIntegerField(db_column='PSR_SP_ID')
    quesId = models.IntegerField(db_column='PSR_QUE_ID')
    question = models.TextField(db_column='PSR_QUESTION')
    ansId = models.IntegerField(db_column='PSR_ANS_ID')
    ansVal = models.CharField(max_length=255, db_column='PSR_ANSWER')
    userReply = models.TextField(db_column='USER_REPLY')
    fromNo = models.CharField(max_length=255, db_column='PSR_FROM_NO')
    toNo = models.CharField(max_length=255, db_column='PSR_TO_NO')
    sid = models.CharField(max_length=255, db_column='PSR_SID')
    sendDate = models.DateTimeField(db_column='PSR_SEND_DATE', null=True, blank=True)
    replyDate = models.DateTimeField(db_column='PSR_REPLY_YDATE', null=True, blank=True)
    fromCountry = models.CharField(max_length=255, db_column='PSR_FROM_COUNTRY')
    fromState = models.CharField(max_length=255, db_column='PSR_FROM_STATE')
    fromCity = models.CharField(max_length=255, db_column='PSR_FROM_CITY')
    fromZip = models.CharField(max_length=255, db_column='PSR_FROM_ZIP')
    tranId = models.BigIntegerField(default=0, db_column='PSR_CT_TRANS_ID')
    psrEmbedding = models.JSONField(null=True, blank=True, db_column='PSA_EMBEDDING')

    class Meta:
        managed = False
        db_table = 'POLLING_SMS_RESPONSES'


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
        db_table = 'DELETE_ACCOUNT'


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










