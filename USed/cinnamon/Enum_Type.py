
class Enum_Type:

# TYPE AND SUBTYPE OF PACKETS
    type_packet = {
    	0: 'Management',
    	1: 'Control',
    	2: 'Data'
    }

    subtypes_management = {
    	0: 'Association-request',
    	1: 'Association-response',
    	2: 'Reassociation-request',
    	3: 'Reassociation-response',
    	4: 'Probe-request',
    	5: 'Probe-response',
    	8: 'Beacon',
    	9: 'Announcement-traffic-indication-message',
    	10: 'Disassociation',
    	11: 'Authentication',
    	12: 'Deauthentication',
    	13: 'Action',
    	14: 'Reserved'
    }

    subtypes_control = {
    	8: 'Block-acknowledgement-request',
    	9: 'Block-acknowledgement',
    	10: 'Power-save-poll',
    	11: 'Request-to-send',
    	12: 'Clear-to-send',
    	13: 'Acknowledgement',
    	14: 'Contention-free-end',
    	15: 'Contention-free-end-plus-acknowledgement'
    }

    subtypes_data = {
    	0: 'Data',
    	1: 'Data-and-contention-free-acknowledgement',
    	2: 'Data-and-contention-free-poll',
    	3: 'Data-and-contention-free-acknowledgement-plus-poll',
    	4: 'Null',
    	5: 'Contention-free-acknowledgement',
    	6: 'Contention-free-poll',
    	7: 'Contention-free-acknowledgement-plus-poll',
    	8: 'Qos-data',
    	9: 'Qos-data-plus-contention-free-acknowledgement',
    	10: 'Qos-data-plus-contention-free-poll',
    	11: 'Qos-data-plus-contention-free-acknowledgement-plus-poll',
    	12: 'Qos-null',
    	14: 'Qos-contention-free-poll-empty',
    }


#EAP
    eap_codes = {
        1: "Request",
        2: "Response",
        3: "Success",
        4: "Failure",
        5: "Initiate",
        6: "Finish"
    }

    eap_types = {
        0:   "Reserved",
        1:   "Identity",
        2:   "Notification",
        3:   "Legacy Nak",
        4:   "MD5-Challenge",
        5:   "One-Time Password (OTP)",
        6:   "Generic Token Card (GTC)",
        7:   "Allocated - RFC3748",
        8:   "Allocated - RFC3748",
        9:   "RSA Public Key Authentication",
        10:  "DSS Unilateral",
        11:  "KEA",
        12:  "KEA-VALIDATE",
        13:  "EAP-TLS",
        14:  "Defender Token (AXENT)",
        15:  "RSA Security SecurID EAP",
        16:  "Arcot Systems EAP",
        17:  "EAP-Cisco Wireless",
        18:  "GSM Subscriber Identity Modules (EAP-SIM)",
        19:  "SRP-SHA1",
        20:  "Unassigned",
        21:  "EAP-TTLS",
        22:  "Remote Access Service",
        23:  "EAP-AKA Authentication",
        24:  "EAP-3Com Wireless",
        25:  "PEAP",
        26:  "MS-EAP-Authentication",
        27:  "Mutual Authentication w/Key Exchange (MAKE)",
        28:  "CRYPTOCard",
        29:  "EAP-MSCHAP-V2",
        30:  "DynamID",
        31:  "Rob EAP",
        32:  "Protected One-Time Password",
        33:  "MS-Authentication-TLV",
        34:  "SentriNET",
        35:  "EAP-Actiontec Wireless",
        36:  "Cogent Systems Biometrics Authentication EAP",
        37:  "AirFortress EAP",
        38:  "EAP-HTTP Digest",
        39:  "SecureSuite EAP",
        40:  "DeviceConnect EAP",
        41:  "EAP-SPEKE",
        42:  "EAP-MOBAC",
        43:  "EAP-FAST",
        44:  "ZoneLabs EAP (ZLXEAP)",
        45:  "EAP-Link",
        46:  "EAP-PAX",
        47:  "EAP-PSK",
        48:  "EAP-SAKE",
        49:  "EAP-IKEv2",
        50:  "EAP-AKA",
        51:  "EAP-GPSK",
        52:  "EAP-pwd",
        53:  "EAP-EKE Version 1",
        54:  "EAP Method Type for PT-EAP",
        55:  "TEAP",
        254: "Reserved for the Expanded Type",
        255: "Experimental",
    }
