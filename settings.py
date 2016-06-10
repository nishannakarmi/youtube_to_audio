MAXIMUM_VIDEO_TIME = 360
MAXIMUM_NUMBER_OF_VIDEOS = 4
ERROR_MSG = {
    'MAX_VIDEO_TIME': 'This video cannot be processed, it time is greater than %s min' %(MAXIMUM_VIDEO_TIME/60),
    'UNKNOWN': 'Sorry Unknown Error'
}
"""
secrete key generation method
import os
os.urandom(24)
"""
SECRET_KEY='\r\x05\xf9\x0f\x1d\xeb\xa4S{\xb4\x86\xba/"R\xb4\xf1\xeeg\\\xe3/J`'
