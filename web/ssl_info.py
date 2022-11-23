from datetime import datetime, timezone
import OpenSSL
import ssl
import socket


class SSLInfo:
    def __init__(self, hostname, port=443):
        self.hostname = hostname
        self.port = port

    def get_num_days_before_expired(self) -> int:
        """
        Get number of days before an TLS/SSL certificate of a domain expired
        """
        try:
            context = ssl.SSLContext()
            connection = socket.create_connection((self.hostname, self.port))
            sock = context.wrap_socket(connection, server_hostname = self.hostname)
            certificate = sock.getpeercert(True)
            pem_cert = ssl.DER_cert_to_PEM_cert(certificate)
            x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, pem_cert)
            cert_expires = datetime.strptime(x509.get_notAfter().decode('utf-8'), '%Y%m%d%H%M%S%z')
            sock.close()
            connection.close()
            return (cert_expires - datetime.now(timezone.utc)).days
        finally:
            sock.close()
            connection.close()

