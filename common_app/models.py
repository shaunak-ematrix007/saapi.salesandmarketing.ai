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

class Tenants(models.Model):
    ten_id = models.BigAutoField(db_column="TEN_ID", primary_key=True)
    ten_parent_id = models.BigIntegerField(db_column="TEN_PARENT_ID", null=True, blank=True)
    ten_crm_enabled = models.CharField(db_column="TEN_CRM_ENABLED", max_length=1, null=True, blank=True)
    ten_multi_client_enabled = models.CharField(db_column="TEN_MULTI_CLIENT_ENABLED", max_length=1, null=True, blank=True)
    ten_status = models.IntegerField(db_column="TEN_STATUS", default=0, null=True, blank=True)
    ten_username = models.CharField(db_column="TEN_USERNAME", max_length=25, null=True, blank=True)
    ten_first_name = models.CharField(db_column="TEN_FIRST_NAME", max_length=50, null=True, blank=True)
    ten_last_name = models.CharField(db_column="TEN_LAST_NAME", max_length=50, null=True, blank=True)
    ten_street_address1 = models.CharField(db_column="TEN_STREET_ADDRESS1", max_length=255, null=True, blank=True)
    ten_street_address2 = models.CharField(db_column="TEN_STREET_ADDRESS2", max_length=250, null=True, blank=True)
    ten_city = models.CharField(db_column="TEN_CITY", max_length=255, null=True, blank=True)
    ten_state = models.CharField(db_column="TEN_STATE", max_length=255, null=True, blank=True)
    ten_post_code = models.CharField(db_column="TEN_POST_CODE", max_length=25, null=True, blank=True)
    ten_country = models.CharField(db_column="TEN_COUNTRY", max_length=50, null=True, blank=True)
    ten_phone = models.CharField(db_column="TEN_PHONE", max_length=25, null=True, blank=True)
    ten_cell_phone = models.CharField(db_column="TEN_CELL_PHONE", max_length=25, null=True, blank=True)
    ten_email = models.CharField(db_column="TEN_EMAIL", max_length=25, null=True, blank=True)
    ten_default_language = models.CharField(db_column="TEN_DEFAULT_LANGUAGE", max_length=25, null=True, blank=True)
    ten_date_registered = models.DateTimeField(db_column="TEN_DATE_REGISTERED", null=True, blank=True)
    ten_last_logon = models.DateTimeField(db_column="TEN_LAST_LOGON", null=True, blank=True)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def id(self):
        return self.ten_id

    @property
    def is_active(self):
        # 0 is the active status based on view logic
        return self.ten_status == 0

    class Meta:
        managed = False
        db_table = "TENANTS"


