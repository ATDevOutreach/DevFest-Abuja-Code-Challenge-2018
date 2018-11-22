FROM elixir:1.6.1


# Install Phoenix packages
RUN mix local.hex --force
RUN mix local.rebar --force


WORKDIR /app
ADD mix.exs mix.lock /app/
RUN mix do deps.get, deps.compile
ADD . .
EXPOSE 4000
