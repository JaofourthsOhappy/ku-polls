FROM python:3-alpine
ARG SECRET_KEY
ARG ALLOWED_HOSTS=127.0.0.1,localhost
WORKDIR /app/polls
ENV SECRET_KEY=${SECRET_KEY}
ENV DEBUG=True
ENV TIMEZONE=Asia/Bangkok
ENV ALLOWED_HOSTS=${ALLOWED_HOSTS:-127.0.0.1,localhost}
COPY ./requirements.txt .
# Install dependencies in Docker container
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

COPY ./entrypoint.sh .
EXPOSE 8000
RUN chmod +x ./entrypoint.sh
# Run application

CMD [ "./entrypoint.sh" ]