class TenantDetails(models.Model):
    td_id = models.BigAutoField(db_column="TD_ID", primary_key=True)

    tenant = models.OneToOneField(
        Tenants,
        db_column="TD_TENANT_ID",
        to_field="ten_id",
        on_delete=models.DO_NOTHING,
        related_name="details",
        null=True,
        blank=True
    )

    td_membership_type = models.CharField(max_length=25, db_column="TD_MEMBERSHIP_TYPE", null=True, blank=True)
    td_country = models.CharField(max_length=50, db_column="TD_COUNTRY", null=True, blank=True)
    td_password = models.CharField(max_length=255, db_column="TD_PASSWORD", null=True, blank=True)

    td_sec_qus_1 = models.BigIntegerField(db_column="TD_SEC_QUS_1", null=True, blank=True)
    td_sec_ans_1 = models.CharField(max_length=255, db_column="TD_SEC_ANS_1", null=True, blank=True)
    td_sec_qus_2 = models.BigIntegerField(db_column="TD_SEC_QUS_2", null=True, blank=True)
    td_sec_ans_2 = models.CharField(max_length=255, db_column="TD_SEC_ANS_2", null=True, blank=True)
    td_sec_qus_3 = models.BigIntegerField(db_column="TD_SEC_QUS_3", default=0, null=True, blank=True)
    td_sec_ans_3 = models.CharField(max_length=255, db_column="TD_SEC_ANS_3", null=True, blank=True)

    td_opt_in = models.CharField(max_length=1, db_column="TD_OPT_IN", null=True, blank=True)

    td_sub_account_type_id = models.BigIntegerField(db_column="TD_SUB_ACCOUNT_TYPE_ID", default=0, null=True, blank=True)
    td_suba_reg_link_expire = models.DateTimeField(db_column="TD_SUBA_REG_LINK_EXPIRE", null=True, blank=True)

    td_date_registered = models.DateTimeField(db_column="TD_DATE_REGISTERED", null=True, blank=True)

    td_is2fa = models.CharField(max_length=1, db_column="TD_IS2FA", null=True, blank=True)
    td_otp = models.CharField(max_length=255, db_column="TD_OTP", null=True, blank=True)

    td_login_preference = models.CharField(max_length=255, db_column="TD_LOGIN_PREFERENCE", null=True, blank=True)
    td_google_authenticator_secret = models.CharField(max_length=2000, db_column="TD_GOOGLE_AUTHENTICATOR_SECRET", null=True, blank=True)
    td_microsoft_authenticator_secret = models.CharField(max_length=2000, db_column='"TD_MICROSOFT_AUTHENTICATOR_SECRET"', null=True, blank=True)

    td_registration_step = models.IntegerField(db_column="TD_REGISTRATION_STEP", default=0, null=True, blank=True)

    td_plan_id = models.CharField(max_length=255, db_column="TD_PLAN_ID", null=True, blank=True)
    td_agree_affiliate_program = models.CharField(max_length=1, db_column="TD_AGREE_AFFILIATE_PROGRAM", null=True, blank=True)
    td_newsletter_subscribe = models.CharField(max_length=1, db_column="TD_NEWSLETTER_SUBSCRIBE", null=True, blank=True)

    td_billing_first_name = models.CharField(max_length=255, db_column="TD_BILLING_FIRST_NAME", null=True, blank=True)
    td_billing_last_name = models.CharField(max_length=255, db_column="TD_BILLING_LAST_NAME", null=True, blank=True)
    td_billing_address1 = models.CharField(max_length=250, db_column="TD_BILLING_ADDRESS1", null=True, blank=True)
    td_billing_address2 = models.CharField(max_length=250, db_column="TD_BILLING_ADDRESS2", null=True, blank=True)
    td_billing_city = models.CharField(max_length=255, db_column="TD_BILLING_CITY", null=True, blank=True)
    td_billing_state = models.CharField(max_length=255, db_column="TD_BILLING_STATE", null=True, blank=True)
    td_billing_post_code = models.CharField(max_length=255, db_column="TD_BILLING_POST_CODE", null=True, blank=True)
    td_billing_country = models.CharField(max_length=255, db_column="TD_BILLING_COUNTRY", null=True, blank=True)
    td_billing_phone = models.CharField(max_length=255, db_column="TD_BILLING_PHONE", null=True, blank=True)

    td_enable_api = models.CharField(max_length=2000, db_column="TD_ENABLE_API", default="N", null=True, blank=True)
    td_auth_key = models.CharField(max_length=2000, db_column="TD_AUTH_KEY", null=True, blank=True)
    td_auth_token = models.CharField(max_length=2000, db_column="TD_AUTH_TOKEN", null=True, blank=True)

    td_authorize_customer_profile_id = models.CharField(max_length=255, db_column='"TD_AUTHORIZE_CUSTOMER_PROFILE_ID"', null=True, blank=True)
    td_authorize_customer_payment_profile_id = models.CharField(max_length=255, db_column='"TD_AUTHORIZE_CUSTOMER_PAYMENT_PROFILE_ID"', null=True, blank=True)
    td_bill_date = models.DateTimeField(db_column="TD_BILL_DATE", null=True, blank=True)
    td_creditcard_status = models.CharField(max_length=250, db_column="TD_CREDITCARD_STATUS", null=True, blank=True)
    td_creditcard_error = models.CharField(max_length=250, db_column="TD_CREDITCARD_ERROR", null=True, blank=True)

    class Meta:
        managed = False
        db_table = "TENANT_DETAILS"

