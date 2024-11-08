docker run --name group1_proj --network monitoring -d -p 55550:7860 karate7800/cs553-project

#ngrok

ngrok http --log=log.txt http://localhost:55550 > /dev/null & ps auxww | grep ngrok

#TO view debug?
docker run -it --network monitoring --name group1_debug alpine