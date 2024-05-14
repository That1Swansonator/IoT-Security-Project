import pyotp
import time
import ecc
import base64
import sibc




# This file will generate otp's for authentication and message verification
# This file will also verify otp's
totp = pyotp.TOTP('base32secret3232')

totp.now() # => '492039'

# OTP verified for current time
print(totp.verify('492039')) # => True
time.sleep(30)
print(totp.verify('492039')) # => False