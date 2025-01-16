FROM postgres:13

# Install dependencies required to build pgvector
RUN apt-get update && apt-get install -y \
      postgresql-server-dev-13 \
      gcc \
      make \
      curl \
  && \
  # Download and extract pgvector source code
  curl -L -o /tmp/pgvector.tar.gz https://github.com/pgvector/pgvector/archive/refs/tags/v0.2.0.tar.gz \
  && mkdir /tmp/pgvector \
  && tar -xf /tmp/pgvector.tar.gz -C /tmp/pgvector --strip-components=1 \
  && cd /tmp/pgvector \
  && make \
  && make install \
  && \
  # Clean up
  rm -rf /var/lib/apt/lists/* /tmp/pgvector /tmp/pgvector.tar.gz

EXPOSE 5432