defmodule Wallet.Repo do
  use Ecto.Repo,
    otp_app: :wallet,
    adapter: Ecto.Adapters.MySQL
end
