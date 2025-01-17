from django.utils.module_loading import import_string

from drfpasswordless.settings import api_settings
from drfpasswordless.utils import create_callback_token_for_user


class TokenService(object):
    @staticmethod
    def send_token(user, alias_type, token_type, **message_payload):
        alias_type_u = alias_type.upper()
        to_alias_field = getattr(
            api_settings, f"PASSWORDLESS_USER_{alias_type_u}_FIELD_NAME"
        )
        to_alias = getattr(user, to_alias_field)
        token = create_callback_token_for_user(user, alias_type, token_type, to_alias)
        send_action = None

        if user.pk in api_settings.PASSWORDLESS_DEMO_USERS or to_alias in getattr(
            api_settings, f"PASSWORDLESS_DEMO_USERS_{alias_type_u}"
        ):
            return True
        if alias_type == 'email':
            send_action = import_string(api_settings.PASSWORDLESS_EMAIL_CALLBACK)
        elif alias_type == 'mobile':
            send_action = import_string(api_settings.PASSWORDLESS_SMS_CALLBACK)
        # Send to alias
        success = send_action(user, token, **message_payload)
        return success
