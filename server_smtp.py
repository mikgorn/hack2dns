from smtpd import SMTPServer
import asyncore


class MySMTP(SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        print(peer)
        print(mailfrom)
        print(rcpttos)
        print(data)
        print(kwargs)


if __name__ == "__main__":
    MySMTP(("localhost", 1025), None, enable_SMTPUTF8=False)
    asyncore.loop()
