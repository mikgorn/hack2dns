import smtplib
from typing import *
from email.message import EmailMessage


class SimpleMailSender:
    def __init__(
        self,
        smtp_host: str,
        smtp_port: int,
        default_sender_addr: Optional[str] = None,
    ):
        self.host = smtp_host
        self.port = smtp_port
        self._smtp: Optional[smtplib.SMTP] = None
        self._default_sender_addr = default_sender_addr

    def start(self) -> None:
        self._smtp = smtplib.SMTP(self.host, self.port)

    def _create_message(self, *args, **kwargs) -> EmailMessage:
        message = EmailMessage()
        message.set_content(*args, **kwargs)
        return message

    def _send_message(
        self,
        from_addr: str,
        to_addrs: Union[str, Sequence[str]],
        *message_args,
        **message_kwargs
    ) -> None:
        if self._smtp is None:
            raise Exception("Mail sender is not running!")
        self._smtp.send_message(
            self._create_message(*message_args, **message_kwargs),
            from_addr=from_addr,
            to_addrs=to_addrs,
        )

    def set_default_sender_addr(self, to_addr) -> None:
        self._default_sender_addr = to_addr

    def send_message_by_default_mail(
        self,
        to_addrs: Union[str, Sequence[str]],
        *message_args,
        **message_kwargs
    ) -> None:
        if self._default_sender_addr is None:
            raise Exception("Send by null-mail!")
        self._send_message(
            self._default_sender_addr,
            to_addrs,
            *message_args,
            **message_kwargs
        )

    def send_message(
        self,
        from_addr: str,
        to_addrs: Union[str, Sequence[str]],
        *message_args,
        **message_kwargs
    ) -> None:
        self._send_message(
            from_addr, to_addrs, *message_args, **message_kwargs
        )

    def _stop(self) -> None:
        assert self._smtp, smtplib.SMTP
        self._smtp.quit()

    def stop(self) -> None:
        self._stop()


if __name__ == "__main__":
    s = SimpleMailSender("localhost", 1025)
    s.start()
    s.send_message("test@k.k", ["check@ар.рф", "Ficus@bk.ru"], "фокус")
    s.stop()
