# Extends python-base image by installing python requirements (ONBUILD)
FROM mgbi/python-base:2

CMD ["python2", "/srv/contact_form.py"]

EXPOSE 5000

COPY . /srv
