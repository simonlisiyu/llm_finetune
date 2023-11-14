docker run -d --name localai --restart unless-stopped \
 -v /data/code/LocalAI/conf.env:/LocalAI/.env \
 -p 23620:23620 docker.art.com/dmc/alita