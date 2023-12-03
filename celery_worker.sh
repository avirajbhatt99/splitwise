#!/bin/bash

cd src
celery -A job.tasks worker --loglevel=info
