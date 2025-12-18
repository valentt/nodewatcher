# Based on FreeBSD src/lib/libcrypt/crypt.c 1.2
# http://www.freebsd.org/cgi/cvsweb.cgi/~checkout~/src/lib/libcrypt/crypt.c?rev=1.2&content-type=text/plain

# Original license:
# * "THE BEER-WARE LICENSE" (Revision 42):
# * <phk@login.dknet.dk> wrote this file.  As long as you retain this notice you
# * can do whatever you want with this stuff. If we meet some day, and you think
# * this stuff is worth it, you can buy me a beer in return.   Poul-Henning Kamp

# This port adds no further stipulations.  I forfeit any copyright interest.

# Updated for Python 3 compatibility - hashlib requires bytes, not strings

from hashlib import md5


def _to_bytes(s):
    """Convert string to bytes if necessary."""
    if isinstance(s, bytes):
        return s
    return s.encode('utf-8')


def md5crypt(password, salt, magic='$1$'):
    # Convert all inputs to bytes for hashlib compatibility
    password = _to_bytes(password)
    salt = _to_bytes(salt)
    magic = _to_bytes(magic)

    # /* The password first, since that is what is most unknown */ /* Then our magic string */ /* Then the raw salt */
    m = md5()
    m.update(password + magic + salt)

    # /* Then just as many characters of the MD5(pw,salt,pw) */
    mixin = md5(password + salt + password).digest()
    for i in range(0, len(password)):
        m.update(bytes([mixin[i % 16]]))

    # /* Then something really weird... */
    # Also really broken, as far as I can tell.  -m
    i = len(password)
    while i:
        if i & 1:
            m.update(b'\x00')
        else:
            m.update(bytes([password[0]]))
        i >>= 1

    final = m.digest()

    # /* and now, just to make sure things don't run too fast */
    for i in range(1000):
        m2 = md5()
        if i & 1:
            m2.update(password)
        else:
            m2.update(final)

        if i % 3:
            m2.update(salt)

        if i % 7:
            m2.update(password)

        if i & 1:
            m2.update(final)
        else:
            m2.update(password)

        final = m2.digest()

    # This is the bit that uses to64() in the original code.

    itoa64 = './0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

    rearranged = ''
    for a, b, c in ((0, 6, 12), (1, 7, 13), (2, 8, 14), (3, 9, 15), (4, 10, 5)):
        # In Python 3, indexing bytes returns int directly, no need for ord()
        v = final[a] << 16 | final[b] << 8 | final[c]
        for i in range(4):
            rearranged += itoa64[v & 0x3f]
            v >>= 6

    v = final[11]
    for i in range(2):
        rearranged += itoa64[v & 0x3f]
        v >>= 6

    # Return as string (decode magic and salt back to str)
    return magic.decode('utf-8') + salt.decode('utf-8') + '$' + rearranged
