import random
import string

class otp: 
    def otp_generation(self):
        try:
            digit = string.digits
            otp = ''.join(random.choice(digit) for _ in range(6))
            return otp
        except Exception as e:
            return f"error : {e}"

if __name__ == "__main__":
    otp_gen = otp()
    otp_generated = otp_gen.otp_generation()
    print(f"otp_generated : {otp_generated}")