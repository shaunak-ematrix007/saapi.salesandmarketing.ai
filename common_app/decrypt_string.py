import hashlib
import base64
import logging
from Crypto.Cipher import AES

# Configure logging
logger = logging.getLogger(__name__)

class DecryptString:
    
    @staticmethod
    def md5(input_str):
        # Java: MessageDigest.getInstance("MD5")
        # Returns a 32-character hexadecimal string
        return hashlib.md5(input_str.encode('utf-8')).hexdigest()

    @staticmethod
    def setEncDecUser(data, act, flag):
        secretKey = "]d=3T[N}+:}YiA;cv418j*dCs"
        initialVectorString = "9eQV5B41wgCyqQb9"
        
        if data is not None:
            try:
                if flag == "":
                    # Java: data.replaceAll("$","") 
                    # Note: in Java replaceAll("$", "") adds nothing at the end of every line.
                    # However, usually this is intended to do nothing or replace literal '$'.
                    # Given the context, we'll follow the Java behavior.
                    return data.replace("$", "")
                else:
                    # Key is MD5 of secretKey
                    key = DecryptString.md5(secretKey).encode('utf-8')
                    iv = initialVectorString.encode('utf-8')
                    
                    # AES/CFB8/NoPadding
                    # In pycryptodome, MODE_CFB with segment_size=8 matches CFB8
                    if act == "display":
                        cipher = AES.new(key, AES.MODE_CFB, iv=iv, segment_size=8)
                        encrypted_byte_array = base64.b64decode(data.encode('utf-8'))
                        decrypted_byte_array = cipher.decrypt(encrypted_byte_array)
                        data = decrypted_byte_array.decode('utf-8')
                    else:
                        cipher = AES.new(key, AES.MODE_CFB, iv=iv, segment_size=8)
                        encrypted_byte_array = cipher.encrypt(data.encode('utf-8'))
                        data = base64.b64encode(encrypted_byte_array).decode('utf-8')
            except Exception as e:
                # Java: e.printStackTrace()
                logger.error("Error in setEncDecUser", exc_info=True)
        
        return data

    @staticmethod
    def decrypt(encryptedData, initialVectorString, secretKey):
        # Java logs
        logger.debug("inside decrypt method")
        logger.debug(f"initialVectorString: {initialVectorString}")
        logger.debug(f"secretKey: {secretKey}")
        
        decryptedData = None
        try:
            # Key is MD5 of secretKey
            key = DecryptString.md5(secretKey).encode('utf-8')
            iv = initialVectorString.encode('utf-8')
            
            # AES/CFB8/NoPadding
            cipher = AES.new(key, AES.MODE_CFB, iv=iv, segment_size=8)
            encrypted_byte_array = base64.b64decode(encryptedData.encode('utf-8'))
            decrypted_byte_array = cipher.decrypt(encrypted_byte_array)
            decryptedData = decrypted_byte_array.decode('utf-8')
        except Exception as e:
            # Java: System.out.println(e); log.error(...)
            print(e)
            logger.error("DecryptString class called", exc_info=True)
            
        return decryptedData
