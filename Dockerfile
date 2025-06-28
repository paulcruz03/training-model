FROM postgres:16

# Install dependencies
RUN apt-get update && apt-get install -y \
    postgresql-server-dev-16 \
    build-essential \
    git

# Clone the pgvector repository
RUN git clone --depth 1 https://github.com/pgvector/pgvector.git

# Build and install pgvector
RUN cd pgvector && make && make install

# Clean up build tools and cache
RUN apt-get remove -y build-essential git && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /pgvector
