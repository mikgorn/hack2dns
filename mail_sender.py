import smtplib
from typing import *
from email.message import EmailMessage


class SimpleMailSender:
    def __init__(
        self,
        smtp_host: str,
        smtp_port: int,
        default_sender_mail: Optional[str] = None,
    ):
        self.host = smtp_host
        self.port = smtp_port
        self._smtp = smtplib.SMTP(self.host, self.port)
        self._default_sender_mail = default_sender_mail

    def _create_message(self, *args, **kwargs) -> EmailMessage:
        message = EmailMessage()
        message.set_content(*args, **kwargs)
        return message

    def _send_message(
        self,
        from_mail: str,
        to_mails: Iterator[str],
        *message_args,
        **message_kwargs
    ) -> None:
        self._smtp.send_message(
            self._create_message(*message_args, **message_kwargs),
            from_addr=from_mail,
            to_addrs=to_mails,
        )

    def _stop(self) -> None:
        self._smtp.quit()


if __name__ == "__main__":
    s = SimpleMailSender("localhost", 1025)
    s._send_message("ficys@bj.k", "фокус@ар.ка", "фокус")
    s._stop()
