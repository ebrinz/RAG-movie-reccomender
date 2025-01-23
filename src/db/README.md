

```
docker exec -it db psql -U user -d movie_recco
```

```
movie_recco=# \d
             List of relations
 Schema |     Name      |   Type   | Owner
--------+---------------+----------+-------
 public | movies        | table    | user
 public | movies_id_seq | sequence | user
 ```
 