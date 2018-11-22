use Mix.Config

# We don't run a server during test. If one is required,
# you can enable the server option below.
config :wallet, WalletWeb.Endpoint,
  http: [port: 4002],
  server: false

# Print only warnings and errors during test
config :logger, level: :warn

# Configure your database
config :wallet, Wallet.Repo,
  username: System.get_env("DB_USER"),
  password: System.get_env("DB_PASSWORD"),
  database: "wallet_test",
  hostname: "localhost",
  pool: Ecto.Adapters.SQL.Sandbox
