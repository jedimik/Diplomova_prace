FROM python:3

# set the working directory in the container
WORKDIR /app
# copy all local files from app
COPY /app /app
# install python libraries
RUN python3 -m pip install -r requirements.txt
# run start script inside container
CMD [ "sh", "./startscript.sh" ]