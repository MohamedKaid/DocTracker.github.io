from apscheduler.schedulers.background import BackgroundScheduler
from database.Dbase import *
from services.EmailService import *
from services.docAuth import getExpiredDocuments

"""
    Begins process handled by driver class
    Repeated daily at 8am
"""

# time values
HOUR = '08'
MINUTE = '00'

# instantiate with timezone
scheduler = BackgroundScheduler(timezone='America/New_York')

# driver call to be repeated daily at 8am
def daily_task():
    # Establish server connection
    emailService = EmailService()

    # Get all dispatch emails
    dispatchers = Dbase.getAllDispatchers()
    
    # Send email for each dispatcher
    for dispatch in dispatchers:
        data = getExpiredDocuments(dispatch)
        emailService.sendEmail(dispatch, data, 'notification')
    
    # Close server connection
    emailService.close()

# scheduler.start() to be called from flask app
# scheduler.add_job(daily_task, trigger='cron', hour=HOUR, minute=MINUTE)

# daily_task()