# (c) Copyright 2021 by Coinkite Inc. This file is covered by license found in COPYING-CC.
#
# Constants and various "limits" shared between embedded and desktop USB protocol
#
try:
    from micropython import const
except ImportError:
    const = int

# USB encryption versions (default USB_NCRY_V1)
#
# This introduces a new ncry version to close a potential attack vector:
#
# A malicious program may re-initialize the connection encryption by sending the ncry command a second time during USB operation.
# This may prove particularly harmful in HSM mode.
#
# Sending version USB_NCRY_V2 changes the behavior in two ways:
#   * All future commands must be encrypted
#   * Returns an error if the ncry command is sent again for the duration of the power cycle
#
# USB_NCRY_V2 is most suitable for HSM mode as in case of any communication issue or simply by closing `ColdcardDevice`
# Coldcard will need to reboot to recover USB operation if USB_NCRY_V2.
USB_NCRY_V1 = const(0x01)
USB_NCRY_V2 = const(0x02)

# For upload/download this is the max size of the data block.
MAX_BLK_LEN = const(2048)

# Max total message length, excluding framing overhead (1 byte per 64).
# - includes args for upload command
MAX_MSG_LEN = const(4+4+4+MAX_BLK_LEN)

# Max PSBT txn we support (384k bytes as PSBT)
# - the max on the wire for mainnet is 100k
# - but a PSBT might contain a full txn for each input
MAX_TXN_LEN = const(384*1024)
MAX_TXN_LEN_MK4 = const(2*1024*1024)

# Max size of any upload (firmware.dfu files in particular)
MAX_UPLOAD_LEN = const(2*MAX_TXN_LEN)
MAX_UPLOAD_LEN_MK4 = const(2*MAX_TXN_LEN_MK4)

# Max length of text messages for signing
MSG_SIGNING_MAX_LENGTH = const(240)

# Bitcoin limitation: max number of signatures in P2SH redeem script (non-segwit)
# - 520 byte redeem script limit <= 15*34 bytes per pubkey == 510 bytes
# - serializations of M/N in redeem scripts assume this range
MAX_SIGNERS = const(15)

# Types of user auth we support
USER_AUTH_TOTP = const(1)       # RFC6238
USER_AUTH_HOTP = const(2)       # RFC4226
USER_AUTH_HMAC = const(3)       # PBKDF2('hmac-sha512', scrt, sha256(psbt), PBKDF2_ITER_COUNT)[:32]
USER_AUTH_SHOW_QR = const(0x80) # show secret on Coldcard screen (best for TOTP enroll)

MAX_USERNAME_LEN = 16
PBKDF2_ITER_COUNT = 2500

# Max depth for derived keys, in PSBT files, and USB commands
MAX_PATH_DEPTH = const(12)

# Bitmask used in sign_transaction (stxn) command
STXN_FINALIZE       = const(0x01)
STXN_VISUALIZE      = const(0x02)
STXN_SIGNED         = const(0x04)
STXN_FLAGS_MASK     = const(0x07)

# Bit values for address types
AFC_PUBKEY      = const(0x01)       # pay to hash of pubkey
AFC_SEGWIT      = const(0x02)       # requires a witness to spend
AFC_BECH32      = const(0x04)       # just how we're encoding it?
AFC_SCRIPT      = const(0x08)       # paying into a script
AFC_WRAPPED     = const(0x10)       # for transition/compat types for segwit vs. old
AFC_BECH32M     = const(0x16)       # no difference between script/key path in taproot

# Numeric codes for specific address types
AF_CLASSIC      = AFC_PUBKEY          # 1addr
AF_P2SH         = AFC_SCRIPT          # classic multisig / simple P2SH / 3hash
AF_P2WPKH       = AFC_PUBKEY  | AFC_SEGWIT | AFC_BECH32     # bc1qsdklfj
AF_P2WSH        = AFC_SCRIPT  | AFC_SEGWIT | AFC_BECH32     # segwit multisig
AF_P2WPKH_P2SH  = AFC_WRAPPED | AFC_PUBKEY | AFC_SEGWIT     # looks classic P2SH, but p2wpkh inside
AF_P2WSH_P2SH   = AFC_WRAPPED | AFC_SCRIPT | AFC_SEGWIT     # looks classic P2SH, segwit multisig
AF_P2TR         = AFC_PUBKEY  | AFC_SEGWIT | AFC_BECH32M    # bc1p

SUPPORTED_ADDR_FORMATS = frozenset([
    AF_CLASSIC,
    AF_P2SH,
    AF_P2WPKH,
    AF_P2TR,
    AF_P2WSH,
    AF_P2WPKH_P2SH,
    AF_P2WSH_P2SH,
])

# BIP-174 aka PSBT defined values
#
PSBT_GLOBAL_UNSIGNED_TX       = const(0)
PSBT_GLOBAL_XPUB              = const(1)

PSBT_IN_NON_WITNESS_UTXO      = const(0)
PSBT_IN_WITNESS_UTXO          = const(1)
PSBT_IN_PARTIAL_SIG           = const(2)
PSBT_IN_SIGHASH_TYPE          = const(3)
PSBT_IN_REDEEM_SCRIPT         = const(4)
PSBT_IN_WITNESS_SCRIPT        = const(5)
PSBT_IN_BIP32_DERIVATION      = const(6)
PSBT_IN_FINAL_SCRIPTSIG       = const(7)
PSBT_IN_FINAL_SCRIPTWITNESS   = const(8)
# BIP-371
PSBT_IN_TAP_KEY_SIG           = const(19)  # 0x13
PSBT_IN_TAP_SCRIPT_SIG        = const(20)  # 0x14
PSBT_IN_TAP_LEAF_SCRIPT       = const(21)  # 0x15
PSBT_IN_TAP_BIP32_DERIVATION  = const(22)  # 0x16
PSBT_IN_TAP_INTERNAL_KEY      = const(23)  # 0x17
PSBT_IN_TAP_MERKLE_ROOT       = const(24)  # 0x18

PSBT_OUT_REDEEM_SCRIPT        = const(0)
PSBT_OUT_WITNESS_SCRIPT       = const(1)
PSBT_OUT_BIP32_DERIVATION     = const(2)
# BIP-371
PSBT_OUT_TAP_INTERNAL_KEY     = const(5)
PSBT_OUT_TAP_TREE             = const(6)
PSBT_OUT_TAP_BIP32_DERIVATION = const(7)

RFC_SIGNATURE_TEMPLATE = '''\
-----BEGIN BITCOIN SIGNED MESSAGE-----
{msg}
-----BEGIN BITCOIN SIGNATURE-----
{addr}
{sig}
-----END BITCOIN SIGNATURE-----
'''

# EOF
