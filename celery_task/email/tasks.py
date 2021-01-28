# -*- coding: utf-8 -*-
# @Auther:Summer
from celery_task.main import app


@app.task(name='p_k')
def p_k():
	print("pk")
