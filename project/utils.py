"""
line function
"""


def line_notify_message(sess, token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    payload = {"message": msg}
    resp = sess.post(
        "https://notify-api.line.me/api/notify", headers=headers, params=payload
    )
    return resp.status_code
