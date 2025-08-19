# Demo: Trino connection

Example URL:

```
trino://user@host:8080/catalog/schema
```

CLI:

```bash
~/.local/bin/dbsl connect trino1 "trino://user@localhost:8080/tpch/tiny"
~/.local/bin/dbsl schema --name trino1 --schema customer
~/.local/bin/dbsl sql --name trino1 "select * from customer limit 5"
```