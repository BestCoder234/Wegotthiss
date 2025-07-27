from dagster import define_asset_job, ScheduleDefinition
from etl.ops.bhavcopy import download_bhavcopy

prices_job = define_asset_job(
    name="prices_job",
    selection=[download_bhavcopy],
)

prices_schedule = ScheduleDefinition(
    job=prices_job,
    cron_schedule="0 2 * * *",
    name="nightly_prices",
) 