from dagster import job, ScheduleDefinition
from etl.ops.fundamentals import download_fundamentals

@job
def fundamentals_job():
    download_fundamentals()

fundamentals_schedule = ScheduleDefinition(
    job=fundamentals_job,
    cron_schedule="0 3 * * *",  # Run at 3 AM daily
    name="daily_fundamentals",
) 