class Clients(models.Model):
    cliId = models.BigAutoField(db_column='CLI_ID', primary_key=True)
    cliTenantId = models.BigIntegerField(db_column='CLI_TENANT_ID')
    cliName = models.CharField(db_column='CLI_NAME', max_length=50, null=True, blank=True)
    cliType = models.CharField(db_column='CLI_TYPE', max_length=25, null=True, blank=True)
    cliAudience = models.CharField(db_column='CLI_AUDIENCE', max_length=25, null=True, blank=True)
    cliWebsite = models.CharField(db_column='CLI_WEBSITE', max_length=100, null=True, blank=True)
    cliWebsiteColors = models.CharField(db_column='CLI_WEBSITE_COLORS', max_length=2000, null=True, blank=True)
    cliLogo = models.CharField(db_column='CLI_LOGO', max_length=500, null=True, blank=True)
    cliCustomerFooter = models.CharField(db_column='CLI_CUSTOMER_FOOTER', max_length=500, null=True, blank=True)
    cliLinkedin = models.CharField(db_column='CLI_LINKEDIN', max_length=100, null=True, blank=True)
    cliRevenue = models.DecimalField(db_column='CLI_REVENUE', max_digits=10, decimal_places=2, null=True, blank=True)
    cliNumEmployees = models.DecimalField(db_column='CLI_NUM_EMPLOYEES', max_digits=10, decimal_places=2, null=True, blank=True)
    cliStockTicker = models.CharField(db_column='CLI_STOCK_TICKER', max_length=25, null=True, blank=True)
    cli10DlcStatus = models.CharField(db_column='CLI_10DLC_STATUS', max_length=25, null=True, blank=True)
    cliSipFriendlyName = models.CharField(db_column='CLI_SIP_FRIENDLY_NAME', max_length=255, null=True, blank=True)
    cliSmsAccountSid = models.CharField(db_column='CLI_SMS_ACCOUNT_SID', max_length=255, null=True, blank=True)
    cliSipConnectionId = models.CharField(db_column='CLI_SIP_CONNECTION_ID', max_length=255, null=True, blank=True)
    cliSipUsername = models.CharField(db_column='CLI_SIP_USERNAME', max_length=255, null=True, blank=True)
    cliSipPassword = models.CharField(db_column='CLI_SIP_PASSWORD', max_length=255, null=True, blank=True)
    cliBusinessName = models.CharField(db_column='CLI_BUSINESS_NAME', max_length=100, null=True, blank=True)
    cliProfileImageUrl = models.CharField(db_column='CLI_PROFILE_IMAGE_URL', max_length=255, null=True, blank=True)
    cliTimeZone = models.CharField(db_column='CLI_TIME_ZONE', max_length=255, null=True, blank=True)
    cliSubAccountTypeId = models.BigIntegerField(db_column='CLI_SUB_ACCOUNT_TYPE_ID', default=0)
    cliSmsForwardMyphoneYn = models.CharField(db_column='CLI_SMS_FORWARD_MYPHONE_YN', max_length=1, default='Y')
    cliFbId = models.CharField(db_column='CLI_FB_ID', max_length=255, null=True, blank=True)
    cliFbAccessToken = models.CharField(db_column='CLI_FB_ACCESS_TOKEN', max_length=2000, null=True, blank=True)
    cliTwOauthtoken = models.CharField(db_column='CLI_TW_OAUTHTOKEN', max_length=2000, null=True, blank=True)
    cliTwOauthtokenSecret = models.CharField(db_column='CLI_TW_OAUTHTOKEN_SECRET', max_length=2000, null=True, blank=True)
    cliLinAuthToken = models.CharField(db_column='CLI_LIN_AUTH_TOKEN', max_length=2000, null=True, blank=True)
    cliLinExpiresAt = models.CharField(db_column='CLI_LIN_EXPIRES_AT', max_length=255, null=True, blank=True)
    cliZoomToken = models.CharField(db_column='CLI_ZOOM_TOKEN', max_length=2000, null=True, blank=True)
    # Oracle VECTOR(768, FLOAT32)
    cliEmbedding = models.JSONField(db_column='CLI_EMBEDDING', null=True, blank=True)

    class Meta:
        db_table = 'CLIENTS'
        managed = False

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
    cntySMSConversationsPerPrice = models.FloatField(db_column='"CNTY_SMS_CONVERSATIONS_PER_PRICE"', default=0.0)
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
    cnty10DLCCampaignTypeCharge = models.FloatField(db_column='"CNTY_10DLC_CAMPAIGN_TYPE_CHARGE"', default=0.0)
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
        db_table = 'USER_LIST'

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
        db_table = 'ADMIN'

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
    isProccessedByLoadbalancer = models.IntegerField(default=0, db_column='"CEQ_IS_PROCCESSED_BY_LOADBALANCER"')
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
    throttlingIncreaseDomainCapacityPercentage = models.IntegerField(default=0, db_column='"THROTTLING_INCREASE_DOMAIN_CAPACITY_PERCENTAGE"')

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
    daId = models.BigAutoField(primary_key=True, db_column='DA_ID')
    daAccountId = models.BigIntegerField(db_column='DA_ACCOUNT_ID')
    daAccountName = models.CharField(max_length=255, db_column='DA_ACCOUNT_NAME')
    daEmail = models.CharField(max_length=255, db_column='DA_EMAIL')
    daIpAddress = models.CharField(max_length=255, db_column='DA_IP_ADDRESS')
    daDateTime = models.CharField(max_length=255, db_column='DA_DATE_TIME')
    daLeavingDetails = models.TextField(db_column='DA_LEAVING_DETAILS')
    daACN = models.TextField(db_column='DA_ACN')

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
    groupId = models.BigAutoField(primary_key=True, db_column='GRP_ID')
    groupName = models.CharField(max_length=75, db_column='GRP_GROUP_NAME')
    dateRegistered = models.DateTimeField(db_column='GRP_DATE_REGISTERED', default=timezone.now)
    lockGroup = models.CharField(db_column='GRP_LOCK_GROUP', max_length=1, default='N')
    segmentYn = models.CharField(db_column='GRP_SEGMENT_YN', max_length=1, default='N')
    duplicateRecordsYn = models.CharField(db_column='GRP_DUPLICATE_RECORDS_YN', max_length=1, default='N')
    typeEmail = models.CharField(db_column='GRP_TYPE_EMAIL', max_length=255, default='unverified')
    totalMember = models.BigIntegerField(db_column='GRP_TOTAL_MEMBER', default=0)
    memberId = models.BigIntegerField(db_column='GRP_CLIENT_ID', null=True, blank=True)
    grpEmbedding = models.JSONField(null=True, blank=True, db_column='GRP_EMBEDDING')

    class Meta:
        managed = False
        db_table = 'GROUPS'


