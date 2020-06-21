import smtplib
from typing import *
from time import sleep
from functools import wraps
from logging import getLogger
from email.message import EmailMessage
from ssl import create_default_context

import smtp

from utils import convert_email_from_punycode_to_utf


WAIT_TIME = 1


def SMTPDisconnectErrorRetryPolicy(f: Callable) -> Callable:
    @wraps(f)
    def inner(self: "SimpleMailSender", *args, **kwargs):
        while True:
            try:
                return f(self, *args, **kwargs)
            except smtplib.SMTPServerDisconnected as e:
                self._logger.exception(e)
                self.reconnect()
                sleep(WAIT_TIME)

    return inner


class SimpleMailSender:
    def __init__(
        self, smtp_host: str, smtp_port: int, sender_addr: Optional[str] = None
    ):
        self.host = smtp_host
        self.port = smtp_port
        self.sender_addr: Optional[str] = sender_addr
        self._smtp: Optional[smtp.UTFSMTP] = None
        self._logger = getLogger(__file__)

    def _start(self) -> None:
        if self._smtp is not None:
            raise Exception("Mail sender is already running!")
        self._smtp = smtp.UTFSMTP(self.host, self.port)

    def start(self) -> None:
        self._start()

    def reconnect(self) -> None:
        assert self._smtp is not None
        self._smtp.connect(self.host, self.port)

    def _create_message(self, *args, **kwargs) -> EmailMessage:
        message = EmailMessage()
        message.set_content(*args, **kwargs)
        return message

    def _convert_addrs_to_utf(
        self, to_addrs: Union[str, Sequence]
    ) -> Union[str, Sequence]:
        if isinstance(to_addrs, str):
            return convert_email_from_punycode_to_utf(to_addrs)
        else:
            return [
                convert_email_from_punycode_to_utf(addr) for addr in to_addrs
            ]

    @SMTPDisconnectErrorRetryPolicy
    def _send_message(
        self,
        to_addrs: Union[str, Sequence[str]],
        *message_args,
        **message_kwargs
    ) -> None:
        assert self._smtp is not None
        if self.sender_addr is None:
            raise Exception("Send by null-mail!")
        message = self._create_message(*message_args, **message_kwargs)
        message["From"] = self.sender_addr
        to_addrs = self._convert_addrs_to_utf(to_addrs)
        self._logger.info("Send message to %s" % to_addrs)
        self._smtp.send_message(
            message, from_addr=self.sender_addr, to_addrs=to_addrs,
        )

    def set_sender_settings(self, from_addr: str, **kwargs) -> None:
        self.sender_addr = from_addr

    def send_message(
        self,
        to_addrs: Union[str, Sequence[str]],
        *message_args,
        **message_kwargs
    ) -> Optional[Exception]:
        try:
            self._send_message(to_addrs, *message_args, **message_kwargs)
            return None
        except Exception as e:
            return e

    def send_messages(
        self, sending_data: Dict[str, str]
    ) -> Dict[str, Optional[Exception]]:
        results = {}
        for email, message in sending_data.items():
            results[email] = self.send_message(email, message)
        return results

    def _stop(self) -> None:
        assert self._smtp is not None
        self._smtp.quit()

    def stop(self) -> None:
        self._stop()


class SecureMailSender(SimpleMailSender):
    def __init__(
        self, smtp_host: str, smtp_port: int, sender_addr: str, password: str
    ):
        super().__init__(smtp_host, smtp_port, sender_addr=sender_addr)
        self._password = password
        self._ssl_context = create_default_context()

    def _login(self) -> None:
        assert self._smtp is not None
        assert self._password is not None
        assert self.sender_addr is not None
        self._smtp.login(self.sender_addr, self._password)  # type: ignore

    def _start(self) -> None:
        if self._smtp is not None:
            raise Exception("Mail sender is already running!")
        self._smtp = smtp.UTFSMTPSSL(self.host, self.port)

    def start(self) -> None:
        self._start()
        self._login()

    def reconnect(self) -> None:
        super().reconnect()
        self._login()

    def set_sender_password(
        self, from_addr: str, password: str, **kwargs
    ) -> None:
        self.sender_addr = from_addr
        self._password = password
        self._login()
