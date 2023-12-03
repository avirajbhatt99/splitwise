#!/bin/bash

cd src
celery -A job.tasks beat --scheduler redbeat.schedulers.RedBeatScheduler