class GroupSegment(models.Model):
    segId = models.BigAutoField(db_column='SEG_ID', primary_key=True)
    segName = models.CharField(db_column='SEG_NAME', max_length=255, null=True, blank=True)
    groupId = models.BigIntegerField(db_column='SEG_GROUP_ID', null=True, blank=True)
    memberId = models.BigIntegerField(db_column='SEG_CLIENT_ID', null=True, blank=True)
    segQuery = models.CharField(db_column='SEG_QUERY', max_length=2000, null=True, blank=True)
    segDateAdded = models.DateTimeField(db_column='SEGADDEDDATE')
    segEmbedding = models.JSONField(null=True, blank=True, db_column='SEG_EMBEDDING')

    class Meta:
        managed = False
        db_table = 'SEGMENTS'


class GroupSegmentField(models.Model):
    segfId = models.BigAutoField(db_column='SF_ID', primary_key=True)
    segId = models.BigIntegerField(db_column='SF_SEG_ID')
    segFieldName = models.CharField(db_column='SF_FEILDS_NAME', max_length=255, null=True, blank=True)
    segFieldOperator = models.CharField(db_column='SF_OPERATOR', max_length=255, null=True, blank=True)
    segFieldValue = models.CharField(db_column='SF_FIELDS_VALUE', max_length=255, null=True, blank=True)
    segConditions = models.CharField(db_column='SF_CONDITIONS', max_length=255, null=True, blank=True)
    segDisplayOrder = models.BigIntegerField(db_column='SF_DISPLAY_ORDER', null=True, blank=True)
    segEmbedding = models.JSONField(null=True, blank=True, db_column='SEG_EMBEDDING')

    class Meta:
        managed = False
        db_table = 'SEGMENT_FIELDS'


