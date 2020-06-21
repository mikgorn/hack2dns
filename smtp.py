import smtplib


class UTFSMTP(smtplib.SMTP):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.command_encoding = "utf-8"

    def rset(self):
        """SMTP 'rset' command -- resets session."""
        self.command_encoding = "utf-8"
        return self.docmd("rset")

    def data(self, msg):
        self.putcmd("data")
        (code, repl) = self.getreply()
        if self.debuglevel > 0:
            self._print_debug("data:", (code, repl))
        if code != 354:
            raise smtplib.SMTPDataError(code, repl)
        else:
            if isinstance(msg, str):
                msg = smtplib._fix_eols(msg).encode(self.command_encoding)
            q = smtplib._quote_periods(msg)
            if q[-2:] != smtplib.bCRLF:
                q = q + smtplib.bCRLF
            q = q + b"." + smtplib.bCRLF
            self.send(q)
            (code, msg) = self.getreply()
            if self.debuglevel > 0:
                self._print_debug("data:", (code, msg))
            return (code, msg)

    def auth(self, mechanism, authobject, *, initial_response_ok=True):
        mechanism = mechanism.upper()
        initial_response = authobject() if initial_response_ok else None
        if initial_response is not None:
            response = smtplib.encode_base64(
                initial_response.encode(self.command_encoding), eol=""
            )
            (code, resp) = self.docmd("AUTH", mechanism + " " + response)
        else:
            (code, resp) = self.docmd("AUTH", mechanism)
        # If server responds with a challenge, send the response.
        if code == 334:
            challenge = smtplib.base64.decodebytes(resp)
            response = smtplib.encode_base64(
                authobject(challenge).encode(self.command_encoding), eol=""
            )
            (code, resp) = self.docmd(response)
        if code in (235, 503):
            return (code, resp)
        raise smtplib.SMTPAuthenticationError(code, resp)

    def auth_cram_md5(self, challenge=None):
        if challenge is None:
            return None
        return (
            self.user
            + " "
            + smtplib.hmac.HMAC(
                self.password.encode(self.command_encoding), challenge, "md5"
            ).hexdigest()
        )

    def sendmail(
        self, from_addr, to_addrs, msg, mail_options=[], rcpt_options=[]
    ):
        self.ehlo_or_helo_if_needed()
        esmtp_opts = []
        if isinstance(msg, str):
            msg = smtplib._fix_eols(msg).encode(self.command_encoding)
        if self.does_esmtp:
            if self.has_extn("size"):
                esmtp_opts.append("size=%d" % len(msg))
            for option in mail_options:
                esmtp_opts.append(option)
        (code, resp) = self.mail(from_addr, esmtp_opts)
        if code != 250:
            if code == 421:
                self.close()
            else:
                self._rset()
            raise smtplib.SMTPSenderRefused(code, resp, from_addr)
        senderrs = {}
        if isinstance(to_addrs, str):
            to_addrs = [to_addrs]
        for each in to_addrs:
            (code, resp) = self.rcpt(each, rcpt_options)
            if (code != 250) and (code != 251):
                senderrs[each] = (code, resp)
            if code == 421:
                self.close()
                raise smtplib.SMTPRecipientsRefused(senderrs)
        if len(senderrs) == len(to_addrs):
            # the server refused all our recipients
            self._rset()
            raise smtplib.SMTPRecipientsRefused(senderrs)
        (code, resp) = self.data(msg)
        if code != 250:
            if code == 421:
                self.close()
            else:
                self._rset()
            raise smtplib.SMTPDataError(code, resp)
        return senderrs


class UTFSMTPSSL(smtplib.SMTP_SSL, UTFSMTP):
    # Order is necessary!
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.command_encoding = "utf-8"
