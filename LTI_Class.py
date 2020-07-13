import re


class lti:

    __LTI_PROP_RE = r"^\$PLTIT.+\*..$"
    __LTI_CHECK_RE = r"^\$(?P<xorstr>PLTIT,.+)\*(?P<csum>..)$"
    __LTI_RETTYP_RE = r"^\$PLTIT,(?P<type>ID|HV|HT|ML),.+\*..$"
    __LTI_ID_RE = r"\$PLTIT,(ID),(.*),([.0-9]*)\*..$"
    __LTI_RETHT_RE = (
        r"^\$PLTIT,(?P<type>HT),"
        r"(?P<HT>-?[.0-9]*),(?P<HTUnits>[FYM]?)"
        r"\*(?P<csum>..)$"
    )
    __LTI_RETGEN_RE = (
        r"^\$PLTIT,(?P<type>HV|ML),"
        r"(?P<HD>-?[0-9]*\.?[0-9]?)(?P<HDPrecision>[01]?),(?P<HDUnits>[FYM]?),"
        r"(?P<AZ>-?[0-9]*\.?[0-9]*),(?P<AZUnits>[D]?),"
        r"(?P<INC>-?[0-9]*\.?[0-9]?)(?P<INCPrecision>[01]?),(?P<INCUnits>[D]?),"
        r"(?P<SD>-?[0-9]*\.?[0-9]?)(?P<SDPrecision>[01]?),(?P<SDUnits>[FYM]?)"
        r"\*(?P<csum>..)$"
    )

    @staticmethod
    def proprietary_string(ltistring):

        if isinstance(ltistring, (bytes, bytearray)):
            ltistring = ltistring.decode("utf-8").strip()

        if re.search(lti.__LTI_PROP_RE, ltistring) is not None:
            return ltistring
        else:
            return None

    @staticmethod
    def checksum(ltistring):

        if lti.proprietary_string(ltistring) is None:
            return None

        if isinstance(ltistring, (bytes, bytearray)):
            ltistring = ltistring.decode("utf-8").strip()

        match = re.search(lti.__LTI_CHECK_RE, ltistring)

        if match is not None:
            return "0x" + match.group("csum").lower()
        else:
            return None

    @staticmethod
    def checksum_calculate(ltistring):

        if lti.proprietary_string(ltistring) is None:
            return None

        if lti.checksum(ltistring) is None:
            return None

        if isinstance(ltistring, (bytes, bytearray)):
            ltistring = ltistring.decode("utf-8").strip()

        match = re.search(lti.__LTI_CHECK_RE, ltistring)

        csum = 0

        for character in match.group("xorstr"):
            csum ^= ord(character)

        return hex(csum)

    @staticmethod
    def checksum_verify(ltistring):

        if lti.proprietary_string(ltistring) is None:
            return False

        if lti.checksum(ltistring) is None:
            return False

        if isinstance(ltistring, (bytes, bytearray)):
            ltistring = ltistring.decode("utf-8").strip()

        match = re.search(lti.__LTI_CHECK_RE, ltistring)

        if match is None:
            return False

        if lti.checksum_calculate(ltistring) == lti.checksum(ltistring):
            return True
        else:
            return False

    @staticmethod
    def decode(ltistring):

        datareturn = {
            "type": None,
            "HD": None,
            "HDPrecision": None,
            "HDUnits": None,
            "AZ": None,
            "AZUnits": None,
            "INC": None,
            "INCPrecision": None,
            "INCUnits": None,
            "SD": None,
            "SDPrecision": None,
            "SDUnits": None,
            "HT": None,
            "HTUnits": None,
            "csum": None,
        }

        if lti.checksum_verify(ltistring) is False:
            return datareturn
        else:
            if re.match(lti.__LTI_RETGEN_RE, ltistring) is not None:
                match = re.match(lti.__LTI_RETGEN_RE, ltistring)

                datareturn["type"] = match.group("type")
                datareturn["HD"] = match.group("HD")
                datareturn["HDPrecision"] = match.group("HDPrecision")
                datareturn["HDUnits"] = match.group("HDUnits")
                datareturn["AZ"] = match.group("AZ")
                datareturn["AZUnits"] = match.group("AZUnits")
                datareturn["INC"] = match.group("INC")
                datareturn["INCPrecision"] = match.group("INCPrecision")
                datareturn["INCUnits"] = match.group("INCUnits")
                datareturn["SD"] = match.group("SD")
                datareturn["SDPrecision"] = match.group("SDPrecision")
                datareturn["SDUnits"] = match.group("SDUnits")
                datareturn["csum"] = match.group("csum")
                return datareturn

            elif re.match(lti.__LTI_RETHT_RE, ltistring) is not None:
                match = re.match(lti.__LTI_RETHT_RE, ltistring)

                datareturn["type"] = (match.group("type"),)
                datareturn["HT"] = (match.group("HT"),)
                datareturn["HTUnits"] = (match.group("HTUnits"),)
                datareturn["csum"] = (match.group("csum"),)
                return datareturn
            else:
                return datareturn