class TempUserlist(models.Model):
    emailId = models.BigAutoField(db_column='TUL_EMAIL_ID', primary_key=True)
    birthday = models.CharField(db_column='TUL_BIRTHDAY', max_length=255, null=True, blank=True)
    city = models.CharField(db_column='TUL_CITY', max_length=255, null=True, blank=True)
    country = models.CharField(db_column='TUL_COUNTRY', max_length=255, null=True, blank=True)
    dateAdded = models.CharField(db_column='TUL_DATE_ADDED', max_length=255, null=True, blank=True)
    dateLastModified = models.CharField(db_column='TUL_DATEL_AS_MODIFIED', max_length=255, null=True, blank=True)
    email = models.CharField(db_column='TUL_EMAIL', max_length=255)
    firstName = models.CharField(db_column='TUL_FIRST_NAME', max_length=250, null=True, blank=True)
    gender = models.CharField(db_column='TUL_GENDER', max_length=255, null=True, blank=True)
    lastName = models.CharField(db_column='TUL_LAST_NAME', max_length=250, null=True, blank=True)
    optDate = models.CharField(db_column='TUL_OPT_DATE', max_length=255, null=True, blank=True)
    phoneNumber = models.CharField(db_column='TUL_PHONE_NUMBER', max_length=255, null=True, blank=True)
    stateProvRegion = models.CharField(db_column='TUL_STATE_PROV_REGION', max_length=255, null=True, blank=True)
    status = models.CharField(db_column='TUL_STATUS', max_length=255, null=True, blank=True)
    streetAddress1 = models.TextField(db_column='TUL_STREET_ADDRESS1', null=True, blank=True)
    streetAddress2 = models.TextField(db_column='TUL_STREET_ADDRESS2', null=True, blank=True)
    fullName = models.CharField(db_column='TUL_FULL_NAME', max_length=255, null=True, blank=True)
    phone = models.CharField(db_column='TUL_PHONE', max_length=255, null=True, blank=True)
    tags = models.CharField(db_column='TUL_TAGS', max_length=250, null=True, blank=True)
    transId = models.CharField(db_column='TUL_TRANS_ID', max_length=500, null=True, blank=True)
    udf1 = models.CharField(db_column='TUL_UDF1', max_length=250, null=True, blank=True)
    udf10 = models.CharField(db_column='TUL_UDF10', max_length=250, null=True, blank=True)
    udf2 = models.CharField(db_column='TUL_UDF2', max_length=250, null=True, blank=True)
    udf3 = models.CharField(db_column='TUL_UDF3', max_length=250, null=True, blank=True)
    udf4 = models.CharField(db_column='TUL_UDF4', max_length=250, null=True, blank=True)
    udf5 = models.CharField(db_column='TUL_UDF5', max_length=250, null=True, blank=True)
    udf6 = models.CharField(db_column='TUL_UDF6', max_length=250, null=True, blank=True)
    udf7 = models.CharField(db_column='TUL_UDF7', max_length=250, null=True, blank=True)
    udf8 = models.CharField(db_column='TUL_UDF8', max_length=250, null=True, blank=True)
    udf9 = models.CharField(db_column='TUL_UDF9', max_length=250, null=True, blank=True)
    zipPostalCode = models.CharField(db_column='TUL_ZIP_POSTAL_CODE', max_length=255, null=True, blank=True)
    memberId = models.BigIntegerField(db_column='TUL_CLIENT_ID', null=True, blank=True)
    usDefaultLanguage = models.CharField(db_column='TUL_US_DEFAULT_LANGUAGE', max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'TEMP_USER_LIST'
        managed = False


class TempCronUserListTotal(models.Model):
    cronId = models.BigAutoField(db_column='CRON_ID', primary_key=True)
    cronMemberId = models.BigIntegerField(db_column='CRON_CLIENT_ID')
    cronGroupId = models.BigIntegerField(db_column='CRON_GROUP_ID')
    cronStartId = models.BigIntegerField(db_column='CRON_START_ID')
    cronEndId = models.BigIntegerField(db_column='CRON_END_ID')
    cronProcess = models.CharField(db_column='CRON_PROCESS', max_length=1, null=True, blank=True)
    cronProcessFinished = models.CharField(db_column='CRON_PROCESS_FINISHED', max_length=1, null=True, blank=True)
    cronOptInMessage = models.CharField(db_column='CRON_OPT_IN_MESSAGE', max_length=250, null=True, blank=True)
    transId = models.CharField(db_column='CRON_TRANS_ID', max_length=255, null=True, blank=True)
    cronCheckDuplicateYN = models.CharField(db_column='CRON_CHECK_DUPLICATE_YN', max_length=1, default='N')
    cronOptInYN = models.CharField(db_column='CRON_OPT_IN_YN', max_length=1, default='N')
    cronEmailVerification = models.CharField(db_column='CRON_EMAIL_VERIFICATION', max_length=1, default='N')
    swapColumns = models.CharField(db_column='CRON_SWAP_COLUMNS', max_length=2000, null=True, blank=True)
    blankFieldsList = models.CharField(db_column='CRON_BLANK_FIELDS_LIST', max_length=250, null=True, blank=True)
    moveList = models.TextField(db_column='CRON_MOVE_LIST', null=True, blank=True)

    class Meta:
        db_table = 'TEMP_CRON_CONTACTS_TOTAL'
        managed = False


class RegistrationLinkLogs(models.Model):
    lnkId = models.BigAutoField(primary_key=True, db_column='LNK_ID')
    lnkLink = models.TextField(db_column='LNK_LINK', null=True, blank=True)
    lnkExpiryDateTime = models.DateTimeField(db_column='LNK_EXPIRY_DATE_TIME', null=True, blank=True)
    lnkPlanId = models.BigIntegerField(db_column='LNK_PLAN_ID', default=0)
    lnkCountrySettingId = models.BigIntegerField(db_column='LNK_COUNTRY_SETTING_ID', default=0)
    lnkDateTime = models.DateTimeField(db_column='LNK_DATE_TIME', null=True, blank=True)

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
    pmId = models.AutoField(db_column='PM_ID', primary_key=True)
    pmTitle = models.CharField(db_column='PM_TITLE', max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'PLAN_MODULES'
        managed = False


class CancelRegistrationLog(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='RL_ID')
    username = models.CharField(max_length=255, null=True, blank=True, db_column='RL_USERNAME')
    firstName = models.CharField(max_length=255, null=True, blank=True, db_column='RL_FIRST_NAME')
    lastName = models.CharField(max_length=255, null=True, blank=True, db_column='RL_LAST_NAME')
    email = models.CharField(max_length=255, null=True, blank=True, db_column='RL_EMAIL')
    cell = models.CharField(max_length=255, null=True, blank=True, db_column='RL_CELL')
    step = models.IntegerField(default=1, db_column='RL_STEP')
    createdDate = models.DateTimeField(null=True, blank=True, db_column='RL_CREATED_DATE')
    status = models.CharField(max_length=255, default='Leaving', db_column='RL_STATUS')
    country = models.CharField(max_length=25, db_column='RL_COUNTRY')

    class Meta:
        managed = False
        db_table = 'REGISTRATION_STEPS'


class TenDLCLogs(models.Model):
    dlcId = models.BigAutoField(primary_key=True, db_column='TDL_ID')
    memberId = models.BigIntegerField(db_column='TDL_CLIENT_ID', null=True, blank=True)
    dlcStatus = models.CharField(max_length=255, db_column='TDL_STATUS', null=True, blank=True)
    dlcDate = models.DateTimeField(db_column='TDL_DATE', null=True, blank=True)
    tdlEmbedding = models.JSONField(null=True, blank=True, db_column='TDL_EMBEDDING')

    class Meta:
        managed = False
        db_table = 'TEN_DLC_LOGS'


class TenDLCRenew(models.Model):
    rnwId = models.BigAutoField(primary_key=True, db_column='TDR_ID')
    rnwMemberId = models.BigIntegerField(db_column='TDR_CLIENT_ID', null=True, blank=True)
    rnwContinue = models.CharField(max_length=255, db_column='TDR_CONTINUE', null=True, blank=True)
    rnwDate = models.DateField(db_column='TDR_DATE', null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'TEN_DLC_RENEW'


class TenDLCData(models.Model):
    datId = models.BigAutoField(primary_key=True, db_column='TDC_ID')
    datMemberId = models.BigIntegerField(db_column='TDC_CLIENT_ID', null=True, blank=True)
    datBrandName = models.CharField(max_length=255, db_column='TDC_BRAND_NAME', null=True, blank=True)
    datCampaignType = models.CharField(max_length=255, db_column='TDC_CAMPAIGN_TYPE', null=True, blank=True)
    datIsActive = models.CharField(max_length=255, db_column='TDC_IS_ACTIVE', null=True, blank=True)
    datRegistrationDate = models.DateField(db_column='TDC_REGISTRATION_DATE', null=True, blank=True)
    tdc_embedding = models.JSONField(null=True, blank=True, db_column='TDC_EMBEDDING')

    class Meta:
        managed = False
        db_table = 'TEN_DLC_DATA'


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
    id = models.BigAutoField(db_column='CES_ID', primary_key=True)
    campId = models.BigIntegerField(db_column='CES_CAMP_ID', null=True, blank=True)
    campSendId = models.BigIntegerField(db_column='CES_SEND_ID', default=0)
    memberId = models.BigIntegerField(db_column='CES_CLIENT_ID', null=True, blank=True)
    email = models.CharField(db_column='CES_EMAIL', max_length=500, null=True, blank=True)
    emailId = models.BigIntegerField(db_column='CES_EMAIL_ID', null=True, blank=True)
    isSend = models.CharField(db_column='CES_IS_SEND', max_length=1, default='N')
    isRead = models.CharField(db_column='CES_IS_READ', max_length=1, null=True, blank=True)
    isBounced = models.CharField(db_column='CES_IS_BOUNCED', max_length=1, null=True, blank=True)
    isUnsubscribed = models.CharField(db_column='CES_IS_UNSUBSCRIBED', max_length=1, null=True, blank=True)
    firstName = models.CharField(db_column='CES_FIRST_NAME', max_length=255, null=True, blank=True)
    lastName = models.CharField(db_column='CES_LAST_NAME', max_length=255, null=True, blank=True)
    emailDomain = models.CharField(db_column='CES_EMAIL_DOMAIN', max_length=50, null=True, blank=True)
    csDefaultLanguage = models.CharField(db_column='CES_CS_DEFAULT_LANGUAGE', max_length=50, default='en')
    smtpServerHost = models.CharField(db_column='CES_SMTP_SERVER_HOST', max_length=50, null=True, blank=True)
    isProcessed = models.CharField(db_column='CES_IS_PROCESSED', max_length=1, default='N')
    emailQId = models.CharField(db_column='CES_EMAIL_Q_ID', max_length=255, null=True, blank=True)
    emailStatus = models.CharField(db_column='CES_EMAIL_STATUS', max_length=255, null=True, blank=True)
    cronStatus = models.CharField(db_column='CES_CRON_STATUS', max_length=255, default='active')
    splitGroup = models.CharField(db_column='CES_SPLIT_GROUP', max_length=1, null=True, blank=True)
    groupWinner = models.CharField(db_column='CES_GROUP_WINNER', max_length=1, null=True, blank=True)
    msgPriority = models.IntegerField(db_column='CES_MSG_PRIORITY', default=0)
    cesEmbedding = models.JSONField(null=True, blank=True, db_column='CES_EMBEDDING')

    class Meta:
        db_table = 'CAMPAIGN_EMAIL_SENT'
        managed = False


class CampaignsSendEmailArchive(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='SEA_ID')
    campId = models.BigIntegerField(null=True, blank=True, db_column='SEA_CAMP_ID')
    campSendId = models.BigIntegerField(default=0, db_column='SEA_CAMP_SEND_ID')
    memberId = models.BigIntegerField(null=True, blank=True, db_column='SEA_CLIENT_ID')
    email = models.CharField(max_length=500, null=True, blank=True, db_column='SEA_EMAIL')
    emailId = models.BigIntegerField(null=True, blank=True, db_column='SEA_EMAIL_ID')
    isSend = models.CharField(max_length=1, default='N', db_column='SEA_IS_SEND')
    isRead = models.CharField(max_length=1, null=True, blank=True, db_column='SEA_IS_READ')
    isBounced = models.CharField(max_length=1, null=True, blank=True, db_column='SEA_IS_BOUNCED')
    isUnsubscribed = models.CharField(max_length=1, null=True, blank=True, db_column='SEA_IS_UNSUBSCRIBED')
    firstName = models.CharField(max_length=255, null=True, blank=True, db_column='SEA_FIRST_NAME')
    lastName = models.CharField(max_length=255, null=True, blank=True, db_column='SEA_LAST_NAME')
    emailDomain = models.CharField(max_length=45, null=True, blank=True, db_column='SEA_EMAIL_DOMAIN')
    csDefaultLanguage = models.CharField(max_length=255, default='en', db_column='SEA_CS_DEFAULT_LANGUAGE')
    smtpServerHost = models.CharField(max_length=255, null=True, blank=True, db_column='SEA_SMTP_SERVER_HOST')
    isProcessed = models.CharField(max_length=1, default='N', db_column='SEA_IS_PROCESSED')
    emailQId = models.CharField(max_length=255, null=True, blank=True, db_column='SEA_EMAIL_Q_ID')
    emailStatus = models.CharField(max_length=255, null=True, blank=True, db_column='SEA_EMAIL_STATUS')
    cronStatus = models.CharField(max_length=255, default='active', db_column='SEA_CRON_STATUS')
    splitGroup = models.CharField(max_length=1, null=True, blank=True, db_column='SEA_SPLIT_GROUP')
    groupWinner = models.CharField(max_length=1, null=True, blank=True, db_column='SEA_GROUP_WINNER')
    msgPriority = models.IntegerField(default=0, db_column='SEA_MSG_PRIORITY')
    seaEmbeddings = models.JSONField(null=True, blank=True, db_column='SEA_EMBEDDINGS')

    class Meta:
        managed = False
        db_table = 'CAMPAIGN_SEND_EMAIL_ARCHIVE'


class AutomationSendContact(models.Model):
    id = models.BigAutoField(db_column='ASC_ID', primary_key=True)
    automationId = models.BigIntegerField(db_column='ASC_AUT_ID')
    automationMasterSendId = models.BigIntegerField(db_column='ASC_MASTER_SEND_ID', default=0)
    memberId = models.BigIntegerField(db_column='ASC_CLIENT_ID')
    email = models.CharField(db_column='ASC_EMAIL', max_length=500, null=True, blank=True)
    emailId = models.BigIntegerField(db_column='ASC_EMAIL_ID', null=True, blank=True)
    isSend = models.CharField(db_column='ASC_IS_SEND', max_length=1, default='N')
    isRead = models.CharField(db_column='ASC_IS_READ', max_length=1, null=True, blank=True)
    isBounced = models.CharField(db_column='ASC_IS_BOUNCED', max_length=1, null=True, blank=True)
    isUnsubscribed = models.CharField(db_column='ASC_IS_UNSUBSCRIBED', max_length=1, null=True, blank=True)
    firstName = models.CharField(db_column='ASC_FIRST_NAME', max_length=255, null=True, blank=True)
    lastName = models.CharField(db_column='ASC_LAST_NAME', max_length=255, null=True, blank=True)
    emailDomain = models.CharField(db_column='ASC_EMAIL_DOMAIN', max_length=45, null=True, blank=True)
    csDefaultLanguage = models.CharField(db_column='ASC_CS_DEFAULT_LANGUAGE', max_length=255, default='en')
    smtpServerHost = models.CharField(db_column='ASC_SMTP_SERVER_HOST', max_length=1, null=True, blank=True)
    isProcessed = models.CharField(db_column='ASC_IS_PROCESSED', max_length=1, default='N')
    emailQId = models.CharField(db_column='ASC_EMAIL_Q_ID', max_length=255, null=True, blank=True)
    emailStatus = models.CharField(db_column='ASC_EMAIL_STATUS', max_length=255, null=True, blank=True)
    cronStatus = models.CharField(db_column='ASC_CRON_STATUS', max_length=255, default='active')
    splitGroup = models.CharField(db_column='ASC_SPLIT_GROUP', max_length=1, null=True, blank=True)
    groupWinner = models.CharField(db_column='LCE_LINK_ID', max_length=1, null=True, blank=True)
    msgPriority = models.IntegerField(db_column='ASC_MSG_PRIORITY', default=0)
    campSendId = models.BigIntegerField(db_column='ASC_CAMP_SEND_ID', default=0)
    sid = models.CharField(db_column='ASC_SID', max_length=255, null=True, blank=True)
    smsStatus = models.CharField(db_column='ASC_SMS_STATUS', max_length=255, null=True, blank=True)
    errorMessage = models.CharField(db_column='ASC_SMS_ERROR_MESSAGE', max_length=255, null=True, blank=True)
    errorCode = models.CharField(db_column='ASC_ERROR_CODE', max_length=255, null=True, blank=True)
    fromContact = models.CharField(db_column='ASC_FROM_CONTACT', max_length=255, null=True, blank=True)
    toContact = models.CharField(db_column='ASC_TO_CONTACT', max_length=255, null=True, blank=True)
    smsSendDate = models.DateTimeField(db_column='ASC_SEND_DATE', null=True, blank=True)
    smsDetails = models.CharField(db_column='ASC_SMS_DETAILS', max_length=2000, null=True, blank=True)
    ascEmbedding = models.JSONField(null=True, blank=True, db_column='ASC_EMBEDDING')

    class Meta:
        db_table = 'AUTOMATION_SEND_CONTACT'
        managed = False


class CampaignLinks(models.Model):
    id = models.BigAutoField(db_column='CL_ID', primary_key=True)
    campId = models.BigIntegerField(db_column='CL_CAMP_ID', null=True, blank=True)
    campLink = models.TextField(db_column='CL_LINK', null=True, blank=True)
    linkCount = models.IntegerField(db_column='CL_LINK_COUNT', default=0)
    splitGroup = models.CharField(db_column='CL_SPLIT_GROUP', max_length=1, null=True, blank=True)
    nodeId = models.BigIntegerField(db_column='CL_NODE_ID', null=True, blank=True)
    automationEmailNodeDetails = models.CharField(db_column='CL_AUTOMATION_EMAIL_NODE_DETAILS', max_length=2000, null=True, blank=True)
    clEmbedding = models.JSONField(null=True, blank=True, db_column='CL_EMBEDDING')

    class Meta:
        db_table = 'CAMPAIGN_LINKS'
        managed = False


class CampaignLinkClick(models.Model):
    id = models.BigAutoField(db_column='ID_LINK', primary_key=True)
    userId = models.BigIntegerField(db_column='USER_ID', null=True, blank=True)
    linkId = models.IntegerField(db_column='LINK_ID', null=True, blank=True)
    linkCount = models.IntegerField(db_column='LINK_COUNT', null=True, blank=True)
    city = models.CharField(db_column='CITY', max_length=255, null=True, blank=True)
    clickDate = models.DateTimeField(db_column='CLICK_DATE', null=True, blank=True)
    sources = models.CharField(db_column='SOURCES', max_length=255, null=True, blank=True)
    sourceDetails = models.CharField(db_column='SOURCE_DETAILS', max_length=2000, null=True, blank=True)

    class Meta:
        db_table = 'TEMP_CAMP_LINK_CLICK'
        managed = False


class CampaignSubscriber(models.Model):
    id = models.BigAutoField(db_column='CS_ID', primary_key=True)
    campId = models.BigIntegerField(db_column='CS_CAMP_ID', null=True, blank=True)
    subId = models.BigIntegerField(db_column='CS_CONTACT_ID', null=True, blank=True)
    totalOpen = models.BigIntegerField(db_column='TOTAL_OPEN', null=True, blank=True)
    lastOpened = models.DateTimeField(db_column='CS_LAST_OPENED', null=True, blank=True)
    csIdEmbedding = models.JSONField(null=True, blank=True, db_column='CS_ID_EMBEDDING')

    class Meta:
        db_table = 'CAMPAIGN_EMAIL_REPORTING'
        managed = False










