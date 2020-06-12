# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# author = CarterHong


class ZoomRequestPayloadText:
    zoom = '''
{boundary}
Content-Disposition: form-data; name="command"

/zoomdev
{boundary}
Content-Disposition: form-data; name="disp"


{boundary}
Content-Disposition: form-data; name="channel"

{channel_id}
{boundary}
Content-Disposition: form-data; name="client_token"

web-1
{boundary}
Content-Disposition: form-data; name="token"

{token}
{boundary}
Content-Disposition: form-data; name="_x_reason"

executeCommand
{boundary}
Content-Disposition: form-data; name="_x_mode"

online
{boundary}
Content-Disposition: form-data; name="_x_sonic"

true
{boundary}--'''

    zoom_meeting_topic = '''
{boundary}
Content-Disposition: form-data; name="command"

/zoomdev
{boundary}
Content-Disposition: form-data; name="disp"

/zoomdev
{boundary}
Content-Disposition: form-data; name="blocks"

[{"type":"rich_text","elements":[{"type":"rich_text_section","elements":[{"type":"text","text":__TEXT__}]}]}]
{boundary}
Content-Disposition: form-data; name="channel"

{channel_id}
{boundary}
Content-Disposition: form-data; name="client_token"

web-1589180880456
{boundary}
Content-Disposition: form-data; name="token"

{token}
{boundary}
Content-Disposition: form-data; name="_x_reason"

executeCommand
{boundary}
Content-Disposition: form-data; name="_x_mode"

online
{boundary}
Content-Disposition: form-data; name="_x_sonic"

true
{boundary}--
'''
