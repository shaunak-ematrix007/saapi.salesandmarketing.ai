import re
import random
import datetime
import calendar
import dns.resolver
import requests
import os
from bs4 import BeautifulSoup
from typing import TypedDict, Optional, Dict, Any
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from common_app.exceptions import ProcessingFailedException

class MailRequestDTO(TypedDict):
    to: str
    templateName: str
    subject: str
    fromAdd: Optional[str]
    replyToAdd: Optional[str]
    name: Optional[str]
    fileName: Optional[str]
    filePath: Optional[str]

class MailResponseDTO(TypedDict):
    status: bool
    message: str


class CommonFunction:

    @staticmethod
    def displayDate(date):
        try:
            # Java: new SimpleDateFormat("yyyy-MM-dd").parse(date)
            modifiedDate = datetime.datetime.strptime(date, "%Y-%m-%d")
            # Java: new SimpleDateFormat("MM/dd/yyyy").format(modifiedDate)
            return modifiedDate.strftime("%m/%d/%Y")
        except Exception:
            raise ProcessingFailedException("Invalid date")

    @staticmethod
    def displayDateTime(date):
        try:
            # Handle optional subsecond/millisecond parts or timezone offsets
            if date:
                if "." in date:
                    date = date.split(".")[0]
                if "+" in date:
                    date = date.split("+")[0]
            # Java: new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").parse(date)
            modifiedDate = datetime.datetime.strptime(date.strip(), "%Y-%m-%d %H:%M:%S")
            # Java: new SimpleDateFormat("MM/dd/yyyy HH:mm:ss").format(modifiedDate)
            return modifiedDate.strftime("%m/%d/%Y %H:%M:%S")
        except Exception:
            raise ProcessingFailedException("Invalid date")

    @staticmethod
    def convertTimeZoneDateTime(date, ms=None):
        try:
            if ms is None:
                # Java: new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSS'Z'").parse(date)
                # Python %f is microseconds, .SSS is milliseconds. 
                # We handle the trailing 'Z' by stripping it or using %z if formatted correctly.
                clean_date = date.replace('Z', '')
                modifiedDate = datetime.datetime.strptime(clean_date, "%Y-%m-%dT%H:%M:%S.%f")
                return modifiedDate.strftime("%m/%d/%Y %H:%M:%S")
            elif ms == 7:
                # Java: yyyy-MM-dd'T'HH:mm:ss.SSSSSSS'Z'
                # Python strptime only supports up to 6 digits for %f.
                # We truncate to 6 digits.
                match = re.match(r"(.*)\.(\d{6})\d*(Z)", date)
                if match:
                    date = match.group(1) + "." + match.group(2) + match.group(3)
                clean_date = date.replace('Z', '')
                modifiedDate = datetime.datetime.strptime(clean_date, "%Y-%m-%dT%H:%M:%S.%f")
                return modifiedDate.strftime("%m/%d/%Y %I:%M:%S").lower() # hh:mm:ss is 12h
            elif ms == 0:
                # Java: yyyy-MM-dd'T'HH:mm:ss'Z'
                clean_date = date.replace('Z', '')
                modifiedDate = datetime.datetime.strptime(clean_date, "%Y-%m-%dT%H:%M:%S")
                return modifiedDate.strftime("%m/%d/%Y %I:%M:%S").lower()
            else:
                return None
        except Exception:
            raise ProcessingFailedException("Invalid date")

    @staticmethod
    def dbDate(date):
        try:
            # Java: new SimpleDateFormat("MM/dd/yyyy").parse(date)
            modifiedDate = datetime.datetime.strptime(date, "%m/%d/%Y")
            # Java: new SimpleDateFormat("yyyy-MM-dd").format(modifiedDate)
            return modifiedDate.strftime("%Y-%m-%d")
        except Exception:
            raise ProcessingFailedException("Invalid date")

    @staticmethod
    def dbDateTime(date):
        try:
            # Java: new SimpleDateFormat("MM/dd/yyyy HH:mm:ss").parse(date)
            modifiedDate = datetime.datetime.strptime(date, "%m/%d/%Y %H:%M:%S")
            # Java: new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(modifiedDate)
            return modifiedDate.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            raise ProcessingFailedException("Invalid date")

    @staticmethod
    def dbTime(date):
        try:
            # Java: new SimpleDateFormat("MM/dd/yyyy HH:mm:ss").parse(date)
            modifiedDate = datetime.datetime.strptime(date, "%m/%d/%Y %H:%M:%S")
            # Java: new SimpleDateFormat("HH:mm:ss").format(modifiedDate)
            return modifiedDate.strftime("%H:%M:%S")
        except Exception:
            raise ProcessingFailedException("Invalid date")

    @staticmethod
    def getTxtRecord(hostName):
        try:
            answers = dns.resolver.resolve(hostName, 'TXT')
            txt_records = []
            for rdata in answers:
                # Java logic: split by comma, replace TXT: , replace quotes, trim
                # Python dnspython gives strings that might be quoted.
                record = str(rdata).replace('"', '')
                txt_records.append(record.strip())
            return "~".join(txt_records)
        except Exception as e:
            # Java prints stack trace and returns empty string
            print(e)
            return ""

    @staticmethod
    def getCNAMERecord(hostName):
        try:
            answers = dns.resolver.resolve(hostName, 'CNAME')
            for rdata in answers:
                # Java: attr.get().toString().substring(0, attr.get().toString().length() - 1)
                # This usually removes a trailing dot in DNS.
                cname = str(rdata.target)
                if cname.endswith('.'):
                    cname = cname[:-1]
                return cname
            return ""
        except Exception as e:
            print(e)
            return ""

    @staticmethod
    def nl2br(text):
        if text is None:
            return ""
        return text.replace("\n", "<br>")

    @staticmethod
    def br2nl(html):
        if html is None:
            return ""
        # Java: Document document = Jsoup.parse(html); document.select("br").append("\\n"); return document.text().replace("\\n", "\n");
        soup = BeautifulSoup(html, "html.parser")
        for br in soup.find_all("br"):
            br.replace_with("\n")
        return soup.get_text()

    @staticmethod
    def getBillType(val):
        if val == "0":
            return "Bills"
        elif val == "1":
            return "Free"
        elif val == "2":
            return "Friends"
        elif val == "3":
            return "Family"
        elif val == "4":
            return "Adjustments"
        return ""

    @staticmethod
    def addOneMonth():
        # Java: LocalDate.now().plusMonths(1).toString()
        now = datetime.date.today()
        # Simple month addition
        month = now.month % 12 + 1
        year = now.year + (now.month + 1 > 12)
        day = min(now.day, calendar.monthrange(year, month)[1])
        return datetime.date(year, month, day).strftime("%Y-%m-%d")

    @staticmethod
    def convertDate(date):
        # Java: new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").parse(date)
        return datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    @staticmethod
    def convertDateOnly(date):
        # Java: new SimpleDateFormat("yyyy-MM-dd").parse(date)
        return datetime.datetime.strptime(date, "%Y-%m-%d").date()

    @staticmethod
    def covertTime(date):
        # Java: (Time) formatter.parse(date) where formatter is HH:mm:ss
        return datetime.datetime.strptime(date, "%H:%M:%S").time()

    @staticmethod
    def covertLocalDateTime(date):
        # Java: LocalDateTime.parse(date, formatter)
        return datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    @staticmethod
    def timeDuration(startTime, endTime):
        # Java uses Instant.parse and Duration.between
        # Python datetime subtraction returns a timedelta
        # We need to return something equivalent to Java Duration
        # Since this is a utility, we'll return the timedelta object
        return endTime - startTime

    @staticmethod
    def daysBetween(one, two):
        # Java: (one.getTime()-two.getTime())/86400000
        diff = one - two
        return abs(diff.days)

    @staticmethod
    def toTimeZone(localDateTime, timeZone):
        # Java: ZonedDateTime.of(localDateTime, ZoneId.systemDefault()).withZoneSameInstant(ZoneId.of(timeZone))
        # Note: In Python, we need to handle timezone conversion
        import pytz
        local_tz = pytz.timezone(timeZone)
        # Assuming localDateTime is naive and represents system default time
        # This is a bit tricky in Python without knowing system TZ. 
        # But usually system default is UTC in server environments.
        system_tz = pytz.utc 
        dt_with_system_tz = system_tz.localize(localDateTime)
        dt_with_target_tz = dt_with_system_tz.astimezone(local_tz)
        return dt_with_target_tz.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def addSeconds(date, seconds):
        return date + datetime.timedelta(seconds=seconds)

    @staticmethod
    def addSlashes(text):
        if text is None:
            return ""
        # Java manual character iteration and replacement
        res = ""
        for char in text:
            if char == '"': res += '\\"'
            elif char == "'": res += "\\'"
            elif char == '\\': res += '\\\\'
            elif char == '\n': res += '\\n'
            elif char == '{': res += '\\{'
            elif char == '}': res += '\\}'
            else: res += char
        return res

    @staticmethod
    def stripSlashes(text):
        if text is None:
            return ""
        return text.replace("\\", "")

    @staticmethod
    def cleanMe(strVal):
        if strVal is None:
            return ""
        # Java: strVal.replaceAll("[^A-Za-z0-9/@.:%,_'-]", " ")
        strVal = re.sub(r"[^A-Za-z0-9/@.:%,_'-]", " ", strVal)
        strVal = CommonFunction.addSlashes(strVal)
        return strVal

    @staticmethod
    def cleanMeNumber(strVal):
        if strVal is None:
            return ""
        # Java: strVal.replaceAll("[^A-Za-z0-9']", "")
        return re.sub(r"[^A-Za-z0-9']", "", strVal)

    @staticmethod
    def lastCharaters(input_str, no):
        if len(input_str) > no:
            return input_str[-no:]
        else:
            return input_str

    @staticmethod
    def ucFirst(str_val):
        if str_val is None or len(str_val) == 0:
            return str_val
        return str_val[0].upper() + str_val[1:]

    @staticmethod
    def ucWords(str_val):
        if str_val is None:
            return str_val
        words = str_val.split(" ")
        res_words = []
        for word in words:
            if len(word) > 0:
                res_words.append(CommonFunction.ucFirst(word))
        return " ".join(res_words)

    @staticmethod
    def campaignPriceListDisplay(memberList, countrySetting):
        if memberList > 0 and countrySetting:
            # Java: memberList * countrySetting.getCntyCampaignPerPrice()
            # Decimal * int
            return float(memberList) * float(countrySetting.cntyCampaignPerPrice)
        return 0.0

    @staticmethod
    def campaignPriceListPer(memberList, countrySetting):
        if memberList > 0 and countrySetting:
            return float(countrySetting.cntyCampaignPerPrice)
        return 0.0

    @staticmethod
    def campaignPriceList(memberList, invFirst, countrySetting):
        if invFirst == "yes":
            if memberList != 0:
                memberList = memberList
            else:
                memberList = 0
        if memberList > 0:
            return float(memberList) * float(countrySetting.cntyCampaignPerPrice)
        return 0.0

    @staticmethod
    def surveyPriceList(memberList, invFirst, countrySetting):
        if invFirst == "yes":
            if memberList != 0:
                memberList = memberList
            else:
                memberList = 0
        if memberList > 0:
            return float(memberList) * float(countrySetting.cntySurveyPerPrice)
        return 0.0

    @staticmethod
    def pregQuote(pStr):
        # Java: pStr.replaceAll("[.\\\\+*?\\[\\^\\]$(){}=!<>|:\\-]", "\\\\$0")
        return re.escape(pStr)

    @staticmethod
    def getSmsTinyUrl(sms, prev):
        # Regex for URL
        regexUrl = r"((http|https)://)(www\.)?[a-zA-Z0-9@:%._\+~#?&//=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%._\+~#?&//=]*)"
        matches = re.finditer(regexUrl, sms)
        for m in matches:
            s = m.group()
            if s[:19] != "https://tinyeas.us/":
                rplUrl = "https://tinyeas.us/xxxxxxxx"
                if prev == 1:
                    rplUrl = CommonFunction.getTinyUrl(s)
                sms = sms.replace(s, rplUrl, 1)
        return sms

    @staticmethod
    def getTinyUrl(link):
        try:
            # Java uses RestTemplate postForObject
            url = "https://tinyeas.us/index.php"
            params = {
                "l": link,
                "o": "gettinyurl",
                "r": str(random.random())
            }
            response = requests.post(url, data=params)
            return response.text
        except  Exception:
            return ""

    @staticmethod
    def smsCampaignPriceListDisplay(totalSms, textIm, countrySetting):
        if totalSms > 0:
            if textIm == "image":
                # Java: cntyMMSPerPrice (assuming it's in countrySetting)
                # If not in model, we might need to add it.
                return float(totalSms) * float(getattr(countrySetting, 'cntyMMSPerPrice', 0))
            else:
                return float(totalSms) * float(countrySetting.cntySMSPerPrice)
        return 0.0

    @staticmethod
    def smsCampaignPriceListPer(totalSms, textIm, countrySetting):
        if totalSms > 0:
            if textIm == "image":
                return float(getattr(countrySetting, 'cntyMMSPerPrice', 0))
            else:
                return float(countrySetting.cntySMSPerPrice)
        return 0.0

    @staticmethod
    def cronSendCampaignContentRemove(data):
        data = CommonFunction.removeWhitespace(data)
        serVal = "display: none;"
        data = data.replace(serVal, "display: none !important;max-width: 0px !important;max-height: 0px !important;overflow:hidden !important;")
        serVal = "display:none;"
        data = data.replace(serVal, "display: none !important;max-width: 0px !important;max-height: 0px !important;overflow:hidden !important;")
        data = data.replace("Drop Content Blocks Here", "")
        data = data.replace("<div class=\"mojoMcContainerEmptyMessage\" style=\"display: none;\"></div>", "")
        data = data.replace("Drop an image here", "")
        data = data.replace("<br>or", "")
        placeholder_image = "<td><div class=\"imagePlaceholder\"><img class=\"mojoImageItemIcon\" src=\"images/icons/empty_image-72.png\"><div data-dojo-attach-point=\"uploadText\"><span></span></div><div><input data-dojo-attach-point=\"browseBtn\" class=\"button-small p3\" value=\"browse\" type=\"button\"></div></div></td>"
        data = data.replace(placeholder_image, "")
        return data

    @staticmethod
    def removeWhitespace(data):
        # Java: data.replaceAll("/(?<=>)\\s+(?=<)/", "")
        # This regex removes whitespace between HTML tags
        return re.sub(r"(?<=>)\s+(?=<)", "", data)

    @staticmethod
    def getRanStr(length):
        characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        return "".join(random.choice(characters) for _ in range(length))

    @staticmethod
    def rangeRandom(min_val, max_val):
        return random.randint(min_val, max_val)

    @staticmethod
    def numberFormat(totalAmount, number):
        # Java: String.format("%."+number+"f", totalAmount)
        fmt = f"%.{number}f"
        return fmt % totalAmount

    @staticmethod
    def renameFileName(fileName):
        # Java: fileName.replaceAll("[^a-zA-Z0-9\\.\\-]+", "_")
        return re.sub(r"[^a-zA-Z0-9.\-]+", "_", fileName)

    @staticmethod
    def getFinalMemberId(member):
        parentMemberId = member.parentMemberId
        memberId = member.memberId
        if parentMemberId and parentMemberId > 0:
            memberId = parentMemberId
        return memberId

    @staticmethod
    def getBrowserName(agent):
        if agent is None: return "Others"
        if "Firefox" in agent: return "Firefox"
        elif "MSIE" in agent or "EIE" in agent: return "IE"
        elif "iPhone" in agent:
            if "Mobile" in agent: return "iPhone"
        elif "iPad" in agent: return "iPad"
        elif "Android" in agent:
            if "Mobile" in agent: return "Android Phone"
            else: return "Android Tab"
        elif "Chrome" in agent: return "Chrome"
        elif "Safari" in agent: return "Safari"
        elif "AIR" in agent: return "Air"
        elif "Fluid" in agent: return "Fluid"
        return "Others"

    @staticmethod
    def addMonth(date, plusMonth):
        # date is a python datetime.date or datetime.datetime
        # Use relative delta or manual month addition
        month = (date.month + plusMonth - 1) % 12 + 1
        year = date.year + (date.month + plusMonth - 1) // 12
        day = min(date.day, calendar.monthrange(year, month)[1])
        if isinstance(date, datetime.datetime):
            return datetime.datetime(year, month, day, date.hour, date.minute, date.second)
        return datetime.date(year, month, day)

    @staticmethod
    def dbLastDateMonth():
        now = datetime.datetime.now()
        day = calendar.monthrange(now.year, now.month)[1]
        return f"{now.year}-{now.month}-{day}"

    @staticmethod
    def convertDateTimeToTimeZone(date):
        try:
            # Java: new SimpleDateFormat("MM/dd/yyyy HH:mm:ss").parse(date)
            dt = datetime.datetime.strptime(date, "%m/%d/%Y %H:%M:%S")
            # Java: new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss").format(dt)
            return dt.strftime("%Y-%m-%dT%H:%M:%S")
        except Exception:
            raise ProcessingFailedException("Invalid date")

    @staticmethod
    def convertTimeZoneToDbDate(date):
        try:
            # Java: new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss").parse(date)
            dt = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
            # Java: new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(dt)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            raise ProcessingFailedException("Invalid date")

    @staticmethod
    def convertEventTimeZoneToUser(date, fromTimeZone, toTimeZone):
        try:
            if fromTimeZone is None or fromTimeZone == toTimeZone or toTimeZone is None:
                return date
            import pytz
            f_tz = pytz.timezone(fromTimeZone)
            t_tz = pytz.timezone(toTimeZone)
            dt = datetime.datetime.strptime(date, "%m/%d/%Y %H:%M:%S")
            f_dt = f_tz.localize(dt)
            t_dt = f_dt.astimezone(t_tz)
            return t_dt.strftime("%m/%d/%Y %H:%M:%S")
        except Exception:
            raise ProcessingFailedException("Invalid date")

    @staticmethod
    def convertEventTimeZoneToUserDB(date, fromTimeZone, toTimeZone):
        try:
            if fromTimeZone is None or fromTimeZone == toTimeZone or toTimeZone is None:
                return date
            import pytz
            f_tz = pytz.timezone(fromTimeZone)
            t_tz = pytz.timezone(toTimeZone)
            dt = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            f_dt = f_tz.localize(dt)
            t_dt = f_dt.astimezone(t_tz)
            return t_dt.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            raise ProcessingFailedException("Invalid date")

    @staticmethod
    def implode(separator, *data):
        # Java: for (int i = 0; i < data.length - 1; i++) { if (!data[i].matches(" *")) { ... } }
        # sb.append(data[data.length - 1].trim());
        if not data:
            return ""
        filtered_data = [d for d in data[:-1] if d.strip()]
        res = separator.join(filtered_data)
        last_item = data[-1].strip()
        if res:
            return res + separator + last_item
        return last_item


