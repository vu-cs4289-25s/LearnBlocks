FROM python:3

EXPOSE 7070

WORKDIR /srv/learnblocks-api
COPY  . .
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "manage.py", "runserver", "7070"]
