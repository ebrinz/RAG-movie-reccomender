### Notes so far


So far I can't figure out how to spin up the Ollama/ollama container
and pull Llama3, then run the serve command without exec'in in.

So, upon build exec into the container and run:

```ollama run llama3```
wait for download to complete

```ollama run serve``` <-- tho im not sure this is neccessary and may run defualt
can check ps aux here


test:


```
curl http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt": "Why is the sky blue?",
  "options": {
    "num_ctx": 2048
  }
}'
```