def send_email(request_data: MailRequestDTO, context: Dict[str, Any]) -> MailResponseDTO:
    """
    Sends an email using standard Django EmailMultiAlternatives and dynamically renders
    the template from request_data['templateName']. Matches Spring Boot's sendEmail logic.
    """
    response: MailResponseDTO = {"status": False, "message": ""}
    try:
        # Dynamically build template path
        template_name = request_data.get('templateName')
        template_path = f"email/{template_name}.html"

        # Render HTML body using Django template loader
        html_content = render_to_string(template_path, context)

        # Subject and Recipient
        subject = request_data.get('subject', '')
        recipient = request_data.get('to')

        # Fallback logic for From Address and Name
        from_email = request_data.get('fromAdd')
        from_name = request_data.get('name')
        if not from_email:
            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', '')
        else:
            if from_name:
                from_email = f"{from_name} <{from_email}>"

        # Fallback logic for Reply-To
        reply_to_email = request_data.get('replyToAdd')
        if not reply_to_email:
            reply_to_email = getattr(settings, 'DEFAULT_REPLY_TO_EMAIL', getattr(settings, 'EMAIL_HOST_USER', ''))

        reply_to_list = [reply_to_email] if reply_to_email else []

        # Construct Django EmailMultiAlternatives
        msg = EmailMultiAlternatives(
            subject=subject,
            body='',  # Empty plain text body as structured in Java
            from_email=from_email,
            to=[recipient] if isinstance(recipient, str) else recipient,
            reply_to=reply_to_list
        )

        # Attach alternative HTML view
        msg.attach_alternative(html_content, "text/html")

        # Attach file if path and name are specified and exist
        file_path = request_data.get('filePath')
        file_name = request_data.get('fileName')
        if file_path and file_name and os.path.exists(file_path):
            msg.attach_file(file_path)

        # Send the email
        msg.send()

        response["status"] = True
        response["message"] = f"Activate mail send to : {recipient}"

    except Exception as e:
        response["status"] = False
        response["message"] = f"Mail Sending failure : {str(e)}"

    